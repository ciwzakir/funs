# Generated by Django 3.2.6 on 2022-08-12 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('altandexp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='add_allotment',
        ),
    ]
