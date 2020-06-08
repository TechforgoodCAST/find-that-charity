# Generated by Django 3.0.6 on 2020-06-05 10:29

from django.db import migrations, models

from dbview.helpers import CreateView


class Migration(migrations.Migration):

    dependencies = [
        ('ftc', '0006_auto_20200601_2109'),
    ]

    operations = [
        CreateView(
            name='LinkedOrganisation',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('org_id_a', models.CharField(max_length=255)),
                ('org_id_b', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
