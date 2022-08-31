# Generated by Django 3.2.6 on 2022-08-13 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altandexp', '0002_remove_category_add_allotment'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='total_allotments_is',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Total of Allotments'),
        ),
    ]
