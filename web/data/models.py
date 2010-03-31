from django.db import models
from django.db import connection, backend, models
import conf
from managers.FishData import FishDataManager, illegalFishingManager
from managers.denormalization import Denormalize
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from listmaker.models import ListItem

class FishData(models.Model):
  """(Data description)"""  
  
  cci = models.TextField(blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  project_no = models.TextField(blank=True, null=True)
  iso_country = models.TextField(blank=True, null=True)
  country_name = models.TextField(blank=True, null=True)
  nuts = models.TextField(blank=True, null=True)
  geo1 = models.TextField(blank=True, null=True)
  geo2 = models.TextField(blank=True, null=True)
  municipality_x_cord = models.TextField(blank=True, null=True)
  municipality_y_cord = models.TextField(blank=True, null=True)
  scheme1_id = models.TextField(blank=True, null=True)
  scheme2_id = models.TextField(blank=True, null=True)
  scheme_name = models.TextField(blank=True, null=True)
  scheme_traffic_light = models.TextField(blank=True, null=True)
  status = models.TextField(blank=True, null=True)
  status_code_status = models.TextField(blank=True, null=True)
  approval_date = models.TextField(blank=True, null=True)
  year = models.IntegerField(blank=True, null=True, db_index=True)
  total_cost = models.TextField(blank=True, null=True)
  member_state = models.TextField(blank=True, null=True)
  fifg = models.TextField(blank=True, null=True)
  vessel_name = models.TextField(blank=True, null=True)
  cfr = models.CharField(blank=True, max_length=100, db_index=True, null=True)
  cfr_link = models.TextField(blank=True, null=True)
  external_marking = models.TextField(blank=True, null=True)
  overall_length = models.TextField(blank=True, null=True)
  main_power = models.TextField(blank=True, null=True)
  tonnage = models.TextField(blank=True, null=True)
  port_name = models.TextField(blank=True, null=True)
  port_country = models.TextField(blank=True, null=True)
  source = models.TextField(blank=True, null=True)
  period = models.TextField(blank=True, null=True)
  port_lng = models.TextField(blank=True, null=True)
  port_lat = models.TextField(blank=True, null=True)
  recipient_id = models.TextField(blank=True, null=True)
  tuna_fleet = models.TextField(blank=True, null=True)
  construction_year = models.TextField(blank=True, null=True)
  construction_place = models.TextField(blank=True, null=True)
  recipient_name = models.TextField(blank=True, null=True)
  greenpeace_link = models.TextField(blank=True, null=True)
  lenght_code = models.TextField(blank=True, null=True)
  total_subsidy = models.TextField(blank=True, null=True)
    
  objects = FishDataManager()
  denormalize = Denormalize()
   
  def __unicode__(self):
    return "%s" % self.pk


class Recipient(models.Model):
  """
  One object per recipient, including vessels, non-vessels, and indeviduals
  """
  recipient_id = models.CharField(blank=False, max_length=255, primary_key=True)
  name = models.CharField(blank=True, max_length=255)
  country = models.CharField(blank=True, max_length=100, db_index=True)
  port = models.CharField(blank=True, null=True, max_length=255)
  amount = models.FloatField(db_index=True, null=True, default=0)
  
  LIST_ENABLED = True

  def __unicode__(self):
    return u"%s" % self.name

class Scheme(models.Model):
    scheme_id = models.IntegerField(blank=True, null=True, db_index=True)
    name = models.CharField(blank=True, max_length=255, db_index=True)
    total = models.FloatField(null=True, default=0)
    year = models.IntegerField(blank=True, null=True)
    traffic_light = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.year,)

class Payment(models.Model):
  """
  Generic payments.  Stores payments for vessels, non-vessels and individuals.
  """
  payment_id = models.IntegerField(primary_key=True)
  recipient_id = models.ForeignKey(Recipient)
  amount = models.FloatField()
  year = models.IntegerField(blank=True, null=True, db_index=True)
  scheme = models.ForeignKey(Scheme)
  country = models.CharField(blank=True, max_length=4, db_index=True)
  
  def __unicode__(self):
    return u"%s (%s)" % (self.payment_id, self.amount)

class illegalFishing(models.Model):
  
  def __unicode__(self):
    return "%s" % self.cfr

  objects = illegalFishingManager()
  
  cfr = models.CharField(blank=True, max_length=100)
  date = models.DateField(blank=True, null=True)
  sanction = models.TextField(blank=True)
  description = models.TextField(blank=True)
  skipper = models.TextField(blank=True)


class DataDownload(models.Model):
    
    public = models.BooleanField(default=True)
    filename = models.CharField(blank=True, max_length=255)
    format = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    file_path = models.CharField(blank=True, max_length=255)
    download_count = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return u"%s" % self.filename
