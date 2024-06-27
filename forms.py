from django import forms
from .models import Book
from .models import sign

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'description', 'cover_photo', 'status']
        widgets = {
            'status': forms.HiddenInput(),
        }

class signform(forms.Form):

    username = forms.CharField(max_length=50) 
    last= forms.CharField(max_length=50)
    password= forms.CharField(max_length=50)
    email= forms.CharField(max_length=50)
    user = forms.BooleanField()
    admin = forms.BooleanField()


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)        