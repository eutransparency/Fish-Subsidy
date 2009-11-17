from django.db import models
from django.db import connection, backend, models
import conf
from managers.FishData import FishDataManager

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
  cfr = models.CharField(blank=True, max_length=100)
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
  total_subsidy = models.TextField(blank=True)
    
  objects = FishDataManager()
   
  def __unicode__(self):
    return "%s" % self.pk


class illegalFishing(models.Model):
  
  def __unicode__(self):
    return "%s" % self.cfr
  
  cfr = models.CharField(blank=True, max_length=100)
  date = models.DateField(blank=True, null=True)
  sanction = models.TextField(blank=True)
  description = models.TextField(blank=True)
  skipper = models.TextField(blank=True)






    