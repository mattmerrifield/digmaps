# Generated by Django 2.0.3 on 2018-03-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_site_population'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='code',
            field=models.CharField(help_text='Short, meaningful ID for the site. Assigned by the admin', max_length=40),
        ),
    ]