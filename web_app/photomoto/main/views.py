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
from .models import Portfolio, PortfolioImage
from .forms import AvatarForm
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
@login_required
def personal_account(request):
    if request.method == 'POST' and 'images' in request.FILES:
        genre = request.POST.get('genre', 'portrait')
        images = request.FILES.getlist('images')

        for image in images:
            PortfolioPhoto.objects.create(
                user=request.user,
                image=image,
                genre=genre
            )

        return redirect('personal_account')

    if request.method == 'POST' and 'avatar' in request.FILES:
        request.user.avatar = request.FILES['avatar']
        request.user.save()
        return redirect('personal_account')

    if request.method == 'POST' and 'delete_avatar' in request.POST:
        if request.user.avatar:
            request.user.avatar.delete()
            request.user.avatar = None
            request.user.save()
        return redirect('personal_account')

    photos = PortfolioPhoto.objects.filter(user=request.user)

    photos_by_genre = defaultdict(list)
    for photo in photos:
        photos_by_genre[photo.genre].append(photo)

    genre_names = {
        'portrait': 'Портрет',
        'landscape': 'Пейзаж',
        'interior': 'Интерьер',
        'reportage': 'Репортаж',
    }

    return render(request, 'main/personal_account.html', {
        'photos': photos,
        'photos_by_genre': dict(photos_by_genre),
        'genre_names': genre_names,
    })

