# Generated by Django 2.2.12 on 2021-05-26 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Cuidador', '0001_initial'),
        ('Usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ap_Reminiscencia',
            fields=[
                ('cveAcceso', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('fechaAp', models.DateField()),
                ('resultadoFinal', models.IntegerField(null=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Ap_Screening',
            fields=[
                ('cveAcceso', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('fechaAp', models.DateField()),
                ('resultadoFinal', models.IntegerField(null=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('cveTemas', models.IntegerField(primary_key=True, serialize=False)),
                ('tema', models.CharField(max_length=20)),
                ('dificultad', models.CharField(choices=[('F', 'Facil'), ('M', 'Medio'), ('D', 'Dificil')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('idApp', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('idReactivo', models.IntegerField()),
                ('respuestaT', models.CharField(max_length=255, null=True)),
                ('respuestaImg', models.ImageField(blank=True, null=True, upload_to='screening')),
                ('puntajeReactivo', models.IntegerField()),
                ('puntajeMaximo', models.IntegerField()),
                ('cveAcceso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Paciente.Ap_Screening')),
            ],
        ),
        migrations.CreateModel(
            name='Reminiscencia',
            fields=[
                ('idApp', models.CharField(max_length=17, primary_key=True, serialize=False)),
                ('respuestaPaciente', models.CharField(max_length=255)),
                ('valoracion', models.BooleanField()),
                ('cveAcceso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='idRem', to='Paciente.Ap_Reminiscencia')),
                ('idPregunta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idRem', to='Cuidador.Pregunta')),
            ],
        ),
        migrations.CreateModel(
            name='Palabra',
            fields=[
                ('idPalabra', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('cvePalabra', models.IntegerField()),
                ('palabra', models.CharField(max_length=10)),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Paciente.Tema')),
            ],
        ),
        migrations.CreateModel(
            name='Ent_Cogn',
            fields=[
                ('cveAcceso', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('fechaAp', models.DateField()),
                ('estado', models.CharField(choices=[('S', 'Superado'), ('NS', 'No superado')], max_length=50)),
                ('tiempo', models.TimeField(null=True)),
                ('cveTema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Paciente.Tema')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.Paciente')),
            ],
        ),
    ]
