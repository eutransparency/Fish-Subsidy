#!/usr/bin/env python
# encoding: utf-8

# system modules
import os
import sys
import math
import re
import string
import csv
import traceback
import codecs
import ConfigParser
import cPickle

# Custom modules
import xapian

def load_scheme(schemename, datafile=None):
  """
  Sheme files are a single csv line containing the  
  heading row with a .scheme extension.
  
  If datafile is None then it will look for a file 
  with the same name in the same dirctory as the 
  scheme file, with a .csv extension, IE:
  file.scheme and file.csv
  
  Note: file.csv shouldn't have a heading row.  
        This allows for splitting large data 
        files for one scheme file
  
  """
  schemename = os.path.abspath(schemename)
  
  # Check if the scheme file exists
  if os.path.exists(schemename):
    if datafile is None:
      basename = "".join(os.path.split(schemename).split('.')[:1])
      datafile = "%s.csv" % basename
    
    # Check if it has a matching data file
    if os.path.exists(datafile):
      
      # Return a list of field names
      fields = csv.reader(codecs.open(schemename)).next()
      return fields
    else:
      raise IOError, "Data file not found at %s" % datafile
  else:
    raise IOError, "Scheme file not found %s" % schemename


def load_data(datafile, fields, dialect=csv):
  """
  - `datafile`: path to the file to be loaded
  - `fields`:   A list of column names in the datafile.  
                Normally created from load_scheme()
  - `dialect`:  The format of the datafile.
  """
  datafile = os.path.abspath(datafile)
  
  
  import csv, codecs, cStringIO

  class SKV(csv.excel):
      # like excel, but uses semicolons
      delimiter = ";"
  csv.register_dialect("SKV", SKV)
  
  return csv.DictReader(codecs.open(datafile, 'U'), dialect=dialect, fieldnames=fields)
  


def load_mapping(filename='fields.cfg'):
  mapping = ConfigParser.ConfigParser()
  mapping.readfp(open(filename))
  return mapping
  

def index(data, scheme, mapping='fields.cfg', options={}):
  """
  - `data`:    A csv.DictReader object (normally from load_data())
  - `scheme`:  A list of column names
  - `mapping`: The mapping file.  See load_mapping() for more.
  """
  
  # General Options
  opts = ConfigParser.ConfigParser()
  opts.readfp(open('indexer.cfg'))
  
  # Mappings
  mapping = load_mapping(mapping) 
  
  # One day this will be beautiful.  For now I'll do it an ugly way. :(
  # modules = opts.options('modules')
  # modules = [ __import__('modules.%s' % module, fromlist=['modules']) for module in modules]
  # objects = [m for m in modules]

  use_xapian = False
  use_mysql = False
  if 'xapian' in opts.options('modules'):
    from modules import xapian_indexer
    use_xapian = True
  if 'mysql' in opts.options('modules'):
    from modules import mysql
    use_mysql = True
    
  if use_xapian:
    xapdb,xapindexer = xapian_indexer.setup(opts)
  
  if use_mysql:
    c = mysql.setup(opts)
    c = mysql.create_or_reload(c, opts)  
  
  # Main loop though each line of the data
  for line in data:

    for k,v in line.items():
      line[k] = unicode(v.decode('latin-1'))
    
    if options.get('test', False):
      if data.line_num >= 11:
        sys.exit()
        
    if use_mysql:
      mysql.index_line(c,line)
    # sys.exit()
    
    if use_xapian:
      xapian_indexer.index_line(xapdb, xapindexer, line, mapping, data)



if __name__ == "__main__":
  scheme = load_scheme('../data/fish.scheme')
  data = load_data('../data/fish.csv', scheme, dialect='SKV')
  options = {
    'database' : '../data/xapian.db',
    'mysql_table' : 'data_fishdata'
    }
  
  if '-t' in sys.argv:
    options['test'] = True
  
  index(data, scheme)


