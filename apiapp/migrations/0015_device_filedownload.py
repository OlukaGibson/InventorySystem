# Generated by Django 4.2.2 on 2023-10-26 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0014_alter_firmware_uploaded_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='fileDownload',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
