from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Eventos(models.Model):
    
    nombreEvento = models.CharField(max_length=100)
    descripcion = models.TextField(blank=False)
    ubicacion = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f'{self.nombreEvento} - {self.usuario.username}'
    
class Inscripciones(models.Model):
    
    idEvento = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fechaInscripcion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.idEvento.nombreEvento} - {self.usuario.username}'