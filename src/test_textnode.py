import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is another text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.CODE)
        node5 = TextNode("This is a text node", TextType.LINK)
        node6 = TextNode("This is a text node", TextType.IMAGE)

        self.assertNotEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node5, node6)

    def test_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
