from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from empresas.models import Empresa
from .forms import CadastroUsuarioForm, EsqueciSenhaForm, LoginForm, RedefinirSenhaForm


User = get_user_model()


def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.cleaned_data['user'])
        if not form.cleaned_data.get('remember_me'):
            request.session.set_expiry(0)
        return redirect(request.GET.get('next') or 'home')

    return render(request, 'login.html', {'form': form})


def cadastro_usuario(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CadastroUsuarioForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')

    return render(request, 'cadastro.html', {'form': form})


def esqueci_senha(request):
    form = EsqueciSenhaForm(request.POST or None)
    enviado = False

    if request.method == 'POST' and form.is_valid():
        user = User.objects.filter(email__iexact=form.cleaned_data['email']).first()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        path = reverse('redefinir_senha', kwargs={'uidb64': uid, 'token': token})
        reset_url = request.build_absolute_uri(path)

        send_mail(
            'Redefinição de senha | Metrópolis',
            (
                f'Olá, {user.first_name or user.email}.\n\n'
                'Use o link abaixo para cadastrar uma nova senha no Metrópolis:\n'
                f'{reset_url}\n\n'
                'Se você não solicitou esta alteração, ignore este email.'
            ),
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@metropolis.local'),
            [user.email],
            fail_silently=False,
        )
        enviado = True

    return render(request, 'esqueci_senha.html', {'form': form, 'enviado': enviado})


def redefinir_senha(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise Http404('Link de redefinição inválido.')

    if not default_token_generator.check_token(user, token):
        raise Http404('Link de redefinição inválido ou expirado.')

    form = RedefinirSenhaForm(user, request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')

    return render(request, 'redefinir_senha.html', {'form': form})


def home(request):
    empresas = Empresa.objects.filter(ativo=True).order_by('nome')
    return render(request, 'home.html', {'empresas': empresas})
