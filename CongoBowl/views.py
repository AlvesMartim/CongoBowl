from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth.hashers import make_password, check_password #Gestion MDP
from django.contrib import messages #Alertes


def index(request):
    context = {
        'pseudo' : request.session.get('utilisateur_pseudo',None)
    }
    return render(request, 'index.html',context)

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
                    request.session['is_authenticated'] = True
                    request.session.set_expiry(3600)  # Session expire après 1 heure


                    messages.success(request, "Connexion réussie.")
                    return redirect('index')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Utilisateur.DoesNotExist:
                messages.error(request, "Pseudo incorrect ou inexistant.")
    else:
        form = LogInForm()
    return render(request,'log_in.html', {'form':form})

def log_out(request):
    # Supprime toutes les données de session
    request.session.flush()
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('index')