# Generated by Django 4.2.7 on 2023-11-19 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('echoApp', '0020_vacancy_is_publish'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vacancy',
            old_name='celery',
            new_name='salary',
        ),
    ]
