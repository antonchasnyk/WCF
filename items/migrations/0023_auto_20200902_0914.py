# Generated by Django 3.1 on 2020-09-02 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0022_auto_20200901_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bom',
            name='assembly_part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consist_of', to='items.item'),
        ),
        migrations.AlterField(
            model_name='bom',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='used_in', to='items.item'),
        ),
    ]
