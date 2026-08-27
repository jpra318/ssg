import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode("p", [LeafNode(None, "This is a child node inside a parent node")])
        node2 = ParentNode("p", [LeafNode(None, "This is a child node inside a parent node")])
        self.assertEqual(node, node2)

    def test_tag(self):
        node = ParentNode("p", [LeafNode(None, "test")])
        parent_tag = "p"
        child_tag = None
        self.assertEqual(node.tag, parent_tag)
        self.assertEqual(node.children[0].tag, child_tag)

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

if __name__ == "__main__":
    unittest.main()
