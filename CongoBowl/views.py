from datetime import datetime

from django.shortcuts import render,redirect

from .forms import SignInForm, LogInForm
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages


def index(request):
    pseudo = request.session['utilisateur_pseudo']
    return render(request, 'index.html',{'pseudo':pseudo})

def apropos(request):
    return render(request,'apropos.html')

def produits(request):
    return render(request,'produits.html')

def sign_in(request):
    if request.method =='POST':
        form =  SignInForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.mot_de_passe = make_password(form.cleaned_data['mot_de_passe']) #Hashage du mdp
            utilisateur.save() # Sauv dans la BD
            request.session['utilisateur_pseudo'] = utilisateur.pseudo
            request.session['utilisateur_mot_de_passe'] = utilisateur.mot_de_passe
            request.session['utilisateur_id'] = utilisateur.id
            print(utilisateur.id)
            return redirect('index')
    else :
        form = SignInForm()
    return render(request,'sign_in.html',{'form':form})

def log_in(request):
    if request.method =='POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            pseudo = form.cleaned_data['pseudo']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            #Vérif de données
            try:
                utilisateur = Utilisateur.objects.get(pseudo=pseudo)
                if check_password(mot_de_passe, utilisateur.mot_de_passe):
                    request.session['utilisateur_pseudo'] = utilisateur.pseudo
                    request.session['utilisateur_id'] = utilisateur.id
                    messages.success(request, "Connexion réussie.")
                    return redirect('index')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Utilisateur.DoesNotExist:
                messages.error(request, "Pseudo incorrect ou inexistant.")
    else:
        form = LogInForm()
    return render(request,'log_in.html', {'form':form})

