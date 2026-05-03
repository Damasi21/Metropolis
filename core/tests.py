from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


User = get_user_model()


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class RecuperacaoSenhaTestCase(TestCase):
    def test_esqueci_senha_exibe_email_nao_cadastrado(self):
        response = self.client.post(reverse('esqueci_senha'), {'email': 'nada@md21.com.br'})

        self.assertContains(response, 'Email nao cadastrado.')
        self.assertEqual(len(mail.outbox), 0)

    def test_esqueci_senha_envia_email_para_usuario_cadastrado(self):
        User.objects.create_user(
            username='marcelo',
            email='marcelo@md21.com.br',
            password='SenhaSegura123',
        )

        response = self.client.post(reverse('esqueci_senha'), {'email': 'marcelo@md21.com.br'})

        self.assertContains(response, 'Enviamos as instruções')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('marcelo@md21.com.br', mail.outbox[0].to)
        self.assertIn('/redefinir-senha/', mail.outbox[0].body)
