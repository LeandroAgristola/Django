from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

# Custom registration form for the User model
class UserRegistrationForm(UserCreationForm):
    # Field for the user's first name, required with a maximum length of 30 characters
    first_name = forms.CharField(max_length=30, required=True)
    # Field for the user's last name, required with a maximum length of 30 characters
    last_name = forms.CharField(max_length=30, required=True)
    # Optional field for uploading a profile picture
    profile_picture = forms.ImageField(required=False)

    class Meta:
        # Specifies the model and fields to include in the form
        model = User
        fields = ["first_name", "last_name", "email", "profile_picture", "password1", "password2"]

    # Initializes the form and customizes its behavior
    def __init__(self, *args, **kwargs):
        # Check if the form is being used to edit an existing user instance
        editing = kwargs.get('instance') is not None
        super().__init__(*args, **kwargs)

        # Remove the email field if editing an existing user
        if editing:
            self.fields.pop("email")

        # Add 'form-control' CSS class to all fields for consistent styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # Validates the uploaded profile picture
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get("profile_picture")

        # If no picture is uploaded, skip further validation
        if not profile_picture:
            return profile_picture

        # Allow only JPEG and PNG image formats
        if profile_picture.content_type not in ["image/jpeg", "image/png"]:
            raise ValidationError("Only JPEG and PNG images are allowed.")

        # Enforce a maximum file size of 2 MB
        max_size_kb = 2048
        if profile_picture.size > max_size_kb * 1024:
            raise ValidationError(f"The maximum image size is {max_size_kb / 1024} MB.")

        return profile_picture

    # Saves the user instance and assigns a username based on the email if it's a new user
    def save(self, commit=True):
        user = super().save(commit=False)
        # Set the username to the email if creating a new user
        if not self.instance.pk:
            user.username = self.cleaned_data["email"]
        # Save the user instance if commit is True
        if commit:
            user.save()
        return user
