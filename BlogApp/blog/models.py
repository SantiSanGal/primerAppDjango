from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

#Creando un objeto  encargado de gestionar el acceso a los datos de los post con estado público
class PublishedManager(models.Manager):
    #sobreescribe el método de models.Manager
    def get_queryset(self):
        # trae los modelos del obj Post, entonces hay que filtrarlos según published
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    #Definir opciones para status
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    #TIPOS DE DATOS
    #Cadena de caracteres, que tiene el máximo especificado.
    title = models.CharField(max_length=250)

    #También cadena de caracteres, pero sólo admite alfanuméricos y guiones, nada de tildes, ñ, etc.
    slug = models.SlugField(max_length=250)

    #Cadena de texto de longitud variable, no requiere indicador de máximo.
    body = models.TextField()

    #toma el manager
    #No crea nada en la bd
    objects = models.Manager()
    published = PublishedManager()


    #Guarda la fecha y hora según la hora en la zona horaria configurada en el settings
    publish = models.DateTimeField(auto_now_add=True)

    #Guarda la fecha en el momento en que se agrega
    created = models.DateTimeField(auto_now_add=True)

    #Guarda la fecha en el momento en que se edita
    updated = models.DateTimeField(auto_now=True)

    #Asignar opciones para status en la clase Status
    #max_length = 2 porque sólo se agrega la inicial definida en la clas Status
    status = models.CharField(choices=Status.choices, default=Status.DRAFT, max_length=2)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", default=1)

    def __str__(self):
        return self.title

    #se ordena según la fecha de publish
    class Meta:
        ordering = ["-publish"]