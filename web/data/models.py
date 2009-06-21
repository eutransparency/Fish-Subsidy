from django.db import models
from django.db import connection, backend, models
from fishsubsidy import conf

class FishDataManager(models.Manager):
  
  def top_vessels(self, country=None, limit=20, year=conf.default_year, port=None):
    extra_and = ""
    if port:
      extra_and = "AND port_name = '%s'" % port
    if country and country != "EU":
      extra_and += " AND `iso_country` = '%s'" % country
    if year and str(year) != "0":
      extra_and += " AND year='%s'" % year
      
    cursor = connection.cursor()
    cursor.execute("""
      SELECT vessel_name, cfr, sum(total_cost) as t, iso_country, count(cfr), port_name 
      FROM `data_fishdata` 
      WHERE vessel_name IS NOT NULL  %(extra_and)s
      GROUP BY cfr
      ORDER BY t DESC
      LIMIT %(limit)s;
    """ % {'country' : country, 'year' : year, 'limit' : limit, 'extra_and' : extra_and })
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], cfr=row[1], total_cost=row[2], iso_country=row[3], status=row[4], port_name=row[5])
        p.total = row[2]
        result_list.append(p)
    return result_list
    
  def top_vessels_by_scheme(self, scheme_id, country=None, limit=10):
    extra_and = ""
    cursor = connection.cursor()
    cursor.execute("""
      SELECT vessel_name, cfr, sum(total_cost) as t, iso_country, port_name 
      FROM `data_fishdata` 
      WHERE scheme2_id = %(scheme_id)s AND vessel_name IS NOT NULL  %(extra_and)s
      GROUP BY vessel_name
      ORDER BY t DESC
      LIMIT %(limit)s;
    """ % {'scheme_id' : scheme_id, 'country' : country, 'limit' : limit, 'extra_and' : extra_and })
        
    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], cfr=row[1], total_cost=row[2], iso_country=row[3], port_name=row[4])
        p.total = row[2]
        result_list.append(p)
    return result_list
    
    
  def top_schemes(self, country=None, limit=10, year=conf.default_year, port=None):
    extra_and = ""
    if port:
      extra_and = "AND port_name = '%s'" % port
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += " AND iso_country = '%s' " % country
      
    cursor = connection.cursor()
    cursor.execute("""
      SELECT scheme_name, scheme2_id, sum(total_cost) t, scheme_traffic_light
      FROM data_fishdata 
      WHERE scheme2_id IS NOT NULL %(extra_and)s
      GROUP BY iso_country,scheme2_id
      ORDER BY t DESC
      LIMIT %(limit)s;
    """ % {'country' : country, 'year' : year, 'limit' : limit, 'extra_and' : extra_and })
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(scheme_name=row[0], scheme2_id=row[1], scheme_traffic_light=row[3], total_cost=row[2])
        p.total = row[2]
        result_list.append(p)
    return result_list
    
  def top_ports(self, country=None, limit=10, year=conf.default_year, geo1=None, scheme_id=None):
    extra_and = ""
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += " AND iso_country = '%s'" % country
    if geo1:
      extra_and += " AND geo1='%s'" % geo1
    if scheme_id:
      extra_and += " AND scheme2_id='%s'" % scheme_id
    
    cursor = connection.cursor()
    cursor.execute("""
      SELECT port_name, sum(total_cost) as t 
      FROM `data_fishdata` 
      WHERE port_name IS NOT NULL %(extra_and)s
      GROUP BY port_name 
      ORDER BY t DESC      
      LIMIT %(limit)s;
    """ % {'country' : country, 'year' : year, 'limit' : limit, 'extra_and' : extra_and })
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(port_name=row[0])
        p.total = row[1]
        result_list.append(p)
    return result_list
    
  def country_years(self, country):
    where = "WHERE year IS NOT NULL "
    if country and country != "EU":
      where += "AND iso_country='%s'" % country
      
    cursor = connection.cursor()
    cursor.execute("""
      SELECT distinct(year), sum(total_cost) 
      FROM data_fishdata %(where)s GROUP BY year ORDER BY year ASC;  
    """ % {'country' : country, 'where' : where})
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0], total_cost=row[1])
        result_list.append(p)
    return result_list

  def country_years_traffic_lights(self, country):
    extra_and = ""
    if country == 0:
      extra_and = "AND iso_country='%s" % country
    cursor = connection.cursor()
    cursor.execute("""
      SELECT distinct(year), sum(total_cost), scheme_traffic_light 
      FROM data_fishdata 
      WHERE year IS NOT NULL %(extra_and)s 
      GROUP BY year, scheme_traffic_light 
      ORDER BY year ASC;  
    """ % {'extra_and' : extra_and})
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0], total_cost=row[1], scheme_traffic_light=row[2])
        result_list.append(p)
    return result_list
    
  def scheme_years(self, scheme_id, country='EU'):
    cursor = connection.cursor()
    extra_and = ""
    if country and country != "EU" :
      extra_and = "AND `iso_country`='%s'" % country

    cursor.execute("""
      SELECT year, sum(total_cost), scheme_traffic_light, scheme_name, scheme2_id 
      FROM `data_fishdata` 
      WHERE scheme2_id=%(scheme_id)s %(extra_and)s 
      GROUP BY `year`
    """ % {'scheme_id' : scheme_id, 'extra_and' : extra_and})
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0], total_cost=row[1], scheme_traffic_light=row[2], scheme_name=row[3], scheme2_id=row[4])
        result_list.append(p)
    return result_list

  def schemes(self, country=None, year=conf.default_year):
    cursor = connection.cursor()
    
    extra_and = ""    
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += "AND `iso_country`='%s'" % country

    cursor.execute("""
      SELECT sum(total_cost) as t, scheme_traffic_light, scheme_name, scheme2_id 
      FROM `data_fishdata` WHERE scheme_name IS NOT NULL %(extra_and)s 
      GROUP BY `scheme2_id`
      ORDER BY t DESC
    """ % {'extra_and' : extra_and, 'year' : year})

    result_list = []
    for row in cursor.fetchall():
        p = self.model(total_cost=row[0], scheme_traffic_light=row[1], scheme_name=row[2], scheme2_id=row[3])
        result_list.append(p)
    return result_list
    

  def scheme_length_count(self, scheme_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT `overall_length` FROM `data_fishdata` WHERE scheme2_id=%(scheme_id)s AND `overall_length` IS NOT NULL GROUP BY `overall_length`
      """ % {'scheme_id' : scheme_id})
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(overall_length=row[0])
        result_list.append(p)
    return result_list
    

  def browse(self, country, sort='total_cost', year=conf.default_year, geo1=None):
    extra_and = ""
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += "AND iso_country='%s'" % country
    if geo1:
      extra_and += "AND geo1='%s'" % geo1
    
    cursor = connection.cursor()
    cursor.execute("""
            SELECT vessel_name, sum(total_cost) as total_cost, port_name, cfr, iso_country
            FROM `data_fishdata` 
            WHERE `vessel_name` IS NOT NULL %(extra_and)s 
            GROUP BY `cfr` 
            ORDER BY %(sort)s 
          """ % {'sort' : sort, 'country' : country, 'extra_and' : extra_and})
              
    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], total_cost=row[1], port_name=row[2], cfr=row[3], iso_country=row[4])
        result_list.append(p)
    return result_list


  def port_browse(self, country, sort='total_cost', year=conf.default_year):
    extra_and = ""
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += "AND iso_country='%s'" % country
    
    cursor = connection.cursor()
    cursor.execute("""
        SELECT port_name, sum(total_cost) as total_cost, port_name, cfr, iso_country
        FROM `data_fishdata` 
        WHERE `port_name` IS NOT NULL  %(extra_and)s
        GROUP BY `port_name` 
        ORDER BY %(sort)s 
      """ % {'sort' : sort, 'country' : country, 'extra_and' : extra_and})

    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], total_cost=row[1], port_name=row[2], cfr=row[3], iso_country=row[4])
        result_list.append(p)
    return result_list
      
  def geo(self,geo=1,country="EU", sort="total_cost DESC", year=conf.default_year, geo1=None, scheme_id=None):
    extra_and = ""
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += " AND iso_country='%s'" % country
    if geo1:
      extra_and += " AND geo1='%s'" % geo1
    if scheme_id:
      extra_and += " AND scheme2_id='%s'" % scheme_id
      

    cursor = connection.cursor()
    cursor.execute("""    
      SELECT geo1,geo2, sum(total_cost) as total_cost
      FROM `data_fishdata`
      WHERE geo%(geo)s IS NOT NULL %(extra_and)s
      GROUP BY geo%(geo)s
      ORDER BY %(sort)s
      """ % {'sort' : sort, 'country' : country, 'extra_and' : extra_and, 'geo' : geo})
      
    result_list = []
    for row in cursor.fetchall():
        p = self.model(geo1=row[0], geo2=row[1], total_cost=row[2])
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


    
