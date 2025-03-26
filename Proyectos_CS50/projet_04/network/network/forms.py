from django import forms
from .models import Post, User

# Form for creating and editing posts
class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # Associate the form with the Post model
        fields = ['content']  # Include only the 'content' field in the form
        widgets = {
            # Customize the 'content' field with a textarea widget
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'What are you thinking??'
            }),
        }
        labels = {
            # Remove the label for the 'content' field
            'content': '',
        }

# Custom form for user registration
class CustomUserCreationForm(forms.ModelForm):
    # Field for entering the user's password
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    
    # Field for confirming the user's password
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User  # Associate the form with the User model
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']  # Include these fields in the form
        widgets = {
            # Customize the 'username' field
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Username'
            }),
            # Customize the 'email' field
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email Address'
            }),
            # Customize the 'first_name' field
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'First Name'
            }),
            # Customize the 'last_name' field
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Last Name'
            }),
            # Customize the 'profile_picture' field
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
