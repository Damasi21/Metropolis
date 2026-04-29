from django import forms
from .models import ContaDRE
from .models import ParametroEmpresa


class ContaDREForm(forms.ModelForm):

    contas_formula = forms.ModelMultipleChoiceField(
        queryset=ContaDRE.objects.filter(ativo=True),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ContaDRE
        fields = ['nome', 'pai', 'sinal', 'ordem', 'kpi', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da conta'
            }),
            'pai': forms.Select(attrs={'class': 'form-select'}),
            'sinal': forms.Select(attrs={'class': 'form-select'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
            'kpi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pai'].queryset = ContaDRE.objects.filter(
            nivel__lt=2,
            ativo=True
        ).order_by('nivel', 'ordem', 'nome')

        self.fields['pai'].required = False
        self.fields['sinal'].required = False

        if self.instance and self.instance.pk:
            self.fields['contas_formula'].queryset = ContaDRE.objects.filter(
                ativo=True
            ).exclude(id=self.instance.id)

#-------------------------------------------------------------------

class ParametroEmpresaForm(forms.ModelForm):
    class Meta:
        model = ParametroEmpresa
        fields = ['app_key_omie', 'app_secret_omie']
        widgets = {
            'app_key_omie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a App Key da Omie'
            }),
            'app_secret_omie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a App Secret da Omie'
            }),
        }
