from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views


urlpatterns = [
    path('clientes/', views.vista_cliente, name='vista_cliente'),
    path('vendedores/', views.vista_vendedor, name='vista_vendedor'),
    path('', views.index, name="inicio"),
    path('registrar', views.registrar_usuario, name='registrar_usuario'),
    
    #path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),


]
