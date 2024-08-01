from django.shortcuts import render
from blog.models import Post #importamos el servicio del models de la APP servicios para poder trabajar sobre la vista servicios

# Create your views here.


def blog(request):
    posts=Post.objects.all()
    return render(request,"blog/blog.html", {"posts": posts})