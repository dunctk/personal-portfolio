# Generated by Django 4.2.6 on 2024-01-06 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lf', '0014_codeproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='codeproject',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
