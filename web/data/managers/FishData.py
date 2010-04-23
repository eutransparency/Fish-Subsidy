import re

from django.db import models
from django.db import connection, backend, models
from django.db.models import Sum, Max
from django.db.models.query import QuerySet, Q
import conf


from django.utils.translation import get_language
import multilingual

class illegalFishingManager(models.Manager):
  
  def all_infringements(self, sort='date'):
    
    if sort == 'country':
        order_by = 'f.iso_country ASC'
    elif sort == 'vessel':
        order_by = 'f.vessel_name ASC'
    elif sort == 'total':
        order_by = 't DESC'
    elif sort == 'port':
        order_by = 'f.port_name ASC'
    else:
        order_by = 'i.date DESC'
    
    cursor = connection.cursor()
    cursor.execute("""
      SELECT i.*, f.vessel_name, f.iso_country, f.port_name, SUM(f.total_subsidy) as t
      FROM data_illegalfishing i
      INNER JOIN `data_fishdata` f
      ON i.cfr = f.cfr
      WHERE f.vessel_name IS NOT NULL
      GROUP BY i.id
      ORDER BY %(order_by)s;
    """ % locals())
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(cfr=row[1], date=row[2], sanction=row[3], description=row[4], skipper=row[5])
        p.vesssel_name = row[6] or row[1]
        p.iso_country = row[7]
        p.port_name = row[8]
        p.total = row[9]
        result_list.append(p)
    return result_list


class VesselsManager(models.Manager):
    def get_query_set(self):
        return super(VesselsManager, self).get_query_set().filter(
                                                    recipient_type='vessel'
                                                    )

    def top_vessels(self, country=None, port=None, scheme_id=None, year=0):
        vessels = self.all()
        kwargs = {}
        if country and country!='EU':
            kwargs['country'] = country
            kwargs['payment__country'] = country
        if int(year) != 0:
            kwargs['payment__year__exact'] = year
        if port:
            kwargs['port__name'] = port
        if scheme_id:
            kwargs['payment__scheme__exact'] = scheme_id

        vessels = vessels.filter(port__country=country, **kwargs)
        vessels = vessels.annotate(payment_total=Sum('payment__amount'))
        vessels = vessels.order_by('-payment_total')
        vessels = vessels[:20]
        vessels = vessels.select_related('port__name')
        return vessels


class NonVesselsManager(models.Manager):
    def get_query_set(self):
        return super(NonVesselsManager, self).get_query_set().filter(
                                                    recipient_type='nonvessel'
                                                    )


    def top_beneficiaries(self, country=None, port=None, scheme_id=None, year=0):
        beneficiaries = self.all()
        kwargs = {}
        if country and country!='EU':
            kwargs['country'] = country
            kwargs['payment__country'] = country
        if int(year) != 0:
            kwargs['payment__year__exact'] = year
        if port:
            kwargs['port__name'] = port
        if scheme_id:
            kwargs['payment__scheme__exact'] = scheme_id

        beneficiaries = beneficiaries.filter(**kwargs)
        beneficiaries = beneficiaries.annotate(payment_total=Sum('payment__amount'))
        beneficiaries = beneficiaries.order_by('-payment_total')
        beneficiaries = beneficiaries.select_related('port__name')
        return beneficiaries


    
class SchemeManager(multilingual.Manager):
    
    def top_schemes(self, country=None, year=0, limit=10):
        """
        Schemes have a global total, but not one per country.
        
        Because of this, we can get a total for all countries easier than we
        can get a total for one country.

        """

        name_value = "name_%s" % get_language()

        top_schemes = self.values("scheme_id", name_value)
        kwargs = {}

        if country and country != "EU":
            kwargs['payment__country__exact'] = country

        if int(year) != 0:
            kwargs['payment__year__exact'] = year
        top_schemes = top_schemes.filter(**kwargs)
        top_schemes = top_schemes.annotate(total=Sum('payment__amount'))
        top_schemes = top_schemes.values(name_value, "traffic_light", "total", "scheme_id")
        top_schemes = top_schemes.order_by('-total')
        
        if limit:
            return top_schemes[:limit]
        else:
            return top_schemes

    
    
    
