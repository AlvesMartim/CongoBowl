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

    USERNAME_FIELD = 'pseudo'
    REQUIRED_FIELDS = ['mot_de_passe', 'pseudo', 'email']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        db_table = "Utilisateur"

class Article(models.Model):
    STATUS_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(verbose_name="Contenu")
    image = models.ImageField(upload_to='articles/', null=True, blank=True, verbose_name="Image")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name="Auteur"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='brouillon',
        verbose_name="Statut"
    )
    categories = models.ManyToManyField(
        'Category',
        related_name='articles',
        blank=True,
        verbose_name="Catégories"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])
