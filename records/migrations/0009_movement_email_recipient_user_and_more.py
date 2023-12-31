# Generated by Django 4.2.2 on 2023-08-02 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0008_alter_movement_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='email_recipient_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='email_recipient_movements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movement',
            name='user_checked_in',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checked_in_movements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movement',
            name='user_checked_out',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checked_out_movements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visitor',
            name='user_checked_in',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checked_in_visitors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visitor',
            name='user_saved',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='saved_visitors', to=settings.AUTH_USER_MODEL),
        ),
    ]
