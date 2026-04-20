from django.urls import path
from . import views 
from .views import *

urlpatterns = [
    path('', views.index , name= 'home'),
    path('about', views.about),
    path('login/', LoginUser.as_view() , name ="login"),
    path('logout/', logout_user , name ="logout"),
    path('register/', RegisterUser.as_view() , name ="register"),
    path('personal-account/', views.personal_account, name='personal_account'),
    path('delete-photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('bulk-delete-photos/', views.bulk_delete_photos, name='bulk_delete_photos'),
    path('update-resume/', views.update_resume, name='update_resume'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    ]
