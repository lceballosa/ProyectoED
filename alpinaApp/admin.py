from django.contrib import admin
from alpinaApp.models import usuarios


class usuarios_(admin.ModelAdmin):
    list_display=("nombre","correo", "contrase")

admin.site.register(usuarios,usuarios_)

# Register your models here.
