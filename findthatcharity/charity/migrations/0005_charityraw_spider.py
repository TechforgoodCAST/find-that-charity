# Generated by Django 3.0.6 on 2020-06-04 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0004_auto_20200604_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='charityraw',
            name='spider',
            field=models.CharField(db_index=True, default='ccew', max_length=200),
            preserve_default=False,
        ),
    ]
