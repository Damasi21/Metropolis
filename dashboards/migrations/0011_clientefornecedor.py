from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0010_composicaocontadre'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteFornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_omie', models.BigIntegerField(unique=True, verbose_name='Codigo do cliente/fornecedor no Omie')),
                ('codigo_integracao', models.CharField(blank=True, max_length=60, null=True, verbose_name='Codigo de integracao')),
                ('razao_social', models.CharField(max_length=120, verbose_name='Razao social')),
                ('nome_fantasia', models.CharField(blank=True, max_length=120, null=True, verbose_name='Nome fantasia')),
                ('cnpj_cpf', models.CharField(blank=True, max_length=20, null=True, verbose_name='CNPJ/CPF')),
                ('data_importacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de importacao')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Cliente/Fornecedor',
                'verbose_name_plural': 'Clientes/Fornecedores',
                'ordering': ['nome_fantasia', 'razao_social', 'codigo_omie'],
            },
        ),
    ]
