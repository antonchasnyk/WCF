# Generated by Django 3.1 on 2020-09-01 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0018_auto_20200901_1749'),
        ('purchase', '0002_auto_20200901_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemvalue',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_value', to='items.item'),
        ),
    ]