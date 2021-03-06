# Generated by Django 2.2 on 2019-10-04 00:59

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bibliography', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortname', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('shortname', models.CharField(help_text="Unique code name, e.g. 'EBIV'", max_length=10, unique=True)),
                ('description', models.TextField(default='')),
                ('start', models.IntegerField(help_text='Approximate Beginning (BCE is negative)')),
                ('end', models.IntegerField(help_text='Approximate Ending (BCE is negative)')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Short, meaningful identifier for the site. Assigned by the admin.', max_length=40)),
                ('modern_name', models.CharField(blank=True, default='', help_text='Name used by modern peoples', max_length=50)),
                ('ancient_name', models.CharField(blank=True, default='', help_text='Name used by ancient peoples to describe the location', max_length=50)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('area', models.FloatField(blank=True, help_text="Area of the site in Hectares. Null represents 'unknown'", null=True)),
                ('population', models.FloatField(blank=True, null=True)),
                ('survey_type', models.CharField(blank=True, choices=[('surface', 'Surface_Survey'), ('excavation', 'Excavation')], default='', max_length=25)),
                ('notes', models.TextField(blank=True, default='')),
                ('notes_easting_northing', models.TextField(blank=True, default='', editable=False, help_text='value of the original coordinate system of record, if it was easting/northing. Do not use directly')),
            ],
        ),
        migrations.CreateModel(
            name='SitePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Period')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Site')),
            ],
        ),
        migrations.CreateModel(
            name='SiteFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evidence', models.PositiveSmallIntegerField(choices=[(100, 'Very_Clear'), (75, 'Clear'), (50, 'Typical'), (25, 'Unclear'), (0, 'Very_Unclear')], default=50, help_text='How clear is the evidence for the site to have this feature?')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Feature')),
                ('periods', models.ManyToManyField(to='locations.Period')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Site')),
            ],
            options={
                'unique_together': {('site', 'feature')},
            },
        ),
        migrations.AddField(
            model_name='site',
            name='features',
            field=models.ManyToManyField(related_name='sites', through='locations.SiteFeature', to='locations.Feature'),
        ),
        migrations.AddField(
            model_name='site',
            name='periods',
            field=models.ManyToManyField(related_name='sites', through='locations.SitePeriod', to='locations.Period'),
        ),
        migrations.AddField(
            model_name='site',
            name='references',
            field=models.ManyToManyField(to='bibliography.Publication'),
        ),
        migrations.AddField(
            model_name='site',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Region'),
        ),
    ]
