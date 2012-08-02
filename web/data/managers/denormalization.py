"""
Actually, this is normalization I guess.  A bit of both.
"""
import re
from decimal import *

from django.db import models
from django.db import connection, backend, models

class Denormalize(models.Manager):
    
    def reltriggers(self, enable=False):
        cursor = connection.cursor()
    
        if enable:
            cursor.execute("""
                ALTER TABLE data_recipient ENABLE TRIGGER ALL;
                ALTER TABLE data_payment ENABLE TRIGGER ALL;
                ALTER TABLE data_scheme ENABLE TRIGGER ALL;
            """)
        else:
            cursor.execute("""
                ALTER TABLE data_recipient DISABLE TRIGGER ALL;
                ALTER TABLE data_payment DISABLE TRIGGER ALL;
                ALTER TABLE data_scheme DISABLE TRIGGER ALL;
            """)
    
    
    def recipient(self):
        
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM data_recipient WHERE recipient_type = 'vessel';
            INSERT INTO data_recipient
            SELECT 'vessel' as recipient_type, cfr as recipient_id, MAX(vessel_name), MAX(iso_country), MAX(p.id), SUM(total_subsidy), MAX(geo1), MAX(geo2)
            FROM data_fishdata as d
            LEFT JOIN (SELECT MAX(id) as id, name FROM data_port GROUP BY name) as p on p.name=d.port_name
            WHERE cfr IS NOT NULL
            GROUP BY cfr;
        """)

        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM data_recipient WHERE recipient_type = 'nonvessel';
            INSERT INTO data_recipient
            SELECT 'nonvessel' as recipient_type, project_no as recipient_id, MAX(vessel_name), MAX(iso_country), MAX(p.id), SUM(total_subsidy), MAX(geo1), MAX(geo2)
            FROM data_fishdata as d
            LEFT JOIN (SELECT MAX(id) as id, name FROM data_port GROUP BY name) as p on p.name=d.port_name
            WHERE project_no IS NOT NULL
            GROUP BY project_no;
        """)
    
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
        cursor.execute("""
            DELETE FROM data_scheme;
            INSERT INTO data_scheme (scheme_id, total, traffic_light)
            SELECT scheme2_id, SUM(total_subsidy) as t, CAST(MAX(scheme_traffic_light) as integer)
            FROM data_fishdata
            WHERE scheme_name !=''
            AND scheme_traffic_light !='0'
            GROUP BY scheme2_id, scheme_name, scheme_traffic_light;
            
            """)

        

    def payments(self):

        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM data_payment;
        INSERT INTO data_payment (recipient_id_id, amount, year, port_id, scheme_id, country)
        SELECT COALESCE(cfr, project_no) as recipient_id_id,  total_subsidy as amount, year, p.id as port_id, scheme2_id as scheme_id, iso_country
        FROM data_fishdata as d
        LEFT JOIN (SELECT MAX(id) as id, name FROM data_port GROUP BY name) as p on p.name=d.port_name
        WHERE COALESCE(cfr, project_no) IS NOT NULL;
        COMMIT;
        """)
        

    def ports(self):
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM data_port;
        INSERT INTO data_port (name, country, total, geo1, geo2, lat, lng)
        SELECT 
            port_name, 
            iso_country, 
            SUM(total_subsidy) as t, 
            MAX(geo1), 
            MAX(geo2),
            AVG(CAST(port_lat as double precision)),
            AVG(CAST(port_lng as double precision))
        FROM data_fishdata
        WHERE total_subsidy IS NOT NULL
        AND port_name IS NOT NULL
        GROUP BY port_name, iso_country;
        """)

