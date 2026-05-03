from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()


class UsuarioEmpresaForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
    }))
    password2 = forms.CharField(label='Confirmar senha', required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = User.objects.filter(email__iexact=email) | User.objects.filter(username__iexact=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError('Já existe um usuário cadastrado com este email.')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if self.instance.pk:
            if password1 or password2:
                if password1 != password2:
                    raise ValidationError('As senhas precisam ser iguais.')
                validate_password(password1, self.instance)
        else:
            if not password1 or not password2:
                raise ValidationError('Informe e confirme a senha do usuário.')
            if password1 != password2:
                raise ValidationError('As senhas precisam ser iguais.')
            validate_password(password1)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user
