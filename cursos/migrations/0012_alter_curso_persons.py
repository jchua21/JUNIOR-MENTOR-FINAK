# Generated by Django 4.2.4 on 2023-08-10 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0011_alter_curso_persons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='persons',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
