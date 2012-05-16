#!/usr/bin/env python
from schwa import dr

class Sentence(dr.Annotation):
  #my_field = dr.Slice('Token', serial='span')
  pass

class Token(dr.Token):
  pos = dr.Field(serial='gold_pos')

class Document(dr.Document):
  tokens    = dr.Store('Token')
  sentences = dr.Store('Sentence')

  #def token_range(self, start, finish):
    #for i in xrange(start._dr_index, finish._dr_index + 1):
      #yield self.tokens[i]


with open('eng.testa.docrep', 'rb') as f:
  reader = dr.Reader(Document)
  for doc in reader.stream(f):
    print type(doc), doc.filename, len(doc.tokens), len(doc.sentences)
    for s in doc.sentences:
      print [t.raw for t in doc.tokens[s.span]]
    print

