# Generated by Django 2.1.5 on 2022-09-15 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220915_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='book',
            field=models.ForeignKey(db_column='isbn13', on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviews', to='books.Book'),
        ),
    ]
