# Generated by Django 3.1 on 2020-09-11 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0028_auto_20200911_1213'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='itemsubcategory',
            name='unique_subcategory',
        ),
        migrations.AddConstraint(
            model_name='itemsubcategory',
            constraint=models.UniqueConstraint(fields=('name', 'parent'), name='items_unique_subcategory'),
        ),
    ]
