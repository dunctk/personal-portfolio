# Generated by Django 4.2.6 on 2023-11-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lf', '0012_marketingcategory_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='pitch_video',
            field=models.URLField(blank=True, null=True),
        ),
    ]
