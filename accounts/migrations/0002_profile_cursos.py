# Generated by Django 4.2.2 on 2023-07-06 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0002_curso_students'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cursos',
            field=models.ManyToManyField(blank=True, related_name='enrolled_students', to='cursos.curso'),
        ),
    ]
