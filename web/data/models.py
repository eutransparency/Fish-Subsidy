from django.db import models
from django.template.defaultfilters import slugify
from django.db import connection, backend, models
from managers.FishData import *
from managers.denormalization import Denormalize
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from listmaker.models import ListItem
from hvad.models import TranslatableModel, TranslatedFields
from misc.countryCodes import country_codes

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
  scheme2_id = models.IntegerField(blank=True, null=True)
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
  total_subsidy = models.FloatField(blank=True, null=True)
    
  objects = FishDataManager()
  denormalize = Denormalize()
   
  def __unicode__(self):
    return "%s" % self.pk

  class Meta():
      # managed = False
      pass

class Recipient(models.Model):
  """
  One object per recipient, including vessels, non-vessels, and indeviduals
  """

  recipient_type = models.CharField(blank=True, max_length=100, db_index=True)
  recipient_id = models.CharField(
                                    blank=False, 
                                    max_length=255, 
                                    primary_key=True,
                                    db_index=True)
  name = models.CharField(blank=True, max_length=255, null=True)
  country = models.CharField(blank=True, max_length=100, db_index=True)
  port = models.ForeignKey('Port', null=True)
  amount = models.DecimalField(max_digits=40, decimal_places=2, null=False, default=0)
  geo1 = models.CharField(blank=True, max_length=255, null=True)
  geo2 = models.CharField(blank=True, max_length=255, null=True)
  
  objects = models.Manager()
  vessels = VesselsManager()
  nonvessels = NonVesselsManager()
  
  LIST_ENABLED = True
  list_hash_fields = ('name', 'country', 'amount')
  list_total_field = 'amount'


  def __unicode__(self):
    return u"%s (%s)" % (self.name, self.pk)

  def get_stemming_lang(self):
    return self.country
  
  @models.permalink
  def get_absolute_url(self):
      if self.recipient_type == "vessel":
          return ('vessel', [self.country, str(self.pk), slugify(self.name)]) 
      else:
          return ('nonvessel', [self.country, str(self.pk), slugify(self.name)]) 
      
class Scheme(TranslatableModel):
    scheme_id = models.IntegerField(blank=True, null=False, primary_key=True)
    total = models.DecimalField(max_digits=40, decimal_places=2, null=True, default=0)
    traffic_light = models.IntegerField(blank=True, null=True)
    
    objects = SchemeManager()
    
    translations = TranslatedFields(
        name = models.CharField(max_length=250),
    )
    
    def __unicode__(self):
        return "%s" % (self.name)

class SchemeYear(models.Model):
    scheme = models.ForeignKey(Scheme)
    year = models.IntegerField(blank=True, null=True)
    country = models.CharField(blank=True, max_length=2)
    total = models.DecimalField(max_digits=40, decimal_places=2, null=True, default=0)


class Payment(models.Model):
  """
  Generic payments.  Stores payments for vessels, non-vessels and individuals.
  """

  recipient_id = models.ForeignKey(Recipient, db_index=True)
  amount = models.DecimalField(max_digits=40, decimal_places=2, null=False, default=0)
  year = models.IntegerField(blank=True, null=True, db_index=True)
  port = models.ForeignKey('Port', null=True) # Only here as an optimization
  scheme = models.ForeignKey(Scheme)
  country = models.CharField(blank=True, max_length=4, db_index=True)
  
  def __unicode__(self):
    return u"%s (%s)" % (self.payment_id, self.amount)


class Port(models.Model):
    """
    Ports are simply a collection of recipients, rather than a 'real' object.
    
    They don't get payments, but there are recipients 'in' them who do.
    """
    name = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=4)
    total = models.DecimalField(max_digits=40, decimal_places=2, null=True, default=0)
    geo1 = models.CharField(blank=True, max_length=255)
    geo2 = models.CharField(blank=True, max_length=255)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    
    # ALTER TABLE data_port ADD COLUMN lat double precision;
    # ALTER TABLE data_port ADD COLUMN lng double precision;
    


    objects = PortManager()
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.pk)

class illegalFishing(models.Model):
  
  def __unicode__(self):
    return u"%s - %s" % (self.recipient, self.dates)

  objects = illegalFishingManager()
  
  recipient = models.ForeignKey(Recipient)
  dates = models.CharField(blank=True, max_length=255)
  sanction = models.TextField(blank=True)
  description = models.TextField(blank=True)
  skipper = models.TextField(blank=True)
  before_subsidy = models.NullBooleanField(default=False, null=True)

  def date_list(self):
      return self.dates.split(',')

class DataDownload(models.Model):
    
    public = models.BooleanField(default=True)
    filename = models.CharField(blank=True, max_length=255)
    format = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    file_path = models.CharField(blank=True, max_length=255)
    download_count = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return u"%s" % self.filename

class EffData(models.Model):
    country = models.CharField(blank=True, null=True, max_length=2)
    area1 = models.CharField(blank=True, null=True, max_length=255)
    area2 = models.CharField(blank=True, null=True, max_length=255)
    fund = models.CharField(blank=True, null=True, max_length=100)
    name = models.CharField(blank=True, null=True, max_length=255)

    axisText = models.TextField(blank=True, null=True)
    actionText = models.TextField(blank=True, null=True)
    projectDescription = models.TextField(blank=True, null=True)
    measureText = models.TextField(blank=True, null=True)
    
    amountEuAllocatedEuro = models.FloatField()
    amountEuPaymentEuro = models.FloatField()
    amountTotalAllocatedEuro = models.FloatField()
    amountTotalPaymentEuro = models.FloatField()
    yearAllocated = models.IntegerField(blank=True, null=True)
    yearPaid = models.IntegerField(blank=True, null=True, db_index=True)
    
    def format_location(self):
        fields = [
            "<a href='?query=country:\"%s\"'>%s</a>" % (self.country, unicode(country_codes(code=self.country)['name']) or ""),
            "<a href='?query=\"%s\"'>%s</a>" % (self.area1, self.area1),
            "<a href='?query=\"%s\"'>%s</a>" % (self.area2, self.area2),
        ]
        fields = [f for f in fields if f]
        return "<br />".join(fields)

    def format_description(self):
        fields = [
            (self.axisText, "axisText"),
            (self.measureText, "measureText"),
            (self.actionText, "actionText"),
            (self.projectDescription, "projectDescription"),
        ]
        fields = [f for f in fields if f[0]]
        f_list = ["<li>- <a href='?query=%s:\"%s\"'>%s</a>.</li>" % (f[1], f[0], f[0]) for f in fields]
        return "".join([f for f in f_list])





