# Generated by Django 2.0.3 on 2018-03-21 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("locations", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="feature",
            name="shortname",
            field=models.CharField(max_length=20, unique=True),
        )
    ]
