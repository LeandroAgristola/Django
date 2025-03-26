from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom user model extending AbstractUser to add extra fields
class User(AbstractUser):
    # Stores the user's first name with a maximum length of 30 characters
    first_name = models.CharField(max_length=30)
    # Stores the user's last name with a maximum length of 30 characters
    last_name = models.CharField(max_length=30)
    # Optional profile picture for the user, stored in 'profile_pics/' directory
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

# Model representing an email with its properties and relationships
class Email(models.Model):
    # The user to whom the email is associated
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
    # The sender of the email; protected from deletion to maintain data integrity
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
    # Recipients of the email; allows multiple users
    recipients = models.ManyToManyField("User", related_name="emails_received")
    # Subject line of the email with a maximum length of 255 characters
    subject = models.CharField(max_length=255)
    # Body content of the email; can be left blank
    body = models.TextField(blank=True)
    # Timestamp indicating when the email was created
    timestamp = models.DateTimeField(auto_now_add=True)
    # Boolean flag indicating if the email has been read
    read = models.BooleanField(default=False)
    # Boolean flag indicating if the email has been archived
    archived = models.BooleanField(default=False)

    # Method to serialize the email object into a dictionary format
    def serialize(self):
        return {
            "id": self.id,  # Unique identifier for the email
            "sender": self.sender.email,  # Email address of the sender
            "recipients": [user.email for user in self.recipients.all()],  # List of recipient emails
            "subject": self.subject,  # Subject of the email
            "body": self.body,  # Body content of the email
            "timestamp": self.timestamp,  # Date and time the email was created
            "read": self.read,  # Read status of the email
            "archived": self.archived,  # Archived status of the email
            "sent": self.sender == self.user  # Indicates if the email was sent by the user
        }
