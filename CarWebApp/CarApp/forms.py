from django import forms
from .models import  CarBooked
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,get_user_model,login,logout

from .views import *
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User

        fields = ('first_name','last_name','username', 'email','password')
        widgets = {
        'password': forms.PasswordInput(),
        }

class LoginForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:

        model = User

        fields = ('username','password')
        widgets = {
        'password': forms.PasswordInput(),
        }



class BookForm(forms.ModelForm):
    note=forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Aggiungi note..'}))
    place=forms.CharField(label="Dove?",widget=forms.TextInput(attrs={'placeholder': 'Aggiungi luogo..'}))
    class Meta:
        model = CarBooked

        fields=('frombooked','tobooked','place','note')


class modifybookForm(forms.ModelForm):
    note=forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Aggiungi note..'}))
    place=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Aggiungi luogo..'}))
    class Meta:
        model = CarBooked

        fields=('frombooked','tobooked','place','note')
