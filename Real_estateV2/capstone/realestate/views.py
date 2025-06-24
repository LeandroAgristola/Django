from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import contactForm, DevelopmentForm
from .models import development

# Home page view
def home(request):
    # Fetch all development projects
    developments = development.objects.all()

    # Handle form submission
    if request.method == "POST":
        forms_contact = contactForm(data=request.POST)
        if forms_contact.is_valid():
            # Extract cleaned data from the form
            name = forms_contact.cleaned_data['name']
            lastname = forms_contact.cleaned_data['lastname']
            phonenumber = forms_contact.cleaned_data['phonenumber']
            email = forms_contact.cleaned_data['email']
            consultation = forms_contact.cleaned_data['consultation']

            # Create the email message with the provided data
            email_message = EmailMessage(
                "Message from Real Estate",
                f"Name: {name} {lastname}\nPhonenumber: {phonenumber}\nEmail: {email}\nConsultation: {consultation}",
                "#",  # Sender email (replace with actual email)
                ["#"],  # Recipient email (replace with actual email)
                reply_to=[email]
            )

            try:
                # Attempt to send the email
                email_message.send()
                return JsonResponse({'status': 'ok'}, status=200)
            except Exception as e:
                # Handle email send errors
                print(f"Error sending email: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            # Return validation errors if form is invalid
            errors = forms_contact.errors.as_json()
            return JsonResponse({'status': 'invalid', 'errors': errors}, status=400)
    
    # If GET request, render the page with an empty contact form
    forms_contact = contactForm()
    return render(request, 'realestate/home.html', {
        'developments': developments, 
        'myform': forms_contact
    })

# Management page view, requires login
@login_required(login_url='login')
def management(request):
    # Fetch all development projects
    developments = development.objects.all()

    # Handle delete request
    if request.method == 'POST':
        if 'delete' in request.POST:
            ids_to_delete = request.POST.getlist('development_ids')

            # Delete selected development projects
            for dev_id in ids_to_delete:
                obj = get_object_or_404(development, id=dev_id)
                obj.delete() 
            
            # Redirect to management page after deletion
            return redirect('management')
    
    # Render the management page with all developments
    return render(request, 'realestate/management.html', {
        'developments': developments
    })

# Add development page view, requires login
@login_required(login_url='login')
def add_development_view(request):
    # Handle form submission
    if request.method == 'POST':
        form = DevelopmentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the new development project
            form.save()
            return redirect('management')
    else:
        form = DevelopmentForm()
    
    # Render the add development form page
    return render(request, 'realestate/add_development.html', {'form': form})

# Edit development page view, requires login
@login_required(login_url='login')
def edit_development(request, dev_id):
    # Fetch the development project to be edited
    dev = get_object_or_404(development, id=dev_id)

    # Handle form submission for editing
    if request.method == 'POST':
        form = DevelopmentForm(request.POST, request.FILES, instance=dev)
        if form.is_valid():
            # Save the updated development project
            form.save()
            return redirect('management')
    else:
        form = DevelopmentForm(instance=dev)

    # Render the edit development form page
    return render(request, 'realestate/edit_development.html', {'form': form, 'development': dev})

# Login view
def login_view(request):
    if request.method == "POST":
        # Authenticate user with provided username and password
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication successful, log the user in and redirect to management page
            login(request, user)
            return HttpResponseRedirect(reverse("management"))
        else:
            # If authentication fails, render login page with an error message
            return render(request, "realestate/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        # Render login page for GET request
        return render(request, "realestate/login.html")

# Logout view
def logout_view(request):
    # Log the user out and redirect to home page
    logout(request)
    return HttpResponseRedirect(reverse("home"))

# Views for different property types
def mobiledDwelling(request):
    # Render page for mobile dwelling properties
    return render(request, 'realestate/mobiledDwelling.html')

def mobileBuildings(request):
    # Render page for mobile buildings properties
    return render(request, 'realestate/mobileBuildings.html')

def mobileIndustries(request):
    # Render page for mobile industries properties
    return render(request, 'realestate/mobileIndustries.html')
