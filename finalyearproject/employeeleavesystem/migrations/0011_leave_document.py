# Generated by Django 4.2.4 on 2024-06-16 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeleavesystem', '0010_alter_employee_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='leave_documents/'),
        ),
    ]
