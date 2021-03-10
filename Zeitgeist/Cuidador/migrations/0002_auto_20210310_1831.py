# Generated by Django 3.1.3 on 2021-03-10 18:31

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Cuidador', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuidador',
            name='contraseña',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=45)),
        ),
    ]
