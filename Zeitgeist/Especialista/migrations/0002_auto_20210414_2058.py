# Generated by Django 3.1.3 on 2021-04-14 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Especialista', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='especialista',
            old_name='contraseña',
            new_name='contrasena',
        ),
    ]
