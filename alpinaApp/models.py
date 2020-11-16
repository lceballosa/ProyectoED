from django.db import models

# Create your models here.
class usuarios(models.Model):
    nombre =models.TextField(max_length=20, blank=True, null=True)
    correo = models.EmailField(primary_key=True)
    contrase = models.TextField(max_length=10, verbose_name="contraseña")
class fech_corta(models.Model):
    lote = models.DateField ( blank=True, null=True, verbose_name="lote")
    codigo = models.IntegerField(blank=True, null=False, verbose_name="codigo")
    producto = models.TextField(max_length=20, blank=True, null=False, verbose_name="producto")
    vencimiento = models.DateField ( blank=True, null=True, verbose_name="vencimiento")
    vida = models.IntegerField(blank=True, null=False, verbose_name="vida")
    cantidad = models.FloatField(blank=True, null=False, verbose_name="cantidad")

    def __str__(self):
        resultado= [self.lote, self.codigo]
        return str(resultado)
class donaciones(models.Model):
    lote = models.DateField ( blank=True, null=True, verbose_name="lote")
    codigo = models.IntegerField(blank=True, null=False, verbose_name="codigo")
    producto = models.TextField(max_length=20, blank=True, null=False, verbose_name="producto")
    vida = models.IntegerField(blank=True, null=False, verbose_name="vida")
    cantidad = models.FloatField(blank=True, null=False, verbose_name="cantidad")
