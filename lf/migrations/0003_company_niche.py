# Generated by Django 4.2.6 on 2023-10-19 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lf', '0002_niche'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='niche',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lf.niche'),
            preserve_default=False,
        ),
    ]
