from django.shortcuts import render, redirect
from .utils import *
from .forms import *
from .models import *
def index(request):
    return render(request, 'main/index.html' )

def about(request):
    
    return render(request, 'main/about.html' )
