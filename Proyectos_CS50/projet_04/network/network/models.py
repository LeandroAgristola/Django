from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom user model extending Django's AbstractUser
class User(AbstractUser):
    # First name of the user
    first_name = models.CharField(max_length=30)
    
    # Last name of the user
    last_name = models.CharField(max_length=30)
    
    # Profile picture of the user, with a default image
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        null=True, 
        blank=True, 
        default='user/default_profile.jpg'
    )
    
    # Followers of the user (many-to-many relationship with other users)
    followers = models.ManyToManyField(
        'self', 
        related_name='following', 
        symmetrical=False, 
        blank=True
    )

# Model representing a post created by a user
class Post(models.Model):
    # The user who created the post
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="posts"
    )
    
    # Content of the post, limited to 280 characters
    content = models.TextField(max_length=280)
    
    # Timestamp of when the post was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Users who liked the post (many-to-many relationship)
    likes = models.ManyToManyField(
        User, 
        related_name="liked_posts", 
        blank=True
    )

    # Method to count the number of likes on the post
    def like_count(self):
        return self.likes.count()

    # String representation of the post, showing the user and a snippet of the content
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
