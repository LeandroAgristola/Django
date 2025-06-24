from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import development
import re

# Custom validator to ensure the field contains only letters
def validateOnlyLetters(value):
    if not value.isalpha():
        raise ValidationError('This field must contain only letters.')

# Custom validator to ensure the field contains only numeric characters
def validateOnlynumbers(value):
    if not re.match(r'^\d+$', value):
        raise ValidationError('The phone number must contain only numbers.')

# Custom validator to ensure the email address format is valid
def validateOnlyemail(value):
    try:
        validate = EmailValidator()
        validate(value)  # Validate the email
    except ValidationError:
        raise ValidationError('Please enter a valid email.')  
    return True 

# Form for the contact page
class contactForm(forms.Form):
    # Field for the user's first name
    name = forms.CharField(
        max_length=100,
        validators=[validateOnlyLetters],  # Ensures only letters are allowed
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ethan'  # Placeholder text for the input field
        })
    )
    # Field for the user's last name
    lastname = forms.CharField(
        max_length=100,
        validators=[validateOnlyLetters],  # Ensures only letters are allowed
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'James'
        })
    )
    # Field for the user's phone number
    phonenumber = forms.CharField(
        max_length=20,
        validators=[validateOnlynumbers],  # Ensures only numbers are allowed
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0115345456'
        })
    )
    # Field for the user's email address
    email = forms.EmailField(
        validators=[validateOnlyemail],  # Ensures the email format is valid
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@djangomail.com'
        })
    )
    # Field for the user's query or message
    consultation = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,  # Number of rows in the text area
            'placeholder': 'Write your query here'
        })
    )

# Model form for adding or editing a development project
class DevelopmentForm(forms.ModelForm):
    class Meta:
        model = development  # Links the form to the 'development' model
        fields = ['title', 'content', 'image', 'brochurePaper']  # Specifies the fields to include

        # Customizes the appearance of each field in the form
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the content',
                'rows': 6  # Number of rows in the text area
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'brochurePaper': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
