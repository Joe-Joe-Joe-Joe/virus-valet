# Generated by Django 3.2.6 on 2021-08-06 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_message_is_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sent_by_nurse',
            field=models.BooleanField(default=False),
        ),
    ]
