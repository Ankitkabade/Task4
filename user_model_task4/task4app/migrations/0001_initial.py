# Generated by Django 5.0.2 on 2024-03-06 09:09

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
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('task_name', models.CharField(max_length=40)),
                ('task_discriptions', models.TextField()),
                ('task_status', models.CharField(choices=[('pending', 'pending'), ('completed', 'completed'), ('in_progress', 'in_progress')], max_length=45)),
                ('task_assigned_date', models.DateTimeField(auto_now_add=True)),
                ('task_completed_date', models.DateTimeField(blank=True, null=True)),
                ('task_deadline', models.DateTimeField(blank=True, null=True)),
                ('task_assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_task', to=settings.AUTH_USER_MODEL)),
                ('task_assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]