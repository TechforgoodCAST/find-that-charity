# Generated by Django 3.0.6 on 2020-07-31 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charity", "0006_auto_20200705_1626"),
    ]

    operations = [
        migrations.AlterField(
            model_name="charityfinancial",
            name="account_type",
            field=models.CharField(
                choices=[
                    ("basic", "Basic"),
                    ("consolidated", "Consolidated"),
                    ("charity", "Charity"),
                    ("basic_oscr", "Basic (OSCR)"),
                    ("detailed_oscr", "Detailed (OSCR)"),
                ],
                default="basic",
                max_length=50,
            ),
        ),
    ]