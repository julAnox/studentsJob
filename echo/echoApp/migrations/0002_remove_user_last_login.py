# Generated by Django 4.2.6 on 2023-10-28 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('echoApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
    ]
