# Generated by Django 2.2 on 2020-06-14 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0015_auto_20200614_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='month',
        ),
    ]