# Generated by Django 3.1 on 2020-08-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0010_bom_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Comment'),
        ),
    ]
