from django.db import migrations


def criar_parametros_para_empresas(apps, schema_editor):
    Empresa = apps.get_model('empresas', 'Empresa')
    ParametroEmpresa = apps.get_model('dashboards', 'ParametroEmpresa')

    for empresa in Empresa.objects.all():
        ParametroEmpresa.objects.update_or_create(
            slug_empresa=empresa.slug,
            defaults={'nome_empresa': empresa.nome},
        )


def remover_parametros_criados(apps, schema_editor):
    Empresa = apps.get_model('empresas', 'Empresa')
    ParametroEmpresa = apps.get_model('dashboards', 'ParametroEmpresa')

    slugs = Empresa.objects.values_list('slug', flat=True)
    ParametroEmpresa.objects.filter(slug_empresa__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0017_dreprojetado_and_more'),
        ('empresas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_parametros_para_empresas, remover_parametros_criados),
    ]
