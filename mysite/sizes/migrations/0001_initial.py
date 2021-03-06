# Generated by Django 3.0.5 on 2020-06-20 09:28

from django.db import migrations, models
import django_enumfield.db.fields
import sizes.model_enums


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', django_enumfield.db.fields.EnumField(enum=sizes.model_enums.SizeOptions)),
                ('size_type', django_enumfield.db.fields.EnumField(enum=sizes.model_enums.SizeTypes)),
                ('gender', django_enumfield.db.fields.EnumField(enum=sizes.model_enums.GenderOptions)),
            ],
        ),
    ]
