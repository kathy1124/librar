# Generated by Django 4.2.5 on 2024-01-09 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytext', '0016_alter_post_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='genre',
            field=models.CharField(choices=[('童話', '童話'), ('comic', '漫畫')], max_length=200),
        ),
    ]
