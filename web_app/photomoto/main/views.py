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
from .models import Photo 
from django.contrib import messages 
from django.contrib.auth import get_user_model
from collections import defaultdict
from django.db.models import Q

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

def update_resume(request):
    if request.method == 'POST':
        user = request.user
        user.resume_city = request.POST.get('city', '')
        selected_genres = request.POST.getlist('genres')
        user.resume_genres = ','.join(selected_genres)
        user.save()
        messages.success(request, 'Резюме успешно обновлено!')
        return redirect('personal_account')
    
@login_required
def delete_photo(request, photo_id):
    """Удаление фото из портфолио"""
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    if photo.image:
        photo.image.delete()  # удаляем файл с диска
    photo.delete()
    return redirect('personal_account')  

@login_required
def bulk_delete_photos(request):
    if request.method == 'POST':
        photo_ids = request.POST.get('photo_ids', '').split(',')
        if photo_ids and photo_ids[0]:  # проверка, что список не пустой
            Photo.objects.filter(id__in=photo_ids, user=request.user).delete()
    return redirect('personal_account')

def profile(request, user_id):
    User = get_user_model()
    profile_user = get_object_or_404(User, id=user_id)

    try:
        from .models import Photo
        photos = PortfolioPhoto.objects.filter(user=profile_user)

        photos_by_genre = defaultdict(list)

        for photo in photos:
            photos_by_genre[photo.genre].append(photo)

        genre_names = {
            'portrait': 'Портрет',
            'landscape': 'Пейзаж',
            'interior': 'Интерьер',
            'reportage': 'Репортаж',
        }
    except:
        photos = []
    
    context = {
    'profile_user': profile_user,
    'photos_by_genre': dict(photos_by_genre),
    'genre_names': genre_names,
}
    return render(request, 'main/profile.html', context)



def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    photos = PortfolioPhoto.objects.filter(user=profile_user)

    photos_by_genre = defaultdict(list)

    for photo in photos:
        photos_by_genre[photo.genre].append(photo)

    genre_names = {
        'portrait': 'Портрет',
        'landscape': 'Пейзаж',
        'interior': 'Интерьер',
        'reportage': 'Репортаж',
    }

    return render(request, 'main/user_profile.html', {
        'profile_user': profile_user,
        'photos_by_genre': dict(photos_by_genre),
        'genre_names': genre_names,
    })



def index(request):
    users = CustomerUser.objects.filter(
        resume_city__isnull=False
    ).exclude(
        resume_city=""
    )

    genre = request.GET.get('genre', '')
    city = request.GET.get('city', '')

    if genre:
        users = users.filter(resume_genres__icontains=genre)

    if city:
        users = users.filter(resume_city__icontains=city)

    for user in users:
        genres = []

        if user.resume_genres:
            if 'portrait' in user.resume_genres:
                genres.append('Портрет')

            if 'landscape' in user.resume_genres:
                genres.append('Пейзаж')

            if 'interior' in user.resume_genres:
                genres.append('Интерьер')

            if 'reportage' in user.resume_genres:
                genres.append('Репортаж')

        user.genres_ru = ', '.join(genres)

    return render(request, 'main/index.html', {
        'users': users,
        'selected_genre': genre,
        'selected_city': city,
    })