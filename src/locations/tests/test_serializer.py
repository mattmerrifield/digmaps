from django.test import TestCase

from locations import parse_excel
from pprint import pprint
print = pprint


class SerializerTestCase(TestCase):
    """
    Parse one record of the Excel spreadsheet correctly, or get fucked.
    """
    
    def test_one_record(self):
        """
        Don't fuck it up
        """
        # This is, roughly speaking, what a row of excel data looks like
        record = {
            "AutoID":                               1,
            "Site ID":                              'ASI49-14',
            "Modern Name":                          'Abu er Riqaqi (southwest)',
            "Ancient Name":                         '',
            "Easting":                              203082,
            "Northing":                             719547,
            "Easting-Long":                         35.030066769,
            "Northing-Lat":                         32.570052158,
            "SiteSize":                             '',
            "Region":                               'TestRegion',
            "GeologicType":                         '',
            "SiteType":                             'Surface',
            "SiteFunction":                         'Unknown',
            "BurialType":                           '',
            "Reference":                            'Tepper Yotam , Gadot Yuval',
            "Notes":                                'Cupmarks and rock-cuttings in a circular depression (a collapsed cave?) on the N side of a small valley. In a nearby cleft of bedrock  to the N (map ref. OIG 15310 21980, NIG 20310 71980), pottery sherds were observed  between a layer of limestone and its overlying layer of nari (likely to assist in dating the upper geological stratum). Pottery: Late Bronze, Iron Age II, Byzantine.',
            "Chalcolithic (undifferentiated)":      0,
            "Early Chalcolithic":                   0,
            "Late Chalcolithic":                    0,
            "Early Bronze Age (undifferentiated)":  0,
            "Early Bronze I":                       0,
            "Early Bronze II-III":                  0,
            "Early Bronze II":                      0,
            "Early Bronze III":                     0,
            "Early Bronze IV (undifferentiated)":   0,
            "Early Bronze IVA":                     0,
            "Early Bronze IVB":                     0,
            "Early Bronze IVC":                     0,
            "Middle Bronze Age (undifferentiated)": 0,
            "Middle Bronze I":                      0,
            "Middle Bronze II-III":                 0,
            "Middle Bronze II":                     0,
            "Middle Bronze III":                    0,
            "Late Bronze Age (undifferentiated)":   1,
            "Late Bronze I":                        0,
            "Late Bronze II":                       0,
            "Late Bronze III":                      0,
        }
        site = parse_excel.parse_site(record)
