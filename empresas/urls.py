from django.urls import path
from .views import configuracoes_empresas

urlpatterns = [
    path('configuracoes/', configuracoes_empresas, name='configuracoes_empresas'),
]