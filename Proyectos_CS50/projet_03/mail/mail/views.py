import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Email
from .forms import UserRegistrationForm

# This view checks if the user is authenticated. If yes, it loads the inbox view. If not, redirects to the login page.
def index(request):
    if request.user.is_authenticated:
        return render(request, "mail/inbox.html")
    else:
        return HttpResponseRedirect(reverse("login"))

# Handle composing a new email. Only POST method is allowed, and it processes the form data to create and save the email.
@csrf_exempt
@login_required
def compose(request):
    # Only allow POST requests
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Parse the request body to extract email details
    data = json.loads(request.body)
    emails = [email.strip() for email in data.get("recipients", "").split(",")]
    
    # Check if at least one recipient is provided
    if emails == [""]:
        return JsonResponse({"error": "At least one recipient required."}, status=400)

    recipients = []
    for email in emails:
        try:
            # Get the user object for each recipient email
            user = User.objects.get(email=email)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({"error": f"User with email {email} does not exist."}, status=400)

    # Extract the subject and body of the email
    subject = data.get("subject", "")
    body = data.get("body", "")

    # Create and save emails for each recipient
    for recipient in recipients:
        email = Email(
            user=recipient,           
            sender=request.user,       
            subject=subject,
            body=body,
            read=False  # Mark as unread initially
        )
        email.save()
        email.recipients.add(*recipients)  # Add all recipients to the email
        email.save()

    # Save the sent email as well
    email_sent = Email(
        user=request.user,          
        sender=request.user,
        subject=subject,
        body=body,
        read=True  # Sent emails are marked as read
    )
    email_sent.save()
    email_sent.recipients.add(*recipients)
    email_sent.save()

    # Return a success message
    return JsonResponse({"message": "Email sent successfully."}, status=201)

# This view handles retrieving emails from different mailboxes (inbox, sent, archived)
@login_required
def mailbox(request, mailbox):
    # Determine which mailbox to retrieve based on the URL parameter
    if mailbox == "inbox":
        emails = Email.objects.filter(user=request.user, recipients=request.user, archived=False)
    elif mailbox == "sent":
        emails = Email.objects.filter(user=request.user, sender=request.user)
    elif mailbox == "archive":
        emails = Email.objects.filter(user=request.user, recipients=request.user, archived=True)
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Order emails by timestamp in descending order and serialize them
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)

# This view handles a specific email (view, update, or delete an email)
@csrf_exempt
@login_required
def email(request, email_id):
    try:
        # Retrieve the email by ID for the current user
        email = Email.objects.get(user=request.user, pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    if request.method == "GET":
        # Return the email details
        return JsonResponse(email.serialize())

    elif request.method == "PUT":
        # Update the email's read status or archived status
        data = json.loads(request.body)
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        email.save()
        return HttpResponse(status=204)

    elif request.method == "DELETE":
        # Delete the email
        email.delete()
        return JsonResponse({"message": "Email deleted successfully."}, status=204)

    else:
        return JsonResponse({"error": "Method not allowed."}, status=400)

# Handle user login, checking the credentials and redirecting accordingly
def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in and redirect to the index page
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mail/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "mail/login.html")

# Log out the user and redirect to the index page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Handle user registration, including form validation and saving user data
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            
            # If a profile picture is uploaded, save it
            if request.FILES.get("profile_picture"):
                user.profile_picture = request.FILES["profile_picture"]
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # If form submission fails, return an error message
            return render(request, "mail/register.html", {"form": form, "message": "Error in form submission."})
    else:
        # Display the registration form
        form = UserRegistrationForm()
        return render(request, "mail/register.html", {"form": form})
