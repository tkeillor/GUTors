# Generated by Django 2.2.28 on 2025-03-27 17:16

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
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('STUDENT', 'Student'), ('TUTOR', 'Tutor')], default='STUDENT', max_length=7)),
                ('bio', models.TextField(blank=True)),
                ('profile_picture', models.ImageField(blank=True, default='profile_images/avatar.jpg', upload_to='profile_images')),
                ('subjects', models.ManyToManyField(blank=True, to='GUTors_app.Subject')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TutoringSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tutoring_session_as_student', to='GUTors_app.UserProfile')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GUTors_app.Subject')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutoring_session_as_tutor', to='GUTors_app.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('session', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='GUTors_app.TutoringSession')),
            ],
        ),
    ]
