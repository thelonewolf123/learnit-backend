# Generated by Django 3.1 on 2020-08-25 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogx', '0003_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='uid',
            field=models.CharField(default='nothing', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]