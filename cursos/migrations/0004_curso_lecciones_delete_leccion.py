# Generated by Django 4.2.4 on 2023-08-09 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_alter_curso_persons_alter_curso_taste_leccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='lecciones',
            field=models.JSONField(default=list),
        ),
        migrations.DeleteModel(
            name='Leccion',
        ),
    ]