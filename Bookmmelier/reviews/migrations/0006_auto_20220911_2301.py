# Generated by Django 2.1.5 on 2022-09-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220911_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='contents',
            field=models.TextField(),
        ),
    ]
