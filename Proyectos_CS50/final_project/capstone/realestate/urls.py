from django.urls import path
from realestate import views
from django.conf import settings 
from django.conf.urls.static import static

# URL patterns for the project
urlpatterns = [
    # Home page route, linked to the home view
    path('', views.home, name="home"),
    
    # Login page route, linked to the login view
    path("login", views.login_view, name="login"),
    
    # Logout page route, linked to the logout view
    path("logout", views.logout_view, name="logout"),
    
    # Management page route, linked to the management view (admin section)
    path('management/', views.management, name='management'),
    
    # Add a new development project page route, linked to the add_development view
    path('management/add/', views.add_development_view, name='add_development'),
    
    # Edit an existing development project page route, linked to the edit_development view
    # The <int:dev_id> part of the path allows for dynamic handling of development IDs
    path('management/edit/<int:dev_id>/', views.edit_development, name='edit_development'),
    
    # Routes for different types of mobile properties
    path('mobiledDwelling/', views.mobiledDwelling, name='mobiledDwelling'),
    path('mobileBuildings/', views.mobileBuildings, name='mobileBuildings'),
    path('mobileIndustries/', views.mobileIndustries, name='mobileIndustries'),
]

# If the project is in DEBUG mode (development environment), allow static media file access
if settings.DEBUG:
    # This will serve media files from the MEDIA_URL path and store them in MEDIA_ROOT
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
