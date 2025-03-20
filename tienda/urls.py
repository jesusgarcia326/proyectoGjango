from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.vista_cliente, name='vista_cliente'),
    path('', views.index, name="inicio"),
]
