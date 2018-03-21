import openpyxl
from django.db import transaction

import bibliography.models
from locations.models import Feature, SitePeriod, SiteFeature, Region, Site


def period_choices():
    """
    All the Period choices implied by the excel sheet column names in the period matrix
    """
    period_names = {
        # Excel Column name (description)       # Shortname
        "Early Bronze Age (undifferentiated)":  ("EB-U", -3300, -3000),
        "Early Bronze I":                       ("EB-I", -3000, -2700),
        "Early Bronze II-III":                  ("EB-II/III", -3000, -2200),
        "Early Bronze II":                      ("EB-II", -3000, -2700),
        "Early Bronze III":                     ("EB-III", -2700, -00),
        "Early Bronze IV (undifferentiated)":   ("EB-IV", -2200, -2100),
        "Early Bronze IVA":                     ("EB-IV/A", -2200, -2000),
        "Early Bronze IVB":                     ("EB-IV/B", -2200, -2000),
        "Early Bronze IVC":                     ("EB-IV/C", -2200, -2000),
        "Middle Bronze Age (undifferentiated)": ("MB-U", -2000, -1550),
        "Middle Bronze I":                      ("MB-I", -2000, -1750),
        "Middle Bronze II-III":                 ("MB-II/III", -1750, -1550),
        "Middle Bronze II":                     ("MB-II", -1750, -1650),
        "Middle Bronze III":                    ("MB-III", -1650, -1550),
        "Late Bronze Age (undifferentiated)":   ("LB-U", -1550, -1200),
        "Late Bronze I":                        ("LB-I", -1400, -1300),
        "Late Bronze II":                       ("LB-II", -1400, -1300),
        "Late Bronze III":                      ('LB-III', -1300, -1400),
        "Later Uncategorized":                  ("Later", -14000, 0),
    }
    choices = {}
    for desc, (short, start, end) in period_names.items():
        t, _ = Period.objects.get_or_create(
            shortname=short,
            defaults={
                'description': desc,
                'start': start,
                'end': end,
            })
        choices[desc] = t
    return choices


class SiteRecord(object):
    def __init__(self, row):
        self.row = row
        self.period_choices = period_choices()

    def periods(self):
        """
        Period tags are stored as 1/0 in specific fields.
        """
        tags = []
        for description, tag in self.period_choices.items():
            is_tagged = self.row[description]
            if is_tagged:
                tags.append(tag)

        # But there's a default catch-all "Later" period, since we didn't bother explicitly tagging things that had
        # settlement evidence during the late bronze. Sites with only a single tag are also assumed to be occupied in
        # the late bronze onward, unless explicitly tagged as "single period"
        if len(tags) == 1 and self.row['Site Type'] != 'Single Period':
            tags.append(self.period_choices['Later Uncategorized'])
        return tags

    def features(self):
        """
        Some fields' contents should just get stored as feature tags. We'll sort the deets out later.
        """
        fields = 'Region GeologicType SiteType SiteFunction BurialType'.split()
        for field_name in fields:
            value = self.row[field_name]
            if value:
                f, _ = Feature.objects.get_or_create(
                    shortname=value,
                    defaults={
                        'name': value,
                    }
                )
                yield f

    def references(self):
        references, _ = bibliography.models.Publication.objects.get_or_create(
            title=self.row['Reference'],
        )
        return [references]

    def region(self):
        region, _ = Region.objects.get_or_create(
            name=self.row['Region'],
        )
        return region

    def site(self):
        """
        Take a row of data off of the excel sheet
        """
        with transaction.atomic():
            site, _ = Site.objects.get_or_create(
                coordinates=(self.row.get('Easting-Lon'), self.row.get('Northing-Lat')),
                modern_name=self.row['Modern Name'],
                ancient_name=self.row['Ancient Name'],
                area=self.row['SiteSize'],
                notes=self.row['Notes'],
                notes_easting_northing="Original Coordinates: {Easting}/{Northing}".format(**self.row),
                region=self.region(),
                references=self.references(),
            )
            for period in self.periods():
                SitePeriod.objects.get_or_create(
                    site=site,
                    period=period,
                )
            for feature in self.features():
                SiteFeature.objects.get_or_create(
                    site=site,
                    feature=feature,
                )

            for ref in self.references():

                site.references.add(ref)
        return site


def parse_workbook(file_name):
    wb = openpyxl.load_workbook(file_name)
    sheet = wb.worksheets['sheet1']



