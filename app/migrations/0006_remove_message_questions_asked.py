# Generated by Django 3.2.6 on 2021-08-06 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_message_questions_asked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='questions_asked',
        ),
    ]
