# Generated by Django 4.2.2 on 2024-01-08 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0018_alter_firmware_firmware_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmware',
            name='firmware_version_file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]