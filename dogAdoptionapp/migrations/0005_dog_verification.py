# Generated by Django 4.2.5 on 2025-02-05 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogAdoptionapp', '0004_adoptionrequest_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='verification',
            field=models.BooleanField(default=False),
        ),
    ]
