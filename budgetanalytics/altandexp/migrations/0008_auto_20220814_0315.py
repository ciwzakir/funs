# Generated by Django 3.2.6 on 2022-08-13 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altandexp', '0007_auto_20220814_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='proggress_of_allotments',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Progressive Allotment'),
        ),
        migrations.AddField(
            model_name='category',
            name='proggress_of_expenses',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Progressive Allotment'),
        ),
    ]