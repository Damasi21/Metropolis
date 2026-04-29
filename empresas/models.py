from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome