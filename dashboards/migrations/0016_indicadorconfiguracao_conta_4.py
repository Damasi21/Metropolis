from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0015_indicadorconfiguracao_conta_3'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicadorconfiguracao',
            name='conta_4',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='indicador_como_conta_4',
                to='dashboards.contadre',
                verbose_name='Conta 4',
            ),
        ),
    ]
