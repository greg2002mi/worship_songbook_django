# Generated by Django 4.2.3 on 2023-07-06 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songbook', '0005_remove_song_user_listitem_slug_lists_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='info',
            field=models.TextField(max_length=140),
        ),
    ]
