# Generated by Django 3.1 on 2020-08-19 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogx', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='subject',
        ),
    ]