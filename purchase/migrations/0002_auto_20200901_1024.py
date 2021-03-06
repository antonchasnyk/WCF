# Generated by Django 3.1 on 2020-09-01 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0017_auto_20200901_1024'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemprice',
            name='created_by',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ItemValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0, verbose_name='Value')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='value', to='items.item')),
            ],
        ),
    ]
