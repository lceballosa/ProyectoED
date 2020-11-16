from django.urls import path
from alpinaApp import views
urlpatterns = [
    path('inicio', views.ingreso, name= "inicio"),
    path('principal/',views.principal, name="principal"),
    path('salida/', views.salida, name="salida"),
    path('informe_produccion/', views.informe_produccion, name="informe_produccion"),
    path('fecha_corta/', views.fecha_corta, name="fecha_corta"),
    path('donaciones/',views.frame_donaciones, name="donaciones"),
    path('historial/', views.historial_, name="historial"),
    #path('ingreso/',views.buscar),
    path('plot/', views.plot),
    #path('', views.inicio, name="home"),
    #path('kk/', views.kk)

]