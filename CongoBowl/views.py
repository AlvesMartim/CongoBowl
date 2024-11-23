from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, 'index.html')

def apropos(request):
    return render(request,'apropos.html')

def produits(request):
    return render(request,'produits.html')

def sign_in(request):
    if request.method =='POST':
        return 1
    return render(request,'sign_in.html')

def log_in(request):
    return render(request,'log_in.html')

