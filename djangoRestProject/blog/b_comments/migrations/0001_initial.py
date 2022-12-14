# Generated by Django 4.1.4 on 2022-12-28 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('b_posts', '0001_initial'),
        ('b_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='B_comment',
            fields=[
                ('comment_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent_id', models.CharField(max_length=20, null=True)),
                ('b_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='b_posts.b_post')),
                ('b_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='b_users.b_user')),
            ],
            options={
                'db_table': 'blog_comments',
            },
        ),
    ]
