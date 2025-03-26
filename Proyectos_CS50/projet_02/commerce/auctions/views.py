from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, AuctionListing, Bid, Comment, Category
from .forms import AuctionListingForm, BidForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# View to show active auction listings
def active_listings(request, category=None):
    # Get all active auctions
    if category:
       # Try filtering by category using the name
        listings = AuctionListing.objects.filter(active=True, category__name=category)
        if not listings.exists():
            # If there are no active auctions for this category, display an appropriate message
            return render(request, "auctions/active_listings.html", {
                "listings": listings,  # We pass the empty list
                "categories": Category.objects.all(),
                "message": "No hay subastas activas para esta categoría.",
                "selected_category": category,
            })
    else:
        # If no category is provided, get all active auctions
        listings = AuctionListing.objects.filter(active=True)

    # Make sure you also pass the list of categories to the context
    categories = Category.objects.all()
    return render(request, "auctions/active_listings.html", {
        "listings": listings,
        "categories": categories,
        "selected_category": category,  # To display the selected category
    })

# Manages user login; authenticates and redirects on success.    
def login_view(request):
    if request.method == "POST":
        # Attempt to log in the user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("active_listings"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

#Logs out the user and redirects to the active listings.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("active_listings"))

# Handles new user registration, ensuring username uniqueness and password confirmation
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure the passwords match
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create a new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("active_listings"))
    else:
        return render(request, "auctions/register.html")


# View to create a new auction listing
@login_required
def create_listing(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            if 'image' in request.FILES:
                print("File received: ", request.FILES['image'].name)  # Check if the file is received correctly
            return redirect('active_listings')

    else:
        form = AuctionListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})

# Handles the bidding process for auction listings, ensuring bids are valid and greater than current bids.
def place_bid(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    # Prevent the owner of the auction from bidding
    if request.user == listing.owner:
        messages.error(request, "You cannot bid on your own auction.")
        return render(request, 'auctions/place_bid.html', {
            'listing': listing,
            'form': BidForm(),  # Initialize a new form
        })

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to place a bid.")
        return redirect("login")  # Redirect to the login page

    if request.method == "POST":
        form = BidForm(request.POST)
        # Add class 'form-control' to the bid_amount field
        form.fields['bid_amount'].widget.attrs.update({'class': 'form-control'})
        
        if form.is_valid():
            bid = form.save(commit=False)
            current_price = listing.highest_bid()

            if bid.bid_amount > current_price:
                bid.user = request.user
                bid.listing = listing
                bid.save()
                # Update the current bid of the listing
                listing.current_bid = bid.bid_amount
                listing.save()
                return redirect('listing_detail', listing_id=listing.id)
            else:
                form.add_error('bid_amount', 'The bid must be higher than the current price.')
    else:
        # If the request is not POST, initialize an empty form with no errors
        form = BidForm()
        # Add class 'form-control' to the bid_amount field in GET
        form.fields['bid_amount'].widget.attrs.update({'class': 'form-control'})

    return render(request, 'auctions/place_bid.html', {
        'form': form,
        'listing': listing,
    })

# Displays details of a specific auction listing, including bids and comments.
def listing_detail(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    bids = Bid.objects.filter(listing=listing)
    comments = Comment.objects.filter(listing=listing)
    is_watching = request.user in listing.watchers.all()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            if request.user.is_authenticated:
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.listing = listing
                comment.save()
                messages.success(request, "Comment added successfully.")
                return redirect('listing_detail', listing_id=listing.id) 
            else:
                messages.warning(request, "You must be logged in to comment.")
                return redirect('login')  
    else:
        comment_form = CommentForm()

    return render(request, 'auctions/listing_detail.html', {
        'listing': listing,
        'bids': bids,
        'comments': comments,
        'is_watching': is_watching,
        'comment_form': comment_form 
    })


# Add a listing to the watchlist
def add_watchlist(request, listing_id):
    if request.user.is_authenticated:
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        listing.watchers.add(request.user)
        messages.success(request, "Listing added to your watchlist.")
        return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))
    else:
        messages.error(request, "You must be logged in to add listings to your watchlist.")
        return redirect("login")  # Redirect to the login page

# Allows users to remove listings from their watchlist.
@login_required
def remove_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    listing.watchers.remove(request.user)
  
    return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))

# Show a user's watchlist
@login_required
def watchlist_view(request):
    # Get the auctions that the user has added to their watchlist
    watchlist_items = AuctionListing.objects.filter(watchers=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

# Displays the auction listings owned by the logged-in user.
@login_required
def my_listings_view(request):
    user_listings = AuctionListing.objects.filter(owner=request.user)
    return render(request, "auctions/my_listings.html", {
        "listings": user_listings
    })

# Allows users to delete their own auction listings.
@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    # Check if the user is the creator of the listing
    if request.user != listing.owner:
        return HttpResponseRedirect(reverse('listing_detail', args=[listing_id]))

    # Delete the listing if the user is the creator
    listing.delete()
    return redirect('active_listings')

# Allows users to edit their own auction listings.
@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    # Check if the user is the creator of the listing
    if request.user != listing.owner:
        return HttpResponseRedirect(reverse('listing_detail', args=[listing_id]))

    if request.method == "POST":
        form = AuctionListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', listing_id=listing.id)
    else:
        form = AuctionListingForm(instance=listing)

    return render(request, 'auctions/edit_listing.html', {'form': form, 'listing': listing})

# Allows users to close their auction listings
@login_required
def finalize_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    # Only the owner can end the auction
    if request.user != listing.owner:
        messages.error(request, "No tienes permiso para finalizar esta subasta.")
        return redirect('listing_detail', listing_id=listing_id)

    # Get the winning bid
    winning_bid = listing.bids.order_by('-bid_amount').first()
    if winning_bid:
        listing.winner = winning_bid.user
        messages.success(request, f"La subasta ha finalizado. El ganador es {winning_bid.user.username}")
    else:
        messages.info(request, "La subasta ha finalizado sin ofertas.")
    
    # Mark auction as inactive
    listing.active = False
    listing.save()

    return redirect('listing_detail', listing_id=listing_id)

# Provides a search functionality for auction listings based on user queries.
@login_required
def won_auctions_view(request):
    # Filtramos subastas donde el usuario actual es el ganador
    won_listings = AuctionListing.objects.filter(winner=request.user)
    return render(request, "auctions/won_auctions.html", {
        "won_listings": won_listings
    })

def search(request):
    query = request.GET.get("query", "")
    results = AuctionListing.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        active=True
    )
    return render(request, "auctions/search_results.html", {
        "query": query,
        "results": results
    })
