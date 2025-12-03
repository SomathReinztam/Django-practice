### Paso 1. Crear el proyecto de Django

En la raiz de la carpeta ejecutar
```
django-admin startproject mysite
```
Esto creará el proyecto de Django:

```
mysite/
    __init__.py
    settings.py
    urls.py
    asgi.py
    wsgi.py
manage.py
```

### Paso 2. Hacer migración inicial
En consola
```
cd mysite
python manage.py migrate
```


### Paso 3. Crear una app

En la misma consola anterior:

```
python manage.py startapp blog
```

Esto crea la aplicacion blog en django

### Paso 4. modelo Post

En `mysite/blog/models.py` creamos nuestro primer modelo `Post`

```python
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

# Esta cosa de alguna forma crea alguna base de datos con columnas title, slug y body ...
class Post(models.Model):
    # Estados DRAFT o PUBLISHED
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    # Meta informacion de la db, le estamos diciendo a Django que el orden de la tabla esta ordenado  decreciente por publish
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title
```
### Paso 5. Activar aplicacion blog

Vamos al archivo `mysite/mysite/settings.py` y en la lista `INSTALLED_APPS` agregamos `'blog.apps.BlogConfig'` y Ahora django sabe que la aplicación está activa

### Paso 6. Creando y aplicando migración y creando ssupersuser

Se creará la correspondiente base de datos del modelo:

> Now that we have a data model for blog posts, we need to create the corresponding database table. Django comes with a migration system that tracks the changes made to models and enables them to propagate into the database.

> The migrate command applies migrations for all applications listed in INSTALLED_APPS. It synchronizes the database with the current models and existing migrations.

> First, we will need to create an initial migration for our Post model.

Ejecutar el siguiente comando

```
python manage.py makemigrations blog
```

El siguiente comando aplica la migración existente

```
python manage.py migrate
```

Crear superuser:

```
python manage.py createsuperuser
```

Y ponesmos usuario admin, email, y alguna contraseña
```
Username (leave blank to use 'admin'): admin
Email address: admin@admin.com
Password: ********
Password (again): ********
```

Esto permitirá acceder a http://127.0.0.1:8000/admin/ para administrar los posts.

### Paso 7. Registrar modelo en el admin

Crear `blog/admin.py`:

```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
```

### Paso 8. Crear una view para mostrar la lista de posts

En el archivo `blog/views.py` agregar:

```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    return render(request, "blog/post_list.html", {"posts": posts})
```

Explicación:

* Obtenemos todos los posts publicados: `Post.Status.PUBLISHED`
* Renderizamos el template `blog/post_list.html`
* Enviamos la lista de posts como un diccionario `{"posts": posts}`


### Paso 9. Crear un template

Crear la carpeta templates/ en blog/
```
mysite/
    blog/
        templates/
            blog/
                post_list.html
```

El archivo debe llamarse post_list.html:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog</title>
</head>
<body>
    <h1>Mis Posts</h1>

    {% for post in posts %}
        <h2>{{ post.title }}</h2>
        <p>{{ post.publish }}</p>
        <p>{{ post.body|truncatewords:30 }}</p>
        <hr>
    {% empty %}
        <p>No hay posts disponibles.</p>
    {% endfor %}
</body>
</html>
```

### Paso 10. Crear las URLs del blog

Dentro de la app blog, crear un archivo **blog/urls.py**:

```
mysite/blog/urls.py
```

Contenido:

```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.post_list, name="post_list"),
]
```

---

### Paso 11. Incluir las URLs del blog en el proyecto

Editar `mysite/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
]
```

Ahora cuando se visite

```
http://127.0.0.1:8000/blog/
```

verás la lista de posts.


### Paso 12. Ejecutar el servidor

```
python manage.py runserver
```

### Requirements.txt

```
asgiref~=3.8
Django~=5.2
sqlparse==0.5.0
```