# Generated by Django 2.1.4 on 2018-12-26 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20181226_1452'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['author']},
        ),
    ]
