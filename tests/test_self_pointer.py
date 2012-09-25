# vim: set ts=2 et:
import unittest

from schwa import dr

from utils import write_read


class Node(dr.Ann):
  label = dr.Field()
  parent = dr.SelfPointer()


class Doc(dr.Doc):
  nodes = dr.Store(Node)


class TestDoc(unittest.TestCase):
  def test_example(self):
    #    a
    #  b   c
    #  d  e f
    d = Doc()
    na = d.nodes.create(label='a')
    nb = d.nodes.create(label='b', parent=na)
    nc = d.nodes.create(label='c', parent=na)
    nd = d.nodes.create(label='d', parent=nb)
    ne = d.nodes.create(label='e', parent=nc)
    nf = d.nodes.create(label='f', parent=nc)

    self.assertEqual(len(d.nodes), 6)
    self.assertIsNone(na.parent)
    self.assertIs(nb.parent, na)
    self.assertIs(nc.parent, na)
    self.assertIs(nd.parent, nb)
    self.assertIs(ne.parent, nc)
    self.assertIs(nf.parent, nc)

    d = write_read(d, Doc)

    self.assertEqual(len(d.nodes), 6)
    na, nb, nc, nd, ne, nf = d.nodes
    self.assertIsNone(na.parent)
    self.assertIs(nb.parent, na)
    self.assertIs(nc.parent, na)
    self.assertIs(nd.parent, nb)
    self.assertIs(ne.parent, nc)
    self.assertIs(nf.parent, nc)
