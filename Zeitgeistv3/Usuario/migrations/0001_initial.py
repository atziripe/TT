# Generated by Django 2.2.12 on 2021-05-14 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuidador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cuidadores',
            },
        ),
        migrations.CreateModel(
            name='Especialista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numpacientesActual', models.IntegerField(default=0)),
                ('numPacientes_Max', models.IntegerField()),
                ('datos_generales', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Especialistas',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('escolaridad', models.CharField(choices=[('N', 'Ninguna'), ('PR', 'Primaria'), ('SC', 'Secundaria'), ('BCH', 'Bachillerato'), ('SUP', 'Licenciatura o superior')], max_length=50)),
                ('fechaNac', models.DateField()),
                ('sexo', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=50)),
                ('fechaDiag', models.DateField()),
                ('cuidador', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuario.Cuidador')),
                ('especialista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuario.Especialista')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Pacientes',
            },
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Administradores',
            },
        ),
    ]
