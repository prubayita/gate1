# Generated by Django 4.2.2 on 2023-07-04 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('organization', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('country_of_origin', models.CharField(max_length=255)),
                ('id_passport_nbr', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('mobile_phone', models.CharField(max_length=20)),
                ('date', models.DateField(auto_now_add=True)),
                ('devices', models.CharField(max_length=255)),
                ('time_in', models.DateTimeField(blank=True, null=True)),
                ('time_out', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
