# Generated by Django 5.0.1 on 2024-01-30 16:03

import user.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='phone_number',
            field=models.CharField(max_length=13, validators=[user.validator.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='phone_number',
            field=models.CharField(max_length=13, validators=[user.validator.validate_phone_number]),
        ),
    ]
