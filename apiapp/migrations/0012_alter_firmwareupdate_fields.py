# Generated by Django 4.2.2 on 2023-10-02 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0011_alter_firmwareupdate_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmwareupdate',
            name='fields',
            field=models.ManyToManyField(through='apiapp.FirmwareUpdateField', to='apiapp.fields'),
        ),
    ]