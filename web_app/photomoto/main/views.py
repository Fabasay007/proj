from django.shortcuts import render, redirect
from .utils import *
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request, 'main/index.html' )

def about(request):
    
    return render(request, 'main/about.html' )
class RegisterUser(DataMixin, CreateView):
    form_class = CustomerUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_contex_data(self, *, object_list =None,**kwargs):
        context = super(). get_contex_data(**kwargs)
        c_def = self.get_user_context(title ="Регистрация")
        return dict(list(context.items())+ list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('home')
    
class LoginUser( DataMixin, LoginView ):
    form_class = LoginUserForm
    template_name= 'main/login.html'

    def get_context_data(self, *, object_list = None,**kwargs ):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Авторизация')
        return dict(list(context.items())+ list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')
