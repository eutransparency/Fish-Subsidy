import sys
import re

def setup(opts):
  import MySQLdb
  
  connection = MySQLdb.connect (host = "localhost",
                             user = opts.get('mysql', 'mysql_user'),
                             passwd = opts.get('mysql', 'mysql_pass'),
                              charset = 'latin1',
                             db = opts.get('mysql', 'mysql_database')
                             )
  
  return connection.cursor()

def create_or_reload(c, opts):
  
  exit = raw_input("""WARNING: This will destroy any existing data that may be 
  in the table named %s.  Do you want to continue?\n[Y/n]:""" % opts.get('mysql', 'mysql_table'))
  if len(exit) > 0 and exit[0] == "n":
    print "Exiting"
    sys.exit()
  f = open(opts.get('mysql', 'mysql_scheme'))
  sql = f.read()
  c.execute(sql)
  c.close()
  return setup(opts)

def format_sql(v):
  if v == None or v == "":
    return '\N'
    
  else:
    return "'%s'" % re.escape(v)

def index_line(c,line):
  values = []
  keys = []
  for k,v in line.items():
    # if v is not None:
    #   v = "'%s'" % v
    values.append(v)
    keys.append(k)
  keys =  ",".join("`%s`" % v for v in keys)
  values =  ",".join(format_sql(v) for v in values)
  # print values
  
  sql = "INSERT INTO `data_fishdata` (%s) VALUES (%s)" % (keys,values)
  c.execute(sql)
  
  
  
  
  
  