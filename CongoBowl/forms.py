from django import forms
from .models import Utilisateur

class SignInForm(forms.ModelForm):
    nom = forms.CharField(widget=forms.TextInput, required=True)
    prenom = forms.CharField(widget=forms.TextInput, required=True)
    pseudo = forms.CharField(widget=forms.TextInput, required=True)
    email = forms.CharField(widget=forms.EmailInput, required=True)
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom','pseudo', 'email', 'mot_de_passe']

class LogInForm(forms.Form):
    pseudo = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Votre pseudo'}), required=True)
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Votre Mot de Passe'}), required=True)