class FishDataManager(models.Manager):
  
  def get_latest_row(self, pk):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM 
    (SELECT *, COALESCE(cfr, project_no) as recipient_id_fixed FROM data_fishdata f
    WHERE cfr=%s OR project_no=%s
    ORDER BY year DESC
    LIMIT 1
    ) t
    """, (pk,pk,))

    desc = cursor.description
    result_list = []
    for row in cursor.fetchall():
        p = self.model()
        p.__dict__.update(dict(zip([col[0] for col in desc], row)))
        result_list.append(p)
    return result_list[0]
      

  def top_vessels(self, country=None, limit=20, year=conf.default_year, port=None):
    extra_and = ""
    if port:
      extra_and += " AND port_name = '%s'" % re.escape(port)
    if country and country != "EU":
      extra_and += " AND `iso_country` = '%s'" % country
    if year and str(year) != "0":
      extra_and += " AND year='%s'" % year
      
    cursor = connection.cursor()
    cursor.execute("""
      SELECT vessel_name, cfr, sum(total_subsidy) as t, iso_country, count(cfr), port_name 
      FROM `data_fishdata` 
      WHERE vessel_name IS NOT NULL  %(extra_and)s
      GROUP BY cfr
      ORDER BY t DESC
      LIMIT %(limit)s;
    """ % {'country' : country, 'year' : year, 'limit' : limit, 'extra_and' : extra_and })
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], cfr=row[1], total_subsidy=row[2], iso_country=row[3], status=row[4], port_name=row[5])
        p.total = row[2]
        result_list.append(p)
    return result_list
  
  def tuna_fleet(self, country):
    extra_and = ""  
    if country and country != "EU":
      extra_and += " AND iso_country='%s'" % country
    
    cursor = connection.cursor()
    cursor.execute("""
      SELECT vessel_name, cfr, sum(total_subsidy) as t, iso_country, count(cfr), port_name 
      FROM `data_fishdata` 
      WHERE vessel_name IS NOT NULL AND `tuna_fleet` IS NOT NULL  %(extra_and)s
      GROUP BY cfr
      ORDER BY t DESC;
    """ % {'extra_and' : extra_and })
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], cfr=row[1], total_subsidy=row[2], iso_country=row[3], status=row[4], port_name=row[5])
        p.total = row[2]
        result_list.append(p)
    return result_list
    
  
    
  def top_vessels_by_scheme(self, scheme_id, country=None, limit=10, year=conf.default_year):

    extra_and = ""    
    if year and str(year) != "0":
      extra_and += " AND year='%s'" % year

    if country and country != "EU":
      extra_and += " AND `iso_country` = '%s'" % country


    cursor = connection.cursor()
    cursor.execute("""
      SELECT vessel_name, cfr, sum(total_subsidy) as t, iso_country, port_name 
      FROM `data_fishdata` 
      WHERE scheme2_id = %(scheme_id)s AND vessel_name IS NOT NULL  %(extra_and)s
      GROUP BY cfr
      ORDER BY t DESC
      LIMIT %(limit)s;
    """ % {'scheme_id' : scheme_id, 'country' : country, 'limit' : limit, 'extra_and' : extra_and })
        
    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], cfr=row[1], total_subsidy=row[2], iso_country=row[3], port_name=row[4])
        p.total = row[2]
        result_list.append(p)
    return result_list
    
    
  def top_schemes(self, country=None, limit=10, year=conf.default_year, port=None):
    extra_and = ""
    if port:
      extra_and = "AND port_name = '%s'" % re.escape(port)
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += " AND iso_country = '%s' " % country
    
    cursor = connection.cursor()
    cursor.execute("""
      SELECT scheme_name, scheme2_id, sum(total_subsidy) t, scheme_traffic_light
      FROM data_fishdata 
      WHERE scheme2_id IS NOT NULL %(extra_and)s
      GROUP BY iso_country,scheme2_id
      ORDER BY t DESC
      LIMIT %(limit)s;
    """ % {'country' : country, 'year' : year, 'limit' : limit, 'extra_and' : extra_and })
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(scheme_name=row[0], scheme2_id=row[1], scheme_traffic_light=row[3], total_subsidy=row[2])
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
      extra_and += " AND geo1='%s'" % re.escape(geo1)
    if scheme_id:
      extra_and += " AND scheme2_id='%s'" % scheme_id
    
    cursor = connection.cursor()
    cursor.execute("""
      SELECT port_name, sum(total_subsidy) as t 
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
    
  def country_years(self, country, port=None, scheme_id=None):
    where = "WHERE year IS NOT NULL "
    if port:
      where += " AND port_name = '%s'" % re.escape(port)
    if scheme_id:
      where += " AND scheme2_id = '%s'" % scheme_id
    if country and country != "EU":
      where += "AND iso_country='%s'" % country
      
    cursor = connection.cursor()
    cursor.execute("""
      SELECT distinct(year), sum(total_subsidy) 
      FROM data_fishdata %(where)s GROUP BY year ORDER BY year ASC;  
    """ % {'country' : country, 'where' : where})
        
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0], total_subsidy=row[1])
        result_list.append(p)
    return result_list

  def country_years_traffic_lights(self, country):
    extra_and = ""
    if country == 0:
      extra_and = "AND iso_country='%s" % country

    cursor = connection.cursor()
    cursor.execute("""
      SELECT distinct(year), sum(total_subsidy), scheme_traffic_light 
      FROM data_fishdata 
      WHERE year IS NOT NULL %(extra_and)s 
      GROUP BY year, scheme_traffic_light 
      ORDER BY year ASC;  
    """ % {'extra_and' : extra_and})
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0], total_subsidy=row[1], scheme_traffic_light=row[2])
        result_list.append(p)
    return result_list
    
  def scheme_years(self, scheme_id, country='EU', year=conf.default_year):
    cursor = connection.cursor()
    extra_and = ""
    if country and country != "EU" :
      extra_and += " AND `iso_country`='%s'" % country
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year

    cursor.execute("""
      SELECT year, sum(total_subsidy), scheme_traffic_light, scheme_name, scheme2_id 
      FROM `data_fishdata` 
      WHERE scheme2_id=%(scheme_id)s %(extra_and)s 
      GROUP BY `year`
    """ % {'scheme_id' : scheme_id, 'extra_and' : extra_and})
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0], total_subsidy=row[1], scheme_traffic_light=row[2], scheme_name=row[3], scheme2_id=row[4])
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
      SELECT sum(total_subsidy) as t, scheme_traffic_light, scheme_name, scheme2_id 
      FROM `data_fishdata` WHERE scheme_name IS NOT NULL %(extra_and)s 
      GROUP BY `scheme2_id`
      ORDER BY t DESC
    """ % {'extra_and' : extra_and, 'year' : year})

    result_list = []
    for row in cursor.fetchall():
        p = self.model(total_subsidy=row[0], scheme_traffic_light=row[1], scheme_name=row[2], scheme2_id=row[3])
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
    

  def browse(self, country, sort='total_subsidy', year=conf.default_year, geo1=None):
    extra_and = ""
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += "AND iso_country='%s'" % country
    if geo1:
      extra_and += "AND geo1='%s'" % re.escape(geo1)
    
    cursor = connection.cursor()
    cursor.execute("""
            SELECT vessel_name, sum(total_subsidy) as total_subsidy, port_name, cfr, iso_country
            FROM `data_fishdata` 
            WHERE `vessel_name` IS NOT NULL %(extra_and)s 
            GROUP BY `cfr` 
            ORDER BY %(sort)s 
          """ % {'sort' : sort, 'country' : country, 'extra_and' : extra_and})
              
    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], total_subsidy=row[1], port_name=row[2], cfr=row[3], iso_country=row[4])
        result_list.append(p)
    return result_list


  def port_browse(self, country, sort='total_subsidy', year=conf.default_year):
    extra_and = ""
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += "AND iso_country='%s'" % country
    
    cursor = connection.cursor()
    cursor.execute("""
        SELECT port_name, sum(total_subsidy) as total_subsidy, port_name, cfr, iso_country
        FROM `data_fishdata` 
        WHERE `port_name` IS NOT NULL  %(extra_and)s
        GROUP BY `port_name` 
        ORDER BY %(sort)s 
      """ % {'sort' : sort, 'country' : country, 'extra_and' : extra_and})

    result_list = []
    for row in cursor.fetchall():
        p = self.model(vessel_name=row[0], total_subsidy=row[1], port_name=row[2], cfr=row[3], iso_country=row[4])
        result_list.append(p)
    return result_list
      
  def geo(self,geo=1,country="EU", sort="total_subsidy DESC", year=conf.default_year, geo1=None, scheme_id=None):
    extra_and = " AND vessel_name IS NULL AND port_name IS NULL "
    if str(year) != "0":
      extra_and += " AND year = '%s' " % year
    if country and country != "EU":
      extra_and += " AND iso_country='%s'" % country
    if geo1:
      extra_and += " AND geo1='%s'" % re.escape(geo1)
    if scheme_id:
      extra_and += " AND scheme2_id='%s'" % scheme_id
      

    cursor = connection.cursor()
    cursor.execute("""    
      SELECT geo1,geo2, sum(total_subsidy) as total_subsidy, iso_country
      FROM `data_fishdata`
      WHERE geo%(geo)s IS NOT NULL %(extra_and)s
      GROUP BY geo%(geo)s
      ORDER BY %(sort)s
      """ % {'sort' : sort, 
             'country' : country, 
             'extra_and' : extra_and, 
             'geo' : geo})
      
    result_list = []
    for row in cursor.fetchall():
        p = self.model(geo1=row[0], geo2=row[1], total_subsidy=row[2], iso_country=row[3])
        result_list.append(p)
    return result_list
      
