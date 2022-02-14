# Generated by Django 3.2.9 on 2021-12-11 16:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_app', '0011_courseenrollment_date_enrolled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseenrollment',
            name='grades',
            field=models.CharField(blank=True, choices=[('10', '10'), ('9', '9'), ('8', '8'), ('7', '7'), ('6', '6'), ('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')], max_length=30, null=True, validators=[django.core.validators.int_list_validator]),
        ),
    ]