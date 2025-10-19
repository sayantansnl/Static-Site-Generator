import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_anchor(self):
        htmlNode = HTMLNode("a", "Holy-Shit", None, {"href": "www.google.com"})
        htmlNode2 = HTMLNode("a", "Holy-Shit", None, {"href": "www.google.com"})
        self.assertEqual(htmlNode, htmlNode2)
    
    def test_eq_heading(self):
        htmlNode = HTMLNode("h1", "Zoomba")
        htmlNode2 = HTMLNode("h1", "Zoomba")
        self.assertEqual(htmlNode, htmlNode2)
    
    def test_repr_self(self):
        htmlNode = HTMLNode("p", "Text", None, {"color": "red"})
        self.assertEqual('<p color="red">Text</p>', repr(htmlNode))