import unittest

from htmlnode import HTMLNode,LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_none_init(self):
        node = HTMLNode()
        ans=True & (node.tag==None) & (node.value==None) & (node.children==None) & (node.props==None)
        self.assertTrue(ans)
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertTrue(node.props_to_html()=="")
    def test_props_to_html(self):
        node = HTMLNode(props={"href":"https://www.google.com", "target": "_blank"})
        self.assertTrue(node.props_to_html()==' href="https://www.google.com" target="_blank"')
    # leaf node test below
    def test_leaf_to_html(self):
        node1 = LeafNode("p","This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html1=node1.to_html()
        html2=node2.to_html()
        self.assertTrue(html1+html2=='<p>This is a paragraph of text.</p><a href="https://www.google.com">Click me!</a>')

    

        


if __name__ == "__main__":
    unittest.main()