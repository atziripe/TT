# Generated by Django 3.1.3 on 2021-03-08 06:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Pruebas', '0004_auto_20210308_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminiscencia',
            name='id',
            field=models.AutoField(auto_created=True, default=django.utils.timezone.now, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reminiscencia',
            name='cveAcceso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_rem', to='Pruebas.ap_reminiscencia'),
        ),
    ]
