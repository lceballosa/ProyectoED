from django.forms import ModelForm
from django import forms    
from django.contrib.auth.models import User
from .models import usuarios, fech_corta


class OrderForm(ModelForm):
    class Meta:
        model=usuarios
        fields= '__all__'
