# Generated by Django 4.0.3 on 2023-09-21 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_categories_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='available_copies',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
