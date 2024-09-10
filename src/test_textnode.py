import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    def test_neq_text(self):
        node = TextNode("This is a text ", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)
    def test_neq_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bod")
        self.assertNotEqual(node, node2)
    def test_url_none(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(None, node.url)
    def test_url_not_none(self):
        node = TextNode("This is a text node", "bold","https://www.boot.dev")
        self.assertNotEqual(None, node.url)
        


if __name__ == "__main__":
    unittest.main()