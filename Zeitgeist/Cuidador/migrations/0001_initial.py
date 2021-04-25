# Generated by Django 3.1.7 on 2021-04-19 06:53

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
            name='Cat_Pregunta',
            fields=[
                ('idReactivo', models.IntegerField(primary_key=True, serialize=False)),
                ('reactivo', models.TextField()),
                ('tipoDato', models.CharField(choices=[('TXT', 'Texto'), ('IMG', 'Imagen'), ('AUD', 'Audio')], max_length=50)),
                ('tipoPregunta', models.CharField(choices=[('A', 'Abierta'), ('OP', 'Opcion Multiple')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Cuidador',
            fields=[
                ('nomUsuario', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=70)),
                ('contrasena', models.CharField(max_length=45)),
                ('correo', models.EmailField(max_length=254)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cuidadores', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='reminiscencia')),
                ('audio', models.FileField(blank=True, null=True, upload_to='reminiscencia')),
                ('respuestaCuidador', models.CharField(max_length=255)),
                ('idCuidador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cuidador.cuidador')),
                ('idReactivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cuidador.cat_pregunta')),
            ],
        ),
    ]
