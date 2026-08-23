import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "HTMLNode")
        node2 = HTMLNode("p", "HTMLNode")
        self.assertEqual(node, node2)

    def test_tag(self):
        node = HTMLNode("p", "This is an HTML node")
        node2 = HTMLNode("h1", "This is an HTML node")
        self.assertNotEqual(node, node2)


    def test_value(self):
        node = HTMLNode("h1", "I'M BIG!!")
        node2 = HTMLNode("h1", "im small... but same size as the big guy!")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("a", "boot.dev", None, None)
        self.assertEqual(node.props_to_html(), "")

        props = {}
        node2 = HTMLNode("a", "boot.dev", None, props)
        self.assertEqual(node2.props_to_html(), "")

        props["href"] = "https://boot.dev"
        expected = ' href="https://boot.dev"'
        node3 = HTMLNode("a", "boot.dev", None, props)
        self.assertEqual(node3.props_to_html(), expected)

        props["target"] = "_blank"
        expected += ' target="_blank"'
        node4 = HTMLNode("a", "boot.dev", None, props)
        self.assertEqual(node4.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()
