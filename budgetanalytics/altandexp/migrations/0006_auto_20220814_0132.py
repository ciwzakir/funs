# Generated by Django 3.2.6 on 2022-08-13 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altandexp', '0005_auto_20220814_0056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='digits7',
            new_name='seven_digit_code',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='vrsHead',
            new_name='voucher_head',
        ),
        migrations.AddField(
            model_name='category',
            name='is_general_or_spl',
            field=models.BooleanField(default=True),
        ),
    ]