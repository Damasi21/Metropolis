from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0014_departamentoomie_empresaomie_projetoomie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicadorconfiguracao',
            name='conta_3',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='indicador_como_conta_3',
                to='dashboards.contadre',
                verbose_name='Conta 3',
            ),
        ),
    ]
