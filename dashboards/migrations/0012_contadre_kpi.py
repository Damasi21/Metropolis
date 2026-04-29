from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0011_clientefornecedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='contadre',
            name='kpi',
            field=models.BooleanField(default=False, verbose_name='KPI'),
        ),
    ]
