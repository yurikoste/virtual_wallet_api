# Generated by Django 3.2.9 on 2021-11-17 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_wallet_last_used_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='last_used_currency',
        ),
    ]
