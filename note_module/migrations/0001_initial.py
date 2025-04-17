# Generated by Django 5.1.6 on 2025-04-14 22:32

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
            name='User_Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_importance', models.CharField(choices=[('high', 'high'), ('moderate', 'moderate'), ('low', 'low')], db_index=True, max_length=20, verbose_name='how important is this note')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='when was this note created')),
                ('title', models.CharField(max_length=200, verbose_name='title of note')),
                ('content', models.TextField(db_index=True, verbose_name='main text of this note')),
                ('attached_file', models.FileField(blank=True, null=True, upload_to='', verbose_name='the attached file of this note (optional)')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL, verbose_name='who wrote this note')),
            ],
            options={
                'verbose_name': 'user_note',
                'verbose_name_plural': 'users_notes',
                'db_table': 'notes',
            },
        ),
    ]
