# Generated by Django 2.1.4 on 2018-12-26 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_bookinstance_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name']},
        ),
    ]
