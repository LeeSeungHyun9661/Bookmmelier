# Generated by Django 2.1.5 on 2022-09-13 05:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0006_auto_20220911_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='like_users',
            field=models.ManyToManyField(related_name='like_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
