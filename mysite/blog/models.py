from django.db import models
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)

    # ForeignKey: Relación "Muchos a Uno". Un usuario puede escribir muchos posts.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, # Si borras al usuario, se borran sus posts
        related_name='blog_posts' # Permite acceder a los posts desde el usuario (user.blog_posts.all())
    )
    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) # Se guarda solo al crear
    updated = models.DateTimeField(auto_now=True)     # Se actualiza cada vez que guardas
    
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    # Metadatos: no son campos, sino instrucciones para Django
    class Meta:
        ordering = ['-publish'] # El guion '-' significa orden descendente (más nuevo primero)
        indexes = [
            models.Index(fields=['-publish']), # Mejora la velocidad de búsqueda por fecha
        ]

    def __str__(self):
        return self.title # Muestra el título en el panel de admin en lugar de "Post object (1)"
    


