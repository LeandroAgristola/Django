from django.contrib import admin
from .models import User, Post

# Custom admin for the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    # Fields to search in the admin panel
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Filters to narrow down the list of users
    list_filter = ('is_staff', 'is_active')

    # Enable deleting users directly from the admin
    actions = ['delete_selected']

# Custom admin for the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = ('user', 'content_snippet', 'created_at', 'like_count')
    
    # Fields to search in the admin panel
    search_fields = ('content', 'user__username')
    
    # Filters to narrow down the list of posts
    list_filter = ('created_at',)
    
    # Enable deleting posts directly from the admin
    actions = ['delete_selected']

    # Method to show a snippet of the post's content
    def content_snippet(self, obj):
        return obj.content[:50]  # Display the first 50 characters
    content_snippet.short_description = 'Content'
