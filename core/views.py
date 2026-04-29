from django.shortcuts import render
from empresas.models import Empresa

def home(request):
    empresas = Empresa.objects.filter(ativo=True).order_by('nome')
    return render(request, 'home.html', {'empresas': empresas})