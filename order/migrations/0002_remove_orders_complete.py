# Generated by Django 3.1.2 on 2020-11-16 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='complete',
        ),
    ]
