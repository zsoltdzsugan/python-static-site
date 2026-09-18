import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_with_no_url(self):
        node = TextNode("This is a link url=none node", TextType.LINK)
        self.assertIsNone(node.url)

    def test_with_url(self):
        node = TextNode("This is a link url is not none node", TextType.LINK, "http://url.com")
        self.assertIsNotNone(node.url)

if __name__ == "__main__":
    unittest.main()
