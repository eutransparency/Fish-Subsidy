# encoding: utf-8

import sys
import cPickle
import xapian
import unicodedata

def test():
  return "xapian"


def load_synonyms(db):
  import synonyms
  synonyms = synonyms.synonyms
  for term, synonym in synonyms.items():
    for s in synonym:
      db.add_synonym(s.lower(), term.lower())
  db.flush()

def setup(opts):
  database = xapian.WritableDatabase(opts.get('xapian', 'db_path'), xapian.DB_CREATE_OR_OPEN)
  indexer = xapian.TermGenerator()
  stemmer = xapian.Stem(opts.get('xapian',"default_stem"))
  indexer.set_database(database)
  indexer.set_stemmer(stemmer)
  indexer.set_flags(indexer.FLAG_SPELLING)
  load_synonyms(database)
  return database,indexer


def index_line(xapdb, xapindexer, line, mapping, data):
  # Set up 
  #Our Xapian document
  doc = xapian.Document()
  
  # Give the indexer the document
  xapindexer.set_document(doc)
  xapindexer.set_flags(xapindexer.FLAG_SPELLING)  
  #List of text to index
  index_text = []
  
  # Values that will be concationated to form the document ID
  docids = [data.line_num]
  for k,v in line.items():
    if k in mapping.sections():
      if v:
      
        v = unicodedata.normalize('NFKD', unicode(v)).encode('ASCII', 'ignore')
      
        if mapping.has_option(k, 'value'):
          doc.add_value(int(mapping.get(k, 'value')),"%s" % v)
      
        
        
        
        if mapping.has_option(k, 'prefix'):
          if mapping.has_option(k, 'index'):
            index_text.append(v)
            termweight = 1
            if mapping.has_option(k,'termweight'):
              termweight = int(mapping.get(k,'termweight'))
            xapindexer.index_text_without_positions(v.lower(),termweight,mapping.get(k,'prefix'))
          else:
            doc.add_term(mapping.get(k,'prefix')+v)
  
  
        # for term in doc.termlist():
        #   print term.term
  
  
  
        if mapping.has_option(k, 'docid'):
          docids.append(v)
    
  doc_data = cPickle.dumps(line)
  doc.set_data(doc_data)
  if len(docids) >=1:
    docid = "XDOCID:%s" % "-".join(str(s) for s in docids)
    doc.add_term(docid)
  else:
    raise ValueError, "Please define at least one docid"
  xapindexer.index_text_without_positions(" ".join(index_text), 1)
  xapdb.replace_document(docid,doc)