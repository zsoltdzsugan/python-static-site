import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><span>child</span></div>',
        )

    def test_to_html_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_nested_parents(self):
        deep = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "one")]),
                        ParentNode("li", [LeafNode(None, "two")]),
                    ],
                )
            ],
        )
        self.assertEqual(
            deep.to_html(),
            "<div><ul><li>one</li><li>two</li></ul></div>",
        )

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "x")])
        with self.assertRaises(ValueError) as ctx:
            node.to_html()
        self.assertIn("tag", str(ctx.exception).lower())

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as ctx:
            node.to_html()
        self.assertIn("children", str(ctx.exception).lower())

    def test_parent_in_parent(self):
        inner = ParentNode("span", [LeafNode(None, "inner")])
        outer = ParentNode("div", [inner])
        self.assertEqual(outer.to_html(), "<div><span>inner</span></div>")

if __name__ == "__main__":
    unittest.main()
