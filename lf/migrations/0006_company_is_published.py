# Generated by Django 4.2.6 on 2023-10-20 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lf', '0005_company_domain_pages_data_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
