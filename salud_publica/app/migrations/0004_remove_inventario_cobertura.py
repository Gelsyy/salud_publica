# Generated by Django 5.0.6 on 2024-07-17 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_inventario_cobertura_alter_insumo_codigo_cup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='cobertura',
        ),
    ]
