from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

# URL patterns for the application
urlpatterns = [
    # Main page
    path("", views.index, name="index"),
    
    # User login
    path("login", views.login_view, name="login"),
    
    # User logout
    path("logout", views.logout_view, name="logout"),
    
    # User registration
    path("register", views.register, name="register"),
    
    # Profile page for a specific user
    path("profile/<str:username>", views.profile_view, name="profile"),
    
    # Page showing posts from followed users
    path("following", views.following_view, name="following"),
    
    # Search functionality
    path("search/", views.search, name="search"),
    
    # Edit an existing post
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    
    # Toggle like/unlike for a specific post
    path("toggle_like/<int:post_id>/", views.toggle_like, name="toggle_like"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
