from django.shortcuts import render, redirect 
from .models import Posts
from .forms import PostsForm


def news_home(request):
    news = Posts.objects.order_by('title')
    return render(request, 'news/news_home.html', {"news": news})

def create(request):
    if request.method == "POST":
        form = PostsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error='PUPUPU'
    form = PostsForm()

    data ={
        'form' : form
    }
    return render(request, 'news/create.html', data)

# Create your views here.
