# Generated by Django 3.0.5 on 2020-06-02 07:21

from django.db import migrations
import django_enumfield.db.fields
import sizes.model_enums


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200602_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender_preference',
            field=django_enumfield.db.fields.EnumField(blank=True, enum=sizes.model_enums.GenderOptions, null=True),
        ),
    ]
