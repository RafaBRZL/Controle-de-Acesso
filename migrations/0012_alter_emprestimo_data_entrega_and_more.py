# Generated by Django 4.2.4 on 2023-12-10 19:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('controleacesso', '0011_chave_portaria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='data_Entrega',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='data_Retirada',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
