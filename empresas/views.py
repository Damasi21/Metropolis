from django.shortcuts import render, redirect
from .forms import EmpresaForm
from .models import Empresa

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