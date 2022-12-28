# Generated by Django 4.1.4 on 2022-12-28 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='M_cinema',
            fields=[
                ('cinema_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('image_url', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('detail_address', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'movie_cinemas',
            },
        ),
    ]