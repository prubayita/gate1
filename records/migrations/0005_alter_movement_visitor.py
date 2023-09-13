# Generated by Django 4.2.2 on 2023-07-29 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_waitinglist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement',
            name='visitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='records.visitor'),
        ),
    ]
