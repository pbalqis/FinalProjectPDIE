# Generated by Django 4.2.4 on 2024-06-03 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeleavesystem', '0004_leave'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='status',
            field=models.CharField(default='Pending', max_length=10),
        ),
    ]