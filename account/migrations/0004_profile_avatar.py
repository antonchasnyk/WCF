# Generated by Django 3.1 on 2020-08-30 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200828_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='/static/assets/img/users/default_avatar.png', upload_to='avatars'),
        ),
    ]
