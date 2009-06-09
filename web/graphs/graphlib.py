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
    traffic_lights = request.GET['traffic_lights'].split("|")
    name_value_dict = zip(years, values)

    # for year in years:
    #   name_value_dict.append((year,float(request.GET[year])))
    # # assert False

    
    figure(figsize=(5, 2), linewidth=0) # image dimensions  

    
    subplots_adjust(left=0.2)

    # add bars
    i = 0
    for key in name_value_dict:
      bar(i+0.25 , float(key[1]), 0.5,  color=format_traffic_lights(traffic_lights[i]), alpha=0.7, linewidth=0)
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
    
    gca().yaxis.set_major_locator(LinearLocator(numticks=4))
    
    for tick in gca().yaxis.get_major_ticks():
      tick = "foo"
    
    
    
    response = HttpResponse(mimetype="image/png")
    savefig(response, dpi=120)
    return response
