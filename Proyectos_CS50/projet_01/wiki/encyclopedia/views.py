from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })

def search(request):
    query = request.GET.get('q')
    if not query:
        return redirect('index')
    
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
    
    if len(matching_entries) == 1 and matching_entries[0].lower() == query.lower():
        return redirect('entry_page', title=matching_entries[0])
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": matching_entries
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })
        
        util.save_entry(title, content)
        return redirect('entry_page', title=title)
    
    return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('entry_page', title=title)
    
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry_page', title=random_entry)