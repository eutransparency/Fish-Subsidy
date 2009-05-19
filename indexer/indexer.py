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
  Sheme files are csv files with a .scheme extension.  
  
  If datafile is None then it will look for a file 
  with the same name in the same dirctory as the 
  scheme file, with a .csv extension, IE:
  file.scheme and file.csv
  
  """
  schemename = os.path.abspath(schemename)
  
  # Check if the scheme file exists
  if os.path.exists(schemename):
    if datafile is None:
      basename = "".join(schemename.split('.')[:1])
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


def load_data(datafile, fields):
  datafile = os.path.abspath(datafile)
  
  class SKV(csv.excel):
      # like excel, but uses semicolons
      delimiter = ";"

  csv.register_dialect("SKV", SKV)
  
  
  return csv.DictReader(codecs.open(datafile, 'U'), dialect="SKV", fieldnames=fields)  


def index(data, scheme, mapping='mapping.cfg', options={}):
  """
  
  Options:
    - database: the database path
    - stem: stemming language
    - mappingfile: path to the field mapping file
  
  """

  # General Options
  opts = ConfigParser.ConfigParser()
  opts.readfp(open(options.get('optionsfile', 'indexer.cfg')))  
  
  # Index in to Mysql as well as xapian
  if opts.getboolean('general', 'mysql') == True:
    import MySQLdb
    
    connection = MySQLdb.connect (host = "localhost",
                               user = opts.get('mysql', 'mysql_user'),
                               passwd = opts.get('mysql', 'mysql_pass'),
                               charset = 'latin1',
                               db = opts.get('mysql', 'mysql_database')
                               )
    
    c = connection.cursor()
    create_sql = open(os.path.abspath(opts.get('mysql', 'mysql_scheme')))
    c.execute(create_sql.read())
    c.close()
    c = connection.cursor()
    


    
  
  # Xapian Stuff
  database = xapian.WritableDatabase(options.get('database', 'xapian.db'), xapian.DB_CREATE_OR_OPEN)
  indexer = xapian.TermGenerator()
  stemmer = xapian.Stem(options.get('stem',"english"))
  indexer.set_stemmer(stemmer)
  indexer.set_database(database)
  indexer.set_flags(indexer.FLAG_SPELLING)
  
  # Mapping Stuff
  mapping = ConfigParser.ConfigParser()
  mapping.readfp(open(options.get('mappingfile', 'fields.cfg')))

  
  # Main loop though each line of the data
  for line in data:    
    if options.get('test', False):
      if data.line_num >= 11:
        sys.exit()
        
    if opts.getboolean('general', 'mysql') == True:
      values = []
      keys = []
      for k,v in line.items():
        if v is None:
          v = ""
        values.append(v)
        keys.append(k)
      keys =  ",".join("`%s`" % v for v in keys)
      values =  ",".join("'%s'" % re.escape(v) for v in values)


      sql = "INSERT INTO `data_fishdata` (%s) VALUES (%s)" % (keys,values)
      # sql = "%s" % str(values)
      # print sql
      c.execute(sql)
      # sys.exit()
            
    
    # Set up 
    #Our Xapian document
    doc = xapian.Document()
    
    # Give the indexer the document
    indexer.set_document(doc)
    
    #List of text to index
    index_text = []
    
    # Values that will be concationated to form the document ID
    docids = [data.line_num]
    
    for k,v in line.items():
      if k in mapping.sections():
        
        if mapping.has_option(k, 'debug_print'):
          print v

        if mapping.has_option(k, 'index'):
          if v:
            index_text.append(v)
    
        if mapping.has_option(k, 'docid'):
          docids.append(v)
    


    doc_data = cPickle.dumps(line)
    doc.set_data(doc_data)
    if len(docids) >=1:
      docid = "XDOCID%s" % "-".join(str(s) for s in docids)
      doc.add_term(docid)
    else:
      raise ValueError, "Please define at least one docid"
    indexer.index_text(" ".join(index_text))
    database.replace_document(docid,doc)




if __name__ == "__main__":
  # print index()
  scheme = load_scheme('../data/fish.scheme')
  data = load_data('../data/fish.csv', scheme)
  options = {
    'database' : '../data/xapian.db',
    'mysql_table' : 'data_fishdata'
    }
  
  if '-t' in sys.argv:
    options['test'] = True
  
  index(data, scheme, options=options)


