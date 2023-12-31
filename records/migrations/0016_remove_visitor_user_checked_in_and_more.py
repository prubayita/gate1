# Generated by Django 4.2.2 on 2023-08-06 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0015_remove_waitinglist_user_requested_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitor',
            name='user_checked_in',
        ),
        migrations.RemoveField(
            model_name='visitor',
            name='user_saved',
        ),
        migrations.AddField(
            model_name='visitor',
            name='devices',
            field=models.TextField(default='No devices'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='visitor',
            name='purpose',
            field=models.CharField(default='Client', max_length=200),
        ),
        migrations.AddField(
            model_name='visitor',
            name='reason_for_decline',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='country_of_origin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='organization',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='position',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
