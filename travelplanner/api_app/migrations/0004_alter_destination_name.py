# Generated by Django 5.1.4 on 2025-01-10 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0003_alter_destination_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
