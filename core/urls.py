from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import cadastro_usuario, esqueci_senha, home, login_usuario, redefinir_senha

urlpatterns = [
    path('', login_usuario, name='login'),
    path('cadastro/', cadastro_usuario, name='cadastro_usuario'),
    path('esqueci-senha/', esqueci_senha, name='esqueci_senha'),
    path('redefinir-senha/<uidb64>/<token>/', redefinir_senha, name='redefinir_senha'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', home, name='home'),
]
