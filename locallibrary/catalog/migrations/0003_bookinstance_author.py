# Generated by Django 2.1.4 on 2018-12-26 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20181225_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Author'),
        ),
    ]
