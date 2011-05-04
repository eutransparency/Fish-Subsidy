"""
Actually, this is normalization I guess.  A bit of both.
"""
import re
from decimal import *

from django.db import models
from django.db import connection, backend, models

class Denormalize(models.Manager):

    def recipient(self):
        
        cursor = connection.cursor()
        cursor.execute("""
          SELECT 
          id, cci, description, project_no, iso_country, country_name, nuts, geo1, geo2, municipality_x_cord, municipality_y_cord, scheme1_id, scheme2_id, scheme_name, scheme_traffic_light, status, status_code_status, approval_date, "year", total_cost, member_state, fifg, vessel_name, cfr, cfr_link, external_marking, overall_length, main_power, tonnage, port_name, port_country, source, period, port_lng, port_lat, recipient_id, tuna_fleet, construction_year, construction_place, recipient_name, greenpeace_link, lenght_code, 
          SUM(f.total_subsidy) as t, COALESCE(cfr, project_no) as recipient_id_fixed
          FROM data_fishdata f
          GROUP BY recipient_id_fixed, id, cci, description, project_no, iso_country, country_name, nuts, geo1, geo2, municipality_x_cord, municipality_y_cord, scheme1_id, scheme2_id, scheme_name, scheme_traffic_light, status, status_code_status, approval_date, "year", total_cost, member_state, fifg, vessel_name, cfr, cfr_link, external_marking, overall_length, main_power, tonnage, port_name, port_country, source, period, port_lng, port_lat, recipient_id, tuna_fleet, construction_year, construction_place, recipient_name, greenpeace_link, lenght_code;
        """ % locals())
    
        desc = cursor.description
        result_list = []
        for row in cursor.fetchall():
            p = self.model()
            item = dict(zip([col[0] for col in desc], row))
            p.__dict__.update(item)
            if item['t']:
                p.amount = Decimal(str(item['t']))
            else:
                p.amount = Decimal(0)
            result_list.append(p)
        return result_list

    def years(self):
        cursor = connection.cursor()
        
        cursor.execute("""
          SELECT year
          FROM data_fishdata f
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
        # if year:
        #     cursor.execute("""
        #       SELECT scheme2_id, scheme_name, year, SUM(total_subsidy) as t, scheme_traffic_light
        #       FROM `data_fishdata`
        #       WHERE scheme_name !=''
        #       AND year = %s
        #       GROUP BY scheme2_id;
        #     """, (year,))
        # else:
        cursor.execute("""
            SELECT scheme2_id, scheme_name, SUM(total_subsidy) as t, MAX(scheme_traffic_light)
            FROM data_fishdata
            WHERE scheme_name !=''
            AND scheme_traffic_light !='0'
            GROUP BY scheme2_id, scheme_name, scheme_traffic_light;        
            """)

        for row in cursor.fetchall():
            p = self.model()
            p.scheme_id = row[0]
            p.name = row[1]
            if row[2]:
                p.total = Decimal(str(row[2]))
            else:
                p.total = Decimal(0)
            p.traffic_light = row[3]
            result_list.append(p)

        return result_list
        

    def payments(self):

        cursor = connection.cursor()
        cursor.execute("""
          SELECT total_subsidy, year, iso_country, port_name, COALESCE(cfr, project_no) as recipient_id
          FROM data_fishdata f
          WHERE recipient_id IS NOT NULL;
        """ % locals())

        desc = cursor.description    
        result_list = []
        for row in cursor.fetchall():
            p = self.model()
            item = dict(zip([col[0] for col in desc], row))
            if item.get('amount'):
                item['amount'] = Decimal(str(item['amount']))
            else:
                item['amount'] = Decimal(0)
            p.__dict__.update(item)
            result_list.append(p)
        return result_list
        

    def ports(self):
        cursor = connection.cursor()
        cursor.execute("""
          SELECT 
          id, cci, description, project_no, iso_country, country_name, nuts, geo1, geo2, municipality_x_cord, municipality_y_cord, scheme1_id, scheme2_id, scheme_name, scheme_traffic_light, status, status_code_status, approval_date, "year", total_cost, member_state, fifg, vessel_name, cfr, cfr_link, external_marking, overall_length, main_power, tonnage, port_name, port_country, source, period, port_lng, port_lat, recipient_id, tuna_fleet, construction_year, construction_place, recipient_name, greenpeace_link, lenght_code, 
          SUM(total_subsidy) as total
          FROM data_fishdata f
          WHERE port_name IS NOT NULL
          GROUP BY port_name, id, cci, description, project_no, iso_country, country_name, nuts, geo1, geo2, municipality_x_cord, municipality_y_cord, scheme1_id, scheme2_id, scheme_name, scheme_traffic_light, status, status_code_status, approval_date, "year", total_cost, member_state, fifg, vessel_name, cfr, cfr_link, external_marking, overall_length, main_power, tonnage, port_name, port_country, source, period, port_lng, port_lat, recipient_id, tuna_fleet, construction_year, construction_place, recipient_name, greenpeace_link, lenght_code;
        """)

        desc = cursor.description
        result_list = []
        for row in cursor.fetchall():
            p = self.model()
            item = dict(zip([col[0] for col in desc], row))
            if item['total']:
                item['total'] = Decimal(str(item['total']))
            else:
                item['total'] = 0
            p.__dict__.update(item)
            result_list.append(p)
        return result_list
