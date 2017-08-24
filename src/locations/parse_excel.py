import openpyxl
from django.db import transaction

from locations import models
import bibliography.models


def parse_workbook(file_name):
    wb = openpyxl.load_workbook(file_name)
    sheet = wb.worksheets['sheet1']


class SiteRecord(object):
    def __init__(self, row):
        self.row = row

    @property
    def tags(self):
        """
        Get or create all the period tags this record should have.
        """
        period_names = {
            # Description                           # Shortname
            "Early Bronze Age (undifferentiated)":  "EB-U",
            "Early Bronze I":                       "EB-I",
            "Early Bronze II-III":                  "EB-II/III",
            "Early Bronze II":                      "EB-II",
            "Early Bronze III":                     "EB-III",
            "Early Bronze IV (undifferentiated)":   "EB-IV",
            "Early Bronze IVA":                     "EB-IV/A",
            "Early Bronze IVB":                     "EB-IV/B",
            "Early Bronze IVC":                     "EB-IV/C",
            "Middle Bronze Age (undifferentiated)": "MB-U",
            "Middle Bronze I":                      "MB-I",
            "Middle Bronze II-III":                 "MB-II/III",
            "Middle Bronze II":                     "MB-II",
            "Middle Bronze III":                    "MB-III",
            "Late Bronze Age (undifferentiated)":   "LB-U",
            "Late Bronze I":                        "LB-I",
            "Late Bronze II":                       "LB-II",
            "Late Bronze III":                      'LB-III',
        }
        tags = []
        for desc, short in period_names.items():
            should_tag = self.row[desc]
            if should_tag:
                t, _ = models.Period.objects.get_or_create(
                    shortname=short,
                    defaults={
                        'description': desc
                        'start': 0,
                        'end': 0,
                    })
                tags.append(t)
        return tags

    @property
    def coordinates(self):
        lat = self.row.get('Easting-Lon')
        lon = self.row.get("Northing-Lat")
        return lat, lon

    @property
    def region(self):
        region, _ = models.Region.objects.get_or_create(
            name=self.row['Region']
        )
        return region

    @property
    def references(self):
        references, _ = bibliography.models.Publication.objects.get_or_create(
            authors=self.row['Reference']
        )
        return [references]

    def site(self):
        """
        Take a row of data off of the excel sheet
        """
        with transaction.atomic():
            site, _ = models.Site.objects.get_or_create(
                coordinates=self.coordinates,
                modern_name=self.row['Modern Name'],
                ancient_name=self.row['Ancient Name'],
                area=self.row['SiteSize'],
                notes=self.row['Notes'],
                references=self.references,
                region=self.region,
            )
        return site

