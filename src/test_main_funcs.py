import unittest

from main import text_node_to_html_node,split_nodes,extract_markdown_links,extract_markdown_images
from htmlnode import HTMLNode,LeafNode,ParentNode
from textnode import TextNode

class TestMainFuncs(unittest.TestCase):
    def test_convert_text(self):
        txt_node=TextNode("This is a text node", "text", "https://www.boot.dev")
        html=text_node_to_html_node(txt_node).to_html()
        self.assertTrue(html=="This is a text node")
    def test_convert_bold(self):
        txt_node=TextNode("This is a text node", "bold", "https://www.boot.dev")
        html=text_node_to_html_node(txt_node).to_html()
        self.assertTrue(html=="<b>This is a text node</b>")
    def test_convert_italic(self):
        txt_node=TextNode("This is a text node", "italic", "https://www.boot.dev")
        html=text_node_to_html_node(txt_node).to_html()
        self.assertTrue(html=="<i>This is a text node</i>")
    def test_convert_code(self):
        txt_node=TextNode("This is a text node", "code", "https://www.boot.dev")
        html=text_node_to_html_node(txt_node).to_html()
        self.assertTrue(html=="<code>This is a text node</code>")
    def test_convert_link(self):
        txt_node=TextNode("This is a text node", "link", "https://www.boot.dev")
        html=text_node_to_html_node(txt_node).to_html()
        self.assertTrue(html=='<a href="https://www.boot.dev">This is a text node</a>')
    def test_convert_image(self):
        txt_node=TextNode("This is a text node", "image", "https://www.boot.dev")
        html=text_node_to_html_node(txt_node).to_html()
        self.assertTrue(html=='<img src="https://www.boot.dev" alt="This is a text node"></img>')
    def test_invalid_type(self):
        txt_node=TextNode("This is a text node", "imag", "https://www.boot.dev")
        correct=False
        try:
            html=text_node_to_html_node(txt_node).to_html()
        except Exception as e:
            if str(e)==f"invalid type for text node {txt_node.text_type}":
                correct=True
        self.assertTrue(correct)

    # split nodes testing
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", "text")
        new_nodes = split_nodes(node)
        # print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word", "text"),
            ],
            new_nodes,
        )
    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", "text"
        )
        new_nodes = split_nodes(node)
        # print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word and ", "text"),
                TextNode("another", "bold"),
            ],
            new_nodes,
        )
    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", "text")
        new_nodes = split_nodes(node)
        # print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word", "text"),
            ],
            new_nodes,
        )
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", "text")
        new_nodes = split_nodes(node)
        # print(new_nodes)
        self.assertListEqual(
            [
                TextNode("bold", "bold"),
                TextNode(" and ", "text"),
                TextNode("italic", "italic"),
            ],
            new_nodes,
        )
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes(node)
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ],
            new_nodes,
        )
        #extract images and links
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

if __name__ == "__main__":
    unittest.main()