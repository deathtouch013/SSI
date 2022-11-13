# Generated by Django 3.2.16 on 2022-11-13 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0006_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='user_hash_id',
            field=models.CharField(default=-1, max_length=64),
            preserve_default=False,
        ),
    ]
