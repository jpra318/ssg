import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


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

    def test_split_nodes_image(self):
        old_nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_nodes_image_at_start(self):
        old_nodes = [TextNode("![image](https://example.com/img.png) rest of text", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" rest of text", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_at_end(self):
        old_nodes = [TextNode("text before ![image](https://example.com/img.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
        )

    def test_split_nodes_image_multiple(self):
        old_nodes = [TextNode("![first](https://example.com/1.png) and ![second](https://example.com/2.png) end", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("first", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "https://example.com/2.png"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_no_images(self):
        old_nodes = [TextNode("This is plain text with no images", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            new_nodes,
            [TextNode("This is plain text with no images", TextType.TEXT)],
        )

    def test_split_nodes_image_non_text_passthrough(self):
        old_nodes = [TextNode("already bold", TextType.BOLD)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(new_nodes, old_nodes)

    def test_split_nodes_image_multiple_nodes(self):
        old_nodes = [
            TextNode("![one](https://example.com/1.png)", TextType.TEXT),
            TextNode("plain", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("plain", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
            ],
        )

    def test_split_nodes_image_empty_alt(self):
        old_nodes = [TextNode("![](https://example.com/img.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            new_nodes,
            [TextNode("", TextType.IMAGE, "https://example.com/img.png")],
        )

    def test_split_nodes_link(self):
        old_nodes = [TextNode("This is text with a [link](https://boot.dev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_split_nodes_link_at_start(self):
        old_nodes = [TextNode("[link](https://boot.dev) rest of text", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" rest of text", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_at_end(self):
        old_nodes = [TextNode("text before [link](https://boot.dev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_split_nodes_link_multiple(self):
        old_nodes = [TextNode("[one](https://example.com/1) and [two](https://example.com/2) end", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("one", TextType.LINK, "https://example.com/1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://example.com/2"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_no_links(self):
        old_nodes = [TextNode("This is plain text with no links", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            new_nodes,
            [TextNode("This is plain text with no links", TextType.TEXT)],
        )

    def test_split_nodes_link_non_text_passthrough(self):
        old_nodes = [TextNode("already italic", TextType.ITALIC)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(new_nodes, old_nodes)

    def test_split_nodes_link_multiple_nodes(self):
        old_nodes = [
            TextNode("[one](https://example.com/1)", TextType.TEXT),
            TextNode("plain", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("one", TextType.LINK, "https://example.com/1"),
                TextNode("plain", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
            ],
        )

    def test_split_nodes_link_empty_text(self):
        old_nodes = [TextNode("[](https://boot.dev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            new_nodes,
            [TextNode("", TextType.LINK, "https://boot.dev")],
        )

    def test_text_to_textnodes_plain(self):
        nodes = text_to_textnodes("This is plain text")
        self.assertListEqual(
            nodes,
            [TextNode("This is plain text", TextType.TEXT)],
        )

    def test_text_to_textnodes_bold(self):
        nodes = text_to_textnodes("This is **bold** text")
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_italic(self):
        nodes = text_to_textnodes("This is _italic_ text")
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_code(self):
        nodes = text_to_textnodes("This is `code` text")
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_image(self):
        nodes = text_to_textnodes("This is an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual(
            nodes,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_text_to_textnodes_link(self):
        nodes = text_to_textnodes("This is a [link](https://boot.dev)")
        self.assertListEqual(
            nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes_combined(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ wordand a `code block`chend an ![image](https://i.imgur.com/zjjcJKZ.png)chend a [link](https://boot.dev)"
        )
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" wordand a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode("chend an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("chend a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes_empty(self):
        nodes = text_to_textnodes("")
        self.assertListEqual(nodes, [])

if __name__ == "__main__":
    unittest.main()
