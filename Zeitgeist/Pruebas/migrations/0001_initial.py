# Generated by Django 3.1.7 on 2021-04-19 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Especialista', '0001_initial'),
        ('Cuidador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('cveTemas', models.IntegerField(primary_key=True, serialize=False)),
                ('tema', models.CharField(max_length=20)),
                ('dificultad', models.CharField(choices=[('F', 'Facil'), ('M', 'Medio'), ('D', 'Dificil')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('nomUsuario', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=70)),
                ('contrasena', models.CharField(max_length=50)),
                ('correo', models.EmailField(blank=True, max_length=254)),
                ('escolaridad', models.CharField(choices=[('N', 'Ninguna'), ('PR', 'Primaria'), ('SC', 'Secundaria'), ('BCH', 'Bachillerato'), ('SUP', 'Licenciatura o superior')], max_length=50)),
                ('fechaNac', models.DateField()),
                ('sexo', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=50)),
                ('fechaIng', models.DateField()),
                ('fechaDiag', models.DateField()),
                ('cuidador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Cuidador.cuidador')),
                ('especialista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Especialista.especialista')),
            ],
        ),
        migrations.CreateModel(
            name='Ent_Cogn',
            fields=[
                ('cveAcceso', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('S', 'Superado'), ('NS', 'No superado')], max_length=50)),
                ('cveTema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pruebas.tema')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pruebas.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Ap_Screening',
            fields=[
                ('cveAcceso', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('fechaAp', models.DateField()),
                ('resultadoFinal', models.IntegerField()),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pruebas.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Ap_Reminiscencia',
            fields=[
                ('cveAcceso', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('fechaAp', models.DateField()),
                ('resultadoFinal', models.IntegerField(null=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pruebas.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('idReactivo', models.IntegerField(primary_key=True, serialize=False)),
                ('respuestaT', models.CharField(max_length=255)),
                ('respuestaImg', models.ImageField(upload_to='')),
                ('puntajeReactivo', models.IntegerField()),
                ('puntajeMaximo', models.IntegerField()),
                ('cveAcceso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Pruebas.ap_screening')),
            ],
            options={
                'unique_together': {('cveAcceso', 'idReactivo')},
            },
        ),
        migrations.CreateModel(
            name='Reminiscencia',
            fields=[
                ('idApp', models.CharField(max_length=17, primary_key=True, serialize=False)),
                ('respuestaPaciente', models.CharField(max_length=255)),
                ('valoracion', models.BooleanField()),
                ('cveAcceso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idRem', to='Pruebas.ap_reminiscencia')),
                ('idPregunta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idRem', to='Cuidador.pregunta')),
            ],
            options={
                'unique_together': {('cveAcceso', 'idPregunta')},
            },
        ),
        migrations.CreateModel(
            name='Palabra',
            fields=[
                ('cvePalabra', models.IntegerField(primary_key=True, serialize=False)),
                ('palabra', models.CharField(max_length=10)),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pruebas.tema')),
            ],
            options={
                'unique_together': {('cvePalabra', 'tema')},
            },
        ),
    ]
