# Generated by Django 3.1 on 2020-08-21 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learncodex', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=600)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learncodex.freecourse')),
            ],
        ),
    ]