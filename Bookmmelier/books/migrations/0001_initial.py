# Generated by Django 4.0.6 on 2022-08-26 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn13', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('vol', models.CharField(blank=True, max_length=20, null=True)),
                ('title', models.CharField(blank=True, max_length=1200, null=True)),
                ('author', models.CharField(blank=True, max_length=1000, null=True)),
                ('publisher', models.CharField(blank=True, max_length=1000, null=True)),
                ('pub_date', models.CharField(blank=True, max_length=10, null=True)),
                ('img_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('kdc_class_no', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'book',
                'managed': False,
            },
        ),
    ]
