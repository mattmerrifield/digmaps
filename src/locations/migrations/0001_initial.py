# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 00:35
from __future__ import unicode_literals

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
            name='Citation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(help_text="The ID number assigned to the site by the publication authors (e.g. 'ASI85-35' or 'BSL-123'", max_length=100)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliography.Publication')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='locations.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modern_name', models.CharField(blank=True, max_length=50, null=True)),
                ('ancient_name', models.CharField(blank=True, max_length=50, null=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('area', models.FloatField(blank=True, help_text='Area in Hectares', null=True)),
                ('notes', models.TextField(default='')),
                ('references', models.ManyToManyField(through='locations.Citation', to='bibliography.Publication')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Region')),
            ],
        ),
        migrations.CreateModel(
            name='SiteTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uncertain', models.BooleanField(default=False, help_text='Evidence for for this tag on this site is not conclusive')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Site')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortname', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Burial',
            fields=[
                ('tag_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='locations.Tag')),
                ('type', models.CharField(choices=[('tomb', 'Tomb'), ('carins', 'Carins'), ('cemetary', 'Cemetary')], max_length=50)),
            ],
            bases=('locations.tag',),
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('tag_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='locations.Tag')),
                ('start', models.IntegerField(help_text='Approximate Beginning (BCE is negative)')),
                ('end', models.IntegerField(help_text='Approximate Ending (BCE is negative)')),
            ],
            bases=('locations.tag',),
        ),
        migrations.AddField(
            model_name='tag',
            name='sites',
            field=models.ManyToManyField(related_name='tags', through='locations.SiteTag', to='locations.Site'),
        ),
        migrations.AddField(
            model_name='sitetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Tag'),
        ),
        migrations.AddField(
            model_name='citation',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Site'),
        ),
        migrations.AlterUniqueTogether(
            name='sitetag',
            unique_together=set([('site', 'tag')]),
        ),
    ]
