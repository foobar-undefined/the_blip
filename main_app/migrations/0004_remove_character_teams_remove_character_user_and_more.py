# Generated by Django 4.2.2 on 2023-06-09 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_character_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='teams',
        ),
        migrations.RemoveField(
            model_name='character',
            name='user',
        ),
        migrations.AddField(
            model_name='team',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
