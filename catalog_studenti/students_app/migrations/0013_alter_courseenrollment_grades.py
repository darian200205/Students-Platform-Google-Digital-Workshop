# Generated by Django 3.2.9 on 2021-12-11 16:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_app', '0012_alter_courseenrollment_grades'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseenrollment',
            name='grades',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.int_list_validator]),
        ),
    ]