# Generated by Django 4.2.2 on 2023-10-24 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0013_fields_edit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmware',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='firmwareupdatefield',
            name='value',
            field=models.CharField(default='0', max_length=255),
        ),
    ]