from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", views.active_listings, name="active_listings"),
    path("won_auctions/", views.won_auctions_view, name="won_auctions"), 
    path("create/", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("listing/<int:listing_id>/finalize", views.finalize_listing, name="finalize_listing"),
    path("search/", views.search, name="search"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/delete", views.delete_listing, name="delete_listing"),
    path("listing/<int:listing_id>/edit", views.edit_listing, name="edit_listing"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path('watchlist/', views.watchlist_view, name='watchlist_view'),
    path("my_listings/", views.my_listings_view, name="my_listings_view"),
    path("<str:category>/", views.active_listings, name="active_listings_by_category"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)