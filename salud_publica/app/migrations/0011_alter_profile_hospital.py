# Generated by Django 4.2.2 on 2024-10-13 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_profile_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hospital', unique=True),
        ),
    ]
