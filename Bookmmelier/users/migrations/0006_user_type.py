# Generated by Django 4.0.6 on 2022-08-25 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
