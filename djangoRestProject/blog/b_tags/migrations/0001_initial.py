# Generated by Django 4.1.4 on 2022-12-28 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('b_posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='B_tag',
            fields=[
                ('tag_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('b_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='b_posts.b_post')),
            ],
            options={
                'db_table': 'blog_tags',
            },
        ),
    ]
