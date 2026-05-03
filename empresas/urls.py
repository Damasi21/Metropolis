from django.urls import path
from .views import configuracoes_empresas, excluir_usuario_empresa, usuarios_empresa

urlpatterns = [
    path('configuracoes/', configuracoes_empresas, name='configuracoes_empresas'),
    path('usuarios/', usuarios_empresa, name='usuarios_empresa'),
    path('usuarios/<int:usuario_id>/editar/', usuarios_empresa, name='editar_usuario_empresa'),
    path('usuarios/<int:usuario_id>/excluir/', excluir_usuario_empresa, name='excluir_usuario_empresa'),
]
