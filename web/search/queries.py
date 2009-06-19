import sys
from fishsubsidy import conf
import cPickle
import unicodedata
import xapian
import ConfigParser
from fishsubsidy import conf

def load_database(db=conf.xapianDbPath):
  """Returns a xapian.Database object
  - `db` full path to a xapian database
  """
  
  db = xapian.Database(db)
  return db


def load_enquire(db):
  """returns a xapian.Enquire opject
  - `db` a xapian.Database object
  """

  enquire = xapian.Enquire(db)
  return enquire

def load_fields(mapfile='indexer/fields.cfg'):
  opts = ConfigParser.ConfigParser()
  opts.readfp(open(conf.paths['project_path'] + mapfile))
  return opts
  

def load_queryparser():
  """Creates a xapian.queryparser object and creates the default term prefixes and value range searchers."""

  qp = xapian.QueryParser()
  stemmer = xapian.Stem("english")
  qp.set_stemmer(stemmer)
  field_mappings = load_fields()

  qp.set_default_op(xapian.Query.OP_AND)
  valueranges = []  

  for field in field_mappings.sections():
    f = field_mappings.options(field)
    # print f
    if 'value_range_search' in f and 'value' in f:
      vrp = xapian.NumberValueRangeProcessor(f['value'],f['value_range_prefix'])
      valueranges.append(vrp)
      qp.add_valuerangeprocessor(vrp) 

    if 'prefix' in f and 'name' in f:
      # if 'boolean' in f:
      #   qp.add_boolean_prefix(field['name'], field['prefix'])
      # else:
      qp.add_prefix(field_mappings.get(field,'name'), field_mappings.get(field,'prefix'))

  return (qp,valueranges)


# def search_ports(query):
#   query_string = unicodedata.normalize('NFKD', unicode(query)).encode('ASCII', 'ignore')
#   (qp,valueranges) = load_queryparser()
#   db = load_database()
#   qp.set_database(db)
#   qp.set_default_op(xapian.Query.OP_OR)
#   DEFAULT_SEARCH_FLAGS = (
#          xapian.QueryParser.FLAG_BOOLEAN |
#          xapian.QueryParser.FLAG_PHRASE |
#          xapian.QueryParser.FLAG_LOVEHATE |   
#          xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE |
#          xapian.QueryParser.FLAG_WILDCARD |
#          xapian.QueryParser.FLAG_SPELLING_CORRECTION
#          # xapian.QueryParser.FLAG_PARTIAL 
#          )
#   query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS, 'port:')
#   enq = load_enquire(db)
#   enq.set_collapse_key(1)
#   enq.set_query(query)
#   matches = enq.get_mset(0, 10)
#   results = {}
#   results['description'] = "Parsed query is: %s" % query.get_description()
#   results['size'] = matches.get_matches_estimated()
#   results['documents'] = {}
#   for k,m in enumerate(matches):
#     results['documents'][k] = dict(cPickle.loads(m.document.get_data()))
#     results['documents'][k]['doc_id'] = m.document.get_docid()
#   return results
# 
# 
def search(query, options={}):
  query_string = query
  (qp,valueranges) = load_queryparser()
  db = load_database()
  qp.set_database(db)
  stemmer = xapian.Stem("en")
  qp.set_stemming_strategy(qp.STEM_SOME)
  qp.set_stemmer(stemmer)

  
  qp.set_default_op(xapian.Query.OP_OR)
  DEFAULT_SEARCH_FLAGS = (
         xapian.QueryParser.FLAG_BOOLEAN |
         xapian.QueryParser.FLAG_PHRASE |
         xapian.QueryParser.FLAG_LOVEHATE |
         xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE |
         xapian.QueryParser.FLAG_WILDCARD |
         xapian.QueryParser.FLAG_SPELLING_CORRECTION |
         xapian.QueryParser.FLAG_SYNONYM |
         xapian.QueryParser.FLAG_AUTO_SYNONYMS
         )
  
  if 'prefix' in options:
    query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS, options['prefix'])
  else:
    query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS)
  
  enq = load_enquire(db)
  
  if 'collapse' in options:
    enq.set_collapse_key(options['collapse'])
    
  enq.set_query(query)
  
  matches = enq.get_mset(0, 10)
  
  results = {}
  results['description'] = "Parsed query is: %s" % query.get_description()
  results['documents'] = {}
  results['size'] = matches.get_matches_estimated()
  results['spelling'] = qp.get_corrected_query_string()
  
  for k,m in enumerate(matches):
    results['documents'][k] = dict(cPickle.loads(m.document.get_data()))
    results['documents'][k]['doc_id'] = m.document.get_docid()
  return results
  

def list_spellings():
  db = load_database()
  for spelling in db.spellings():
    if spelling.term[0] == "l":
      print spelling.term

def list_synonyms():
  db = load_database()
  for synonym in db.synonyms('country:uk'):
    print synonym

  
if __name__ == "__main__":
  # list_spellings()
  list_synonyms()
  # results =  search('%s' % " ".join(sys.argv[1:]), 'country:')
  # print results['description']
  # for i,result in results['documents'].items():
  #   print result['iso_country']