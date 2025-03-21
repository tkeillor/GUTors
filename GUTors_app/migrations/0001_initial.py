# Generated by Django 5.1.7 on 2025-03-16 19:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TutoringSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GUTors_app.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(default=5)),
                ('comment', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('session', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='GUTors_app.tutoringsession')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('STUDENT', 'Student'), ('TUTOR', 'Tutor')], default='STUDENT', max_length=7)),
                ('bio', models.TextField(blank=True)),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('subjects', models.ManyToManyField(blank=True, to='GUTors_app.subject')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tutoringsession',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tutoring_session_as_student', to='GUTors_app.userprofile'),
        ),
        migrations.AddField(
            model_name='tutoringsession',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutoring_session_as_tutor', to='GUTors_app.userprofile'),
        ),
    ]
