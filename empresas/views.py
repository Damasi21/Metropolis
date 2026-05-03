from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from .forms import EmpresaForm
from .models import Empresa
from .user_forms import UsuarioEmpresaForm


User = get_user_model()

def configuracoes_empresas(request):
    form = EmpresaForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('configuracoes_empresas')

    empresas = Empresa.objects.all().order_by('nome')

    return render(request, 'configuracoes_empresas.html', {
        'form': form,
        'empresas': empresas
    })


def usuarios_empresa(request, usuario_id=None):
    usuario = get_object_or_404(User, pk=usuario_id) if usuario_id else None
    form = UsuarioEmpresaForm(request.POST or None, instance=usuario)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuário salvo com sucesso.')
        return redirect('usuarios_empresa')

    usuarios = User.objects.all().order_by('first_name', 'last_name', 'email')

    return render(request, 'usuarios.html', {
        'form': form,
        'usuarios': usuarios,
        'usuario_editando': usuario,
    })


def excluir_usuario_empresa(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)

    if request.method == 'POST':
        if request.user.is_authenticated and request.user.pk == usuario.pk:
            messages.error(request, 'Você não pode excluir o usuário conectado.')
        else:
            usuario.delete()
            messages.success(request, 'Usuário excluído com sucesso.')

    return redirect('usuarios_empresa')
