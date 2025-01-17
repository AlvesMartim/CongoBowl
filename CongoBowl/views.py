from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth.hashers import make_password, check_password #Gestion MDP
from django.contrib import messages #Alertes
from django.shortcuts import get_object_or_404 #Gérer les erreurs


def index(request):
    context = {
        'pseudo' : request.session.get('utilisateur_pseudo',None)
    }
    return render(request, 'index.html',context)

def apropos(request):
    return render(request,'apropos.html')

def panier(request):
    if not request.session.get('utilisateur_id'):
        messages.error(request, "Veuillez vous connecter pour voir votre panier.")
        return redirect('log_in')
    
    utilisateur = Utilisateur.objects.get(id=request.session['utilisateur_id'])
    panier = Commande.objects.filter(utilisateur=utilisateur, statut='non paye').first()

    articles_commandes = ArticlesCommandes.filter(commande_id=panier) if panier else []
    articles = Article.objects

    context = {
        'pseudo': request.session.get('utilisateur_pseudo', None),
        'articles_commandes': articles_commandes
    }
    return render(request, 'panier.html', context)

def produits(request):
    if request.method == 'GET':
        articles = Article.objects.filter(statut='publie')
        context = {
            'pseudo': request.session.get('utilisateur_pseudo', None),
            'articles': articles
        }
        return render(request, 'produits.html',context)


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

def ajouter_panier(request, article_id):
    #Recup/Crée panier
    if not request.session.get('utilisateur_id'):
        messages.error(request, "Veuillez vous connecter pour ajouter des articles au panier.")
        return redirect('log_in')

    utilisateur = Utilisateur.objects.get(id=request.session['utilisateur_id'])
    panier = get_or_create_panier(utilisateur)

    #Ajout au panier
    article = get_object_or_404(Article, id=article_id)
    article_commande, created = ArticlesCommandes.objects.get_or_create(
        article_id=article,
        commande_id=panier,
    )
    if not created:
        article_commande.quantite += 1
        article_commande.save()

    messages.success(request, f"L'article {article.titre} a été ajouté au panier.")
    return redirect('produits')
    
def get_or_create_panier(utilisateur):
    panier, created = Commande.objects.get_or_create_panier(utilisateur)
    return panier



#oeeeeeeeeeeeee