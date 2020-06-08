# Generated by Django 3.0.6 on 2020-05-30 23:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ftc', '0003_organisationlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationlink',
            name='source',
            field=models.ForeignKey(default='rsl', on_delete=django.db.models.deletion.CASCADE, to='ftc.Source'),
            preserve_default=False,
        ),
    ]
