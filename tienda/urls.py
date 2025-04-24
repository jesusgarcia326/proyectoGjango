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
    path('entrada/<int:pepito>', views.dame_entrada, name='dame_entrada'),
    path('entrada/<int:pepito>/editar', views.editar_entrada, name='editar_entrada'),
    path('discoteca/<int:jaimito>', views.dame_discoteca, name='dame_discoteca'),
    path('discoteca/<int:jaimito>/editar', views.editar_discoteca, name='editar_discoteca'),
    path('entrada/<int:entrada_id>/elimiar', views.eliminar_entrada, name='eliminar_entrada'),
    path('perfil/cliente/<int:id_cliente>/', views.perfil_cliente, name='perfil_cliente'),
    path('perfil/vendedor/<int:id_vendedor>/', views.perfil_vendedor, name='perfil_vendedor'),
    path('banco/crear', views.crear_banco, name='crear_banco'),
    path('banco/<int:banco_id>/editar', views.editar_banco, name='editar_banco'),
    path('banco/<int:banco_id>/eliminar', views.eliminar_banco, name='eliminar_banco'),
    path('datosvendedor/', views.vista_datos_vendedor, name='vista_datos_vendedor'),
    path('datosvendedor/crear', views.crear_datos_vendedor, name='crear_datos_vendedor'),
    path('datosvendedor/<int:datos_id>/editar', views.editar_datos_vendedor, name='editar_datos_vendedor'),
    path('datosvendedor/<int:datos_id>/eliminar', views.eliminar_datos_vendedor, name='eliminar_datos_vendedor'),
    path('crear/inventario', views.crear_inventario, name='crear_inventario'),
    

    
    #path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),


]
