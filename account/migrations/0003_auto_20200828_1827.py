# Generated by Django 3.1 on 2020-08-28 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200827_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=80, verbose_name='Location'),
        ),
    ]
