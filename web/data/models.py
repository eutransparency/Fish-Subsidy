from django.db import models
from django.db import connection, backend, models
from fishsubsidy import conf

class FishDataManager(models.Manager):
  
  def top_vessels(self, country=None, limit=10, year=conf.default_year, port=None):
    extra_and = ""
    if port:
      extra_and = "AND port_name = '%s'" % port
    cursor = connection.cursor()
    cursor.execute("""
      SELECT vessel_name, cfr, sum(total_cost) as t 
      FROM `data_fishdata` 
      WHERE iso_country = '%(country)s' AND vessel_name IS NOT NULL AND year='%(year)s'  %(extra_and)s
      GROUP BY vessel_name
      ORDER BY t DESC
      LIMIT %(limit)s;
    """ % {'country' : country, 'year' : year, 'limit' : limit, 'extra_and' : extra_and })
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], cfr=row[1])
        p.total = row[2]
        result_list.append(p)
    return result_list
    
    
  def top_schemes(self, country=None, limit=10, year=conf.default_year, port=None):
    extra_and = ""
    if port:
      extra_and = "AND port_name = '%s'" % port
    cursor = connection.cursor()
    cursor.execute("""
      SELECT scheme_name, scheme2_id, sum(total_cost) t
      FROM data_fishdata 
      WHERE iso_country = '%(country)s' AND year = '%(year)s' %(extra_and)s
      GROUP BY iso_country,scheme2_id
      ORDER BY t DESC
      LIMIT %(limit)s;
    """ % {'country' : country, 'year' : year, 'limit' : limit, 'extra_and' : extra_and })
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(scheme_name=row[0], scheme2_id=row[1])
        p.total = row[2]
        result_list.append(p)
    return result_list
    
  def top_ports(self, country=None, limit=10, year=conf.default_year):
    cursor = connection.cursor()
    cursor.execute("""
      SELECT port_name, sum(total_cost) as t 
      FROM `data_fishdata` 
      WHERE iso_country = '%(country)s' AND port_name IS NOT NULL AND year = '%(year)s'
      GROUP BY port_name 
      ORDER BY t DESC      
      LIMIT %(limit)s;
    """ % {'country' : country, 'year' : year, 'limit' : limit })
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(port_name=row[0])
        p.total = row[1]
        result_list.append(p)
    return result_list
    
  def country_years(self, country):
    cursor = connection.cursor()
    cursor.execute("""
      SELECT distinct(year), sum(total_cost) FROM data_fishdata WHERE iso_country='%(country)s' GROUP BY year ORDER BY year ASC;  
    """ % {'country' : country})
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0], total_cost=row[1])
        result_list.append(p)
    return result_list

  def country_years_traffic_lights(self, country):
    cursor = connection.cursor()
    cursor.execute("""
      SELECT distinct(year), sum(total_cost), scheme_traffic_light FROM data_fishdata WHERE iso_country='%(country)s' GROUP BY year, scheme_traffic_light ORDER BY year ASC;  
    """ % {'country' : country})
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0], total_cost=row[1], scheme_traffic_light=row[2])
        result_list.append(p)
    return result_list
    



class FishData(models.Model):
  """(Data description)"""  
  
  # id = models.TextField(blank=True)
  cci = models.TextField(blank=True)
  description = models.TextField(blank=True)
  project_no = models.TextField(blank=True)
  iso_country = models.TextField(blank=True)
  country_name = models.TextField(blank=True)
  nuts = models.TextField(blank=True)
  geo1 = models.TextField(blank=True)
  geo2 = models.TextField(blank=True)
  municipality_x_cord = models.TextField(blank=True)
  municipality_y_cord = models.TextField(blank=True)
  scheme1_id = models.TextField(blank=True)
  scheme2_id = models.TextField(blank=True)
  scheme_name = models.TextField(blank=True)
  scheme_traffic_light = models.TextField(blank=True)
  status = models.TextField(blank=True)
  status_code_status = models.TextField(blank=True)
  approval_date = models.TextField(blank=True)
  year = models.IntegerField(blank=True)
  total_cost = models.TextField(blank=True)
  member_state = models.TextField(blank=True)
  fifg = models.TextField(blank=True)
  vessel_name = models.TextField(blank=True)
  cfr = models.TextField(blank=True)
  cfr_link = models.TextField(blank=True)
  external_marking = models.TextField(blank=True)
  overall_length = models.TextField(blank=True)
  main_power = models.TextField(blank=True)
  tonnage = models.TextField(blank=True)
  port_name = models.TextField(blank=True)
  port_country = models.TextField(blank=True)
  source = models.TextField(blank=True)
  period = models.TextField(blank=True)
  port_lng = models.TextField(blank=True)
  port_lat = models.TextField(blank=True)
  recipient_id = models.TextField(blank=True)
  tuna_fleet = models.TextField(blank=True)
  construction_year = models.TextField(blank=True)
  construction_place = models.TextField(blank=True)
  recipient_name = models.TextField(blank=True)
  greenpeace_link = models.TextField(blank=True)
  lenght_code = models.TextField(blank=True)
  
  objects = FishDataManager()
   
  def __unicode__(self):
    return "%s" % self.pk

  def top_vessels(self):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("""
      SELECT vessel_name v, 
             (SELECT SUM(total_cost) 
              FROM `data_fishdata`
              WHERE vessel_name = v
              ) as total
              
      """)
    row = cursor.fetchone() 
    return row 

    

def port_vessel_count(country):
  from django.db import connection, transaction
  cursor = connection.cursor()

  cursor.execute('SELECT port_name, port_name as p, (SELECT count(port_name) FROM `data_fishdata` WHERE port_name=p) as vessels FROM `data_fishdata` WHERE iso_country="%s" AND scheme2_id <= 10 AND port_name IS NOT NULL GROUP BY port_name;' % country)
  desc = cursor.description
  dict = {}
  # print cursor.rowcount
  data = cursor.fetchall()  
  for i ,row in enumerate(data):
    dict[i] = {}
    for (name, value) in zip(desc, row) :
      dict[i][name[0]] = value

  return dict






