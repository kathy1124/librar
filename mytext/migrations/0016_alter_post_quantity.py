# Generated by Django 4.2.5 on 2024-01-06 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytext', '0015_post_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
