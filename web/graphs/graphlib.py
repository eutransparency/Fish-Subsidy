# !/usr/bin/env python
# encoding: utf-8

import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # force the antigrain backend
from matplotlib import rc
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.cbook import iterable
import matplotlib.numerix as nx
from pylab import *
from django.http import HttpResponse
from pylab import figure, show, rand
from matplotlib.patches import Ellipse
import locale
locale.setlocale(locale.LC_ALL, '')

 
def format_ticks(a,b):
  return u"€%s" % locale.format('%d', float(a), True)

def format_traffic_lights(t):
  t = str(t)
  if t == "3":
    return '#FF0000'
  if t == "2":
    return '#FF9900'
  if t == "1":
    return '#339900'

def make_fig(request, type):
    """ make a chart """
    name_value_dict = {}
    
    years = request.GET['years'].split("|")
    values = request.GET['values'].split("|")
    if 'traffic_lights' in request.GET:
      traffic_lights = request.GET['traffic_lights'].split("|")
    else:
      traffic_lights = None
    name_value_dict = zip(years, values)

    figure(figsize=(5, 2), linewidth=0) # image dimensions  

    subplots_adjust(left=0.2)

    # add bars
    i = 0
    for key in name_value_dict:
      if traffic_lights:
        bar(i+0.25 , float(key[1]), 0.5,  color=format_traffic_lights(traffic_lights[i]), alpha=0.7, linewidth=0)
      else:
        bar(i+0.25 , float(key[1]), 0.5,  color='grey', alpha=0.7, linewidth=0)
      i = i+1
    # assert False      

    # axis setup
    xticks(arange(0.5, len(name_value_dict)),
        [('%s' % value[0]) 
        for value in name_value_dict],
        size='xx-small')
    max_value = max([float(v[1]) for v in name_value_dict])
    
    
    yticks(size='xx-small')

    formatter = FuncFormatter(format_ticks)
    
    gca().yaxis.set_major_formatter(formatter)
    
    # gca().yaxis.set_major_locator(LinearLocator(numticks=5))
    gca().yaxis.set_major_locator(MaxNLocator(nbins=3, symmetric=True))
    
    for tick in gca().yaxis.get_major_ticks():
      tick = "foo"
    
    
    
    response = HttpResponse(mimetype="image/png")
    savefig(response, dpi=120)
    return response
    
def stack_graph(request,country='GB'):
  
  from fishsubsidy.web.data.models import FishData
  sql_data = FishData.objects.country_years_traffic_lights(country)
  data = []
  good = {}
  bad = {}
  ugly = {}
  years = []
  
  for o in sql_data:
    if o.year not in good:
      good[o.year] = 0
    if o.year not in bad:
      bad[o.year] = 0
    if o.year not in ugly:  
      ugly[o.year] = 0
      
    if o.scheme_traffic_light == "1":
      good[o.year] += o.total_cost
      bad[o.year] += 0
      ugly[o.year] += 0
    if o.scheme_traffic_light == "2":
      ugly[o.year] += o.total_cost
      bad[o.year] += 0
      good[o.year] += 0
      
    if o.scheme_traffic_light == "3":
      bad[o.year] += o.total_cost
      good[o.year] += 0
      ugly[o.year] += 0
      
    
    if o.year not in years:
      years.append(o.year)
      
  data.append([v for k,v in good.items()])
  data.append([v for k,v in ugly.items()])
  data.append([v for k,v in bad.items()])
    
  figure(figsize=(5, 2), linewidth=0) # image dimensions  
  subplots_adjust(left=0.2, bottom=0.2)
  
  colLabels = [y for y in years]
  ind = arange(len(colLabels)) + 0.3
  yoff = array([0.0] * len(colLabels))

  rows = len(data)

  for row in xrange(rows):
    bar(ind, data[row], 0.4, bottom=yoff, color=format_traffic_lights(row+1), linewidth=0,)
    yoff = yoff + data[row]

  xticks(arange(0.5, len(years)),
      [('%s' % value) 
      for value in years],
      size='xx-small', rotation=45)
  yticks(size='xx-small')
  formatter = FuncFormatter(format_ticks)
  
  gca().yaxis.set_major_formatter(formatter)
  
  gca().yaxis.set_major_locator(LinearLocator(numticks=5))

   
  response = HttpResponse(mimetype="image/png")
  savefig(response, dpi=120)
  return response









