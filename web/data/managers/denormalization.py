"""
Actually, this is normalization I guess.  A bit of both.
"""
import re

from django.db import models
from django.db import connection, backend, models
import conf

class Denormalize(models.Manager):

    def recipient(self):
        
        cursor = connection.cursor()
        cursor.execute("""
          SELECT *, SUM(f.total_subsidy) as t, COALESCE(cfr, project_no) as recipient_id_fixed
          FROM `data_fishdata` f
          GROUP BY recipient_id_fixed;
        """ % locals())
    
        desc = cursor.description
        result_list = []
        for row in cursor.fetchall():
            p = self.model()
            item = dict(zip([col[0] for col in desc], row))
            p.__dict__.update(item)
            p.amount = item['t']
            result_list.append(p)
        return result_list

    # def non_vessel_recipient(self):

    def years(self):
        cursor = connection.cursor()
        
        cursor.execute("""
          SELECT year
          FROM `data_fishdata` f
          WHERE f.year !=''
          GROUP BY year;
        """)
    
        result_list = []
        for row in cursor.fetchall():
            p = self.model()
            p.year = row[0] or None
            result_list.append(p)
        return result_list
        
    def schemes(self, year=None):
        cursor = connection.cursor()
        result_list = []
        if year:
            cursor.execute("""
              SELECT scheme2_id, scheme_name, year, SUM(total_subsidy) as t, scheme_traffic_light
              FROM `data_fishdata`
              WHERE scheme_name !=''
              AND year = %s
              GROUP BY scheme2_id;
            """, (year,))
        else:
            cursor.execute("""
              SELECT scheme2_id, scheme_name, '0', SUM(total_subsidy) as t, scheme_traffic_light
              FROM `data_fishdata`
              WHERE scheme_name !=''
              GROUP BY scheme2_id;
            """)

        for row in cursor.fetchall():
            p = self.model()
            p.scheme_id = row[0]
            p.name = row[1]
            p.year = row[2]
            p.total = row[3]
            p.traffic_light = row[4]
            result_list.append(p)

        return result_list
        

    def payments(self):

        cursor = connection.cursor()
        cursor.execute("""
          SELECT *, COALESCE(cfr, project_no) as recipient_id
          FROM `data_fishdata` f
          WHERE recipient_id IS NOT NULL;
        """ % locals())

        desc = cursor.description    
        result_list = []
        for row in cursor.fetchall():
            p = self.model()
            item = dict(zip([col[0] for col in desc], row))
            p.__dict__.update(item)
            result_list.append(p)
        return result_list
        

    def ports(self):
        cursor = connection.cursor()
        cursor.execute("""
          SELECT *, SUM(total_subsidy) as total
          FROM `data_fishdata` f
          WHERE port_name IS NOT NULL
          GROUP BY port_name
        """)

        desc = cursor.description
        result_list = []
        for row in cursor.fetchall():
            p = self.model()
            item = dict(zip([col[0] for col in desc], row))
            p.__dict__.update(item)
            result_list.append(p)
        return result_list