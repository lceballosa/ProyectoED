# Generated by Django 3.1.2 on 2020-10-23 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usuarios',
            fields=[
                ('correo', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('contrase', models.TextField(max_length=10)),
            ],
        ),
    ]
