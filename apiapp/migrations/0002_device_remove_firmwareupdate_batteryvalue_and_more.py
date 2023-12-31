# Generated by Django 4.2.2 on 2023-09-22 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=50)),
                ('channel_id', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='firmwareupdate',
            name='batteryValue',
        ),
        migrations.RemoveField(
            model_name='firmwareupdate',
            name='device_id',
        ),
        migrations.RemoveField(
            model_name='firmwareupdate',
            name='version',
        ),
        migrations.AddField(
            model_name='firmwareupdate',
            name='confrigDownload',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='firmwareupdate',
            name='fileDownload',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='firmwareupdate',
            name='firmware_version',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='firmwareupdate',
            name='firmware_version_file',
            field=models.FileField(default=1, upload_to='firmware/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='firmwareupdate',
            name='syncState',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='FirmwareUpdateHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firmware_version', models.CharField(max_length=20)),
                ('firmware_version_file', models.FileField(upload_to='firmware/')),
                ('fileDownload', models.IntegerField()),
                ('spvValue', models.PositiveIntegerField()),
                ('syncState', models.IntegerField()),
                ('confrigDownload', models.IntegerField()),
                ('uploaded_at', models.DateTimeField()),
                ('history_date', models.DateTimeField(auto_now=True, null=True)),
                ('device_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiapp.device')),
            ],
        ),
        migrations.AddField(
            model_name='firmwareupdate',
            name='device_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apiapp.device'),
            preserve_default=False,
        ),
    ]
