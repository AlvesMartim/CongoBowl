from django.db import models

class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, db_column='nom')
    prenom = models.CharField(max_length=100, db_column='prenom')
    pseudo = models.CharField(max_length=100, db_column='pseudo', unique =True)
    email = models.EmailField(unique=True, db_column='mail')
    mot_de_passe = models.CharField(max_length=100, db_column='mot_de_passe')
    date_inscription = models.DateTimeField(auto_now_add=True, db_column='date_inscription')

    USERNAME_FIELD = 'pseudo'
    REQUIRED_FIELDS = ['mot_de_passe', 'pseudo', 'email']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        db_table = "Utilisateur"