# Generated by Django 3.1.2 on 2020-11-16 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_customers_userimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='userImage',
            field=models.ImageField(blank=True, height_field=140, null=True, upload_to='', width_field=140),
        ),
    ]
