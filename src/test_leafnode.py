import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "LeafNode")
        node2 = LeafNode("p", "LeafNode")
        self.assertEqual(node, node2)

    def test_tag(self):
        node = LeafNode("p", "This is a leaf node")
        node2 = LeafNode("h1", "This is a leaf node")
        self.assertNotEqual(node, node2)


    def test_value(self):
        node = LeafNode("p", "I'M BIG!!")
        node2 = LeafNode("p", "i'm small... but does it really make any difference?")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = LeafNode("a", "boot.dev", None)
        self.assertEqual(node.props_to_html(), "")

        props = {}
        node2 = LeafNode("a", "boot.dev", props)
        self.assertEqual(node2.props_to_html(), "")

        props["href"] = "https://boot.dev"
        expected = ' href="https://boot.dev"'
        node3 = LeafNode("a", "boot.dev", props)
        self.assertEqual(node3.props_to_html(), expected)

        props["target"] = "_blank"
        expected += ' target="_blank"'
        node4 = LeafNode("a", "boot.dev", props)
        self.assertEqual(node4.props_to_html(), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()
