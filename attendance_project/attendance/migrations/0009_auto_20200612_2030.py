# Generated by Django 2.2 on 2020-06-12 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_auto_20200612_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='duration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='out_time',
            field=models.TimeField(blank=True, default='19:00:00', null=True),
        ),
    ]
