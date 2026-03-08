from .models import Posts
from django.forms import ModelForm, TextInput, FileInput



class PostsForm(ModelForm):
    class Meta:
        model = Posts
        fields =['title','annons','photo' ]

        widgets ={
            'title':TextInput(attrs={
                'class':'form-control',
                'placeholder':'Название поста'
            }),
            'annons':TextInput(attrs={
                'class':'form-control',
                'placeholder':'Описание'
            }),

            'photo':FileInput(attrs={
                'class':'form-control'
                
            })
          
        }