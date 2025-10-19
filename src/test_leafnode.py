import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_raw_text(self):
        node = LeafNode(None, "Python is slow")
        self.assertEqual(node.to_html(), "Python is slow")
    
    def test_error(self):
        node = LeafNode("h2", None)
        with self.assertRaises(ValueError):
            node.to_html()