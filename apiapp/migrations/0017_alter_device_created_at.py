# Generated by Django 4.2.2 on 2023-10-27 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0016_remove_firmwareupdate_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
