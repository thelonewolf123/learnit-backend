# Generated by Django 3.1 on 2020-08-26 11:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('discription', models.TextField(max_length=600)),
                ('profile', models.ImageField(upload_to='learncodex/profile/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='FreeCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('title_img', models.ImageField(upload_to='learnIT/images')),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('tags', models.CharField(max_length=200, unique=True)),
                ('short_disc', models.TextField(max_length=600)),
                ('discription', models.TextField(max_length=10000)),
                ('created_day', models.CharField(max_length=4)),
                ('created_month', models.CharField(max_length=40)),
                ('created_year', models.CharField(max_length=5)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_list', to='learncodex.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='learncodex.category')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='learncodex.freecourse')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=600, null=True)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learncodex.freecourse')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FreeLesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=650, unique=True)),
                ('title', models.CharField(max_length=600)),
                ('dropbox_url', models.CharField(max_length=100)),
                ('discription', models.TextField(max_length=10000)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learncodex.freecourse')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=600)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learncodex.freecourse')),
            ],
        ),
        migrations.CreateModel(
            name='CoursePrerequisite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prerequisite', models.CharField(max_length=600)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learncodex.freecourse')),
            ],
        ),
    ]
