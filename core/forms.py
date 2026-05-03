from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError


User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Email',
        'autocomplete': 'email',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Senha',
        'autocomplete': 'current-password',
    }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'auth-check-input',
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            usuario = User.objects.filter(email__iexact=email).first()
            username = usuario.username if usuario else email
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Email ou senha inválidos.')
            if not user.is_active:
                raise forms.ValidationError('Usuário inativo.')
            cleaned_data['user'] = user

        return cleaned_data


class CadastroUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Senha',
        'autocomplete': 'new-password',
    }))
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Confirmar senha',
        'autocomplete': 'new-password',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'auth-input', 'placeholder': 'Email', 'autocomplete': 'email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(username__iexact=email).exists() or User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Já existe um usuário cadastrado com este email.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('As senhas precisam ser iguais.')

        if password1:
            validate_password(password1)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class EsqueciSenhaForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Email cadastrado',
        'autocomplete': 'email',
    }))

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Email nao cadastrado.')
        return email


class RedefinirSenhaForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Nova senha', widget=forms.PasswordInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Nova senha',
        'autocomplete': 'new-password',
    }))
    new_password2 = forms.CharField(label='Confirmar nova senha', widget=forms.PasswordInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Confirmar nova senha',
        'autocomplete': 'new-password',
    }))
