from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, db_column='nom')
    prenom = models.CharField(max_length=100, db_column='prenom')
    pseudo = models.CharField(max_length=100, db_column='pseudo', unique =True)
    email = models.EmailField(unique=True, db_column='mail')
    mot_de_passe = models.CharField(max_length=100, db_column='mot_de_passe')
    date_inscription = models.DateTimeField(auto_now_add=True, db_column='date_inscription')
    droits_admin = models.BooleanField(default=False, db_column='droits_admin')

    USERNAME_FIELD = 'pseudo'
    REQUIRED_FIELDS = ['mot_de_passe', 'pseudo', 'email']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        db_table = "Utilisateur"

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class Article(models.Model):
    Choix_statut = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True)
    contenu = models.TextField(verbose_name="Contenu")
    image = models.ImageField(upload_to='static/images/articles/', null=True, blank=True, verbose_name="Image")
    auteur_id = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name="Auteur"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_upload = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    statut = models.CharField(
        max_length=10,
        choices=Choix_statut,
        default='brouillon',
        verbose_name="Statut"
    )
    categorie_id = models.ManyToManyField(
        Categorie,
        related_name='articles',
        blank=True,
        verbose_name="Catégories"
    )

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        db_table = "Article"

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

class Commande(models.Model):
    STATUS_CHOICES = [
        ('non paye', 'Non payé'),
        ('en livraison', 'En livraison'),
        ('livre', 'Livré')
    ]
    date_achat = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='non paye')

    def __str__(self):
        return f"Commande {self.id} - {self.statut}"

class ArticlesCommandes(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    commande_id = models.ForeignKey(Commande, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Article commandé"
        verbose_name_plural = "Articles commandés"
