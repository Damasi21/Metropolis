from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0012_contadre_kpi'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicadorConfiguracao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chave', models.CharField(choices=[('receita_bruta', 'Receita Bruta'), ('deducoes_gastos_variaveis', 'Deducoes e Gastos Variaveis'), ('margem_contribuicao', 'Margem de Contribuicao'), ('gastos_fixos', 'Gastos Fixos'), ('ebit', 'EBIT')], max_length=50, verbose_name='Indicador')),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('conta_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='indicador_como_conta_1', to='dashboards.contadre', verbose_name='Conta 1')),
                ('conta_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='indicador_como_conta_2', to='dashboards.contadre', verbose_name='Conta 2')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicadores_configurados', to='dashboards.parametroempresa', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Configuracao de Indicador',
                'verbose_name_plural': 'Configuracoes de Indicadores',
            },
        ),
        migrations.AddConstraint(
            model_name='indicadorconfiguracao',
            constraint=models.UniqueConstraint(fields=('empresa', 'chave'), name='uniq_indicador_config_empresa_chave'),
        ),
    ]
