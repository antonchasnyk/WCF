# Generated by Django 3.1 on 2020-09-07 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0003_auto_20200901_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemvalue',
            name='status',
            field=models.CharField(choices=[('nd', 'Needs'), ('or', 'Ordered'), ('pa', 'Paid'), ('ow', 'On the way'), ('re', 'Received')], default='nd', max_length=2, verbose_name='Status'),
        ),
    ]
