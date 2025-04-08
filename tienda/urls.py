from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views


urlpatterns = [
    path('clientes/', views.vista_cliente, name='vista_cliente'),
    path('vendedores/', views.vista_vendedor, name='vista_vendedor'),
    path('', views.index, name="inicio"),
    path('registrar', views.registrar_usuario, name='registrar_usuario'),
    path('entradas/', views.vista_entradas, name='vista_entrada'),
    path('crearentrada/', views.crear_entrada, name='crear_entrada'),
    path('creardiscoteca/', views.crear_discoteca, name='crear_discoteca'),
    path('discotecas/', views.vista_discoteca, name='vista_discoteca'),
    
    #path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),


]
