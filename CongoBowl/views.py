from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def apropos(request):
    return render(request,'apropos.html')

def produits(request):
    return render(request,'produits.html')

def sign_in(request):
    return render(request,'sign_in')

def log_in(request):
    return render(request,'log_in')