# Generated by Django 3.1 on 2020-08-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogx', '0002_auto_20200819_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]