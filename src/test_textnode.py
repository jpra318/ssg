import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is an italic text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("print('Hello World!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello World!')")

    def test_link(self):
        node = TextNode("Clicky to git gud!", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        expected = '<a href="https://boot.dev">Clicky to git gud!</a>'
        self.assertEqual(html_node.to_html(), expected)

    def test_image(self):
        node = TextNode("Image test", TextType.IMAGE, "test.jpg")
        html_node = text_node_to_html_node(node)
        expected = '<img src="test.jpg" alt="Image test"></img>'
        self.assertEqual(html_node.to_html(), expected)

    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("This is text with a **bold** word", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        old_nodes = [TextNode("This is text with an _italic_ word", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_code(self):
        old_nodes = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_unclosed(self):
        old_nodes = [TextNode("unclosed **bold", TextType.TEXT)]
        with self.assertRaises(ValueError):
            _ = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_split_nodes_delimiter_non_text_passthrough(self):
        old_nodes = [TextNode("already bold", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(new_nodes, old_nodes)

    def test_split_nodes_delimiter_at_edges(self):
        old_nodes = [TextNode("**bold** word", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_multiple_pairs(self):
        old_nodes = [TextNode("**one**and **two**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("one", TextType.BOLD),
                TextNode("and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
        )

    def test_split_nodes_delimiter_multiple_nodes(self):
        old_nodes = [
            TextNode("**one**", TextType.TEXT),
            TextNode("plain", TextType.TEXT),
            TextNode("**two**", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("one", TextType.BOLD),
                TextNode("plain", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
        )

    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [TextNode("no delimiter here", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [TextNode("no delimiter here", TextType.TEXT)],
        )

if __name__ == "__main__":
    unittest.main()
