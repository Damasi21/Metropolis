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

    def test_dashboard_cria_parametros_se_empresa_ja_existir(self):
        Empresa.objects.create(
            nome='Empresa Legada',
            slug='empresa-legada',
            ativo=True,
        )

        response = self.client.get(reverse('dashboard_empresa', kwargs={'slug': 'empresa-legada'}))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ParametroEmpresa.objects.filter(
                slug_empresa='empresa-legada',
                nome_empresa='Empresa Legada',
            ).exists()
        )

    def test_dashboard_exibe_logo_da_empresa_no_menu_lateral(self):
        Empresa.objects.create(
            nome='Empresa com Logo',
            slug='empresa-com-logo',
            logo='logos/empresa-com-logo.png',
            ativo=True,
        )

        response = self.client.get(reverse('dashboard_empresa', kwargs={'slug': 'empresa-com-logo'}))

        self.assertContains(response, 'src="/media/logos/empresa-com-logo.png"')
        self.assertContains(response, 'class="empresa-sidebar-logo"')

    def test_dashboard_exibe_nome_da_empresa_quando_nao_houver_logo(self):
        Empresa.objects.create(
            nome='Empresa sem Logo',
            slug='empresa-sem-logo',
            ativo=True,
        )

        response = self.client.get(reverse('dashboard_empresa', kwargs={'slug': 'empresa-sem-logo'}))

        self.assertContains(response, '<h5 class="fw-bold mb-3">Empresa sem Logo</h5>', html=True)
