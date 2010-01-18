#!/usr/bin/env python
# encoding: utf-8


"""
This indexer only deals with *importing* data from a preformatted CSV file.

If does not deal with creating the database tables, as django will do this for us.

"""

import os
import sys
from datetime import datetime
import csv
import codecs
import MySQLdb
from optparse import OptionParser
import ConfigParser


class database(object):
  
  def __init__(self, options):
    
    # ConfigParser, to read from indexer.cfg
    conf = ConfigParser.ConfigParser()
    conf.readfp(open('indexer.cfg'))
    
    csvfile = options.filename or conf.get('illegaldata', 'filename')
    self.csvfile = "../data/" + csvfile
    
    self.table_name = conf.get('illegaldata', 'mysql_illegal_table')
    
    self.connection = MySQLdb.connect (host = "localhost",
                               user = conf.get('mysql', 'mysql_user'),
                               passwd = conf.get('mysql', 'mysql_pass'),
                               charset = 'latin1',
                               db = conf.get('mysql', 'mysql_database')
                               )

    self.cursor = self.connection.cursor()
    
    
  def index(self):
    
    reader = csv.DictReader(codecs.open(self.csvfile, 'U'))
    for line in reader:
      if line['cfr']:
        line['table_name'] = self.table_name.strip()
        try:
          line['date'] = datetime.strptime(line['date'], "%d/%m/%y")
        except:
          line['date'] = None
        self.cursor.execute("""
        INSERT INTO data_illegalfishing (cfr,date,sanction,description,skipper)
        VALUES (%(cfr)s,%(date)s,%(sanction)s,%(description)s,%(skipper)s)
        """, line)
  
  def reset(self):
      self.cursor.execute("DELETE FROM %s" % self.table_name)

def main():
  
  # OptParser for command line arguments
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="filename",
                    help="File to import from", metavar="filename")
  parser.add_option("-a", "--append", dest="append", action="store_true", default=False,
                    help="Append data to existing data (don't reset)", metavar="append")

  (options, args) = parser.parse_args()
  
  
  db = database(options)
  if not options.append:
      db.reset()
  db.index()


if __name__ == "__main__":
  main()