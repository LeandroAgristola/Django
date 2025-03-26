from django import template

register = template.Library()

@register.filter
def profile_picture_or_default(profile_picture):
    if profile_picture:
        return profile_picture.url
    return '/static/network/user/default_profile.jpg'