from django.shortcuts import render, redirect 
from .models import Posts
from .forms import PostsForm
from django.contrib.auth.decorators import login_required

def news_home(request):
    news = Posts.objects.order_by('title')
    return render(request, 'news/news_home.html', {"news": news})



@login_required
def create(request):
    if request.method == "POST":
        form = PostsForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("news_home")
    else:
        form = PostsForm()

    return render(request, "news/create.html", {"form": form})

# Create your views here.
