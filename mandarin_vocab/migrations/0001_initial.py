# Generated by Django 5.2 on 2025-05-01 04:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserVocabulary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_learned', models.BooleanField(default=False)),
                ('last_reviewed', models.DateTimeField(blank=True, null=True)),
                ('review_count', models.IntegerField(default=0)),
                ('next_review', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'User Vocabulary',
                'verbose_name_plural': 'User Vocabularies',
            },
        ),
        migrations.CreateModel(
            name='VocabularyWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chinese', models.CharField(max_length=50)),
                ('pinyin', models.CharField(max_length=100)),
                ('english', models.CharField(max_length=200)),
                ('hsk_level', models.IntegerField(choices=[(1, 'HSK1'), (2, 'HSK2'), (3, 'HSK3'), (4, 'HSK4'), (5, 'HSK5'), (6, 'HSK6')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)])),
                ('stroke_order_gif', models.FileField(blank=True, null=True, upload_to='stroke_orders/')),
                ('audio', models.FileField(blank=True, null=True, upload_to='word_audio/')),
                ('example_sentence', models.TextField(blank=True)),
                ('example_pinyin', models.TextField(blank=True)),
                ('example_translation', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Vocabulary Word',
                'verbose_name_plural': 'Vocabulary Words',
                'ordering': ['hsk_level', 'chinese'],
            },
        ),
        migrations.CreateModel(
            name='HSKBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('hsk_level', models.IntegerField(choices=[(1, 'HSK1'), (2, 'HSK2'), (3, 'HSK3'), (4, 'HSK4'), (5, 'HSK5'), (6, 'HSK6')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)])),
                ('book_type', models.CharField(choices=[('TB', 'Textbook'), ('TBA', 'Textbook A'), ('TBB', 'Textbook B'), ('WB', 'Workbook')], max_length=3)),
                ('file', models.FileField(upload_to='books/')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='book_covers/')),
                ('description', models.TextField(blank=True)),
                ('page_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'HSK Book',
                'verbose_name_plural': 'HSK Books',
                'ordering': ['hsk_level', 'book_type'],
                'unique_together': {('hsk_level', 'book_type')},
            },
        ),
    ]
