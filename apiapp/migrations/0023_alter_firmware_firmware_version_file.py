# Generated by Django 4.2.2 on 2024-01-11 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0022_alter_firmware_firmware_version_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmware',
            name='firmware_version_file',
            field=models.FileField(null=True, upload_to='firmwares/'),
        ),
    ]
