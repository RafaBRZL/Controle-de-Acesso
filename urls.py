from django.urls import path
from . import views
#Associa a função views.index a url 'index'
urlpatterns = [
    path('', views.index, name='index'),
    path('listar', views.listar, name='listar'),
    path('chaves/<int:id>/', views.ver_chave, name = 'ver_chave'),
    path('login/', views.fazer_login, name='fazer_login'),
    path('logout/', views.fazer_logout, name='fazer_logout'),
    path('avaliar_codigo/', views.avaliar_codigo, name='avaliar_codigo'),
    path('solicitar_pessoa/<int:id_chave>/', views.solicitar_pessoa, name = 'solicitar_pessoa'),
]