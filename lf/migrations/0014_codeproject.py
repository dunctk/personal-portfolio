# Generated by Django 4.2.6 on 2024-01-06 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lf', '0013_company_pitch_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('live_url', models.URLField(blank=True, null=True)),
                ('screenshot_url', models.URLField(blank=True, null=True)),
                ('github_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]