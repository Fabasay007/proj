from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomerUser
from django.contrib.auth.forms import AuthenticationForm

class CustomerUserForm(UserCreationForm):
    avatar = forms.ImageField(required=False, label ='Аватарка')
    age = forms.IntegerField(required=True, label='Возраст')
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    phone_number = forms.CharField(required=True, label ='Номер телефона')

    class Meta:
        model = CustomerUser
        fields = ('username', 'age','email','phone_number', 'avatar', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.avatar = self.cleaned_data.get('avatar')  
        user.phone_number = self.cleaned_data['phone_number']
        user.age = self.cleaned_data['age']
        if commit:
            user.save()
        return user
