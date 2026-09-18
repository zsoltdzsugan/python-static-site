import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "https://www.google.com", [], {"href": "https://www.google.com"})
        html_props = node.props_to_html()
        result = ' href="https://www.google.com"'
        self.assertEqual(html_props, result)

    def test_ne(self):
        node = HTMLNode("a", "https://www.google.com", [], {"href": "https://www.google.com", "target": "_blank"})
        html_props = node.props_to_html()
        result = ' href="https://www.google.com"'
        self.assertNotEqual(html_props, result)

    def test_no_props(self):
        node = HTMLNode("a", "https://www.google.com")
        html_props = node.props_to_html()
        self.assertEqual(html_props, "")

if __name__ == "__main__":
    unittest.main()
