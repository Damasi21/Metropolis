from django.test import TestCase
from django.urls import reverse

from dashboards.models import ParametroEmpresa
from .models import Empresa


class ConfiguracoesEmpresasTests(TestCase):
    def test_cadastro_empresa_cria_parametros_do_dashboard(self):
        response = self.client.post(
            reverse('configuracoes_empresas'),
            {
                'nome': 'Empresa Nova',
                'slug': 'empresa-nova',
                'ativo': 'on',
            },
        )

        self.assertRedirects(response, reverse('configuracoes_empresas'))
        self.assertTrue(Empresa.objects.filter(slug='empresa-nova').exists())
        self.assertTrue(
            ParametroEmpresa.objects.filter(
                slug_empresa='empresa-nova',
                nome_empresa='Empresa Nova',
            ).exists()
        )
