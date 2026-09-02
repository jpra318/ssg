import unittest
from markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "![first](https://example.com/1.png) and ![second](https://example.com/2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("first", "https://example.com/1.png"),
                ("second", "https://example.com/2.png"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is plain text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/img.png)")
        self.assertListEqual([("", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_empty_url(self):
        matches = extract_markdown_images("![alt]()")
        self.assertListEqual([("alt", "")], matches)

    def test_extract_markdown_images_mixed(self):
        text = "![image](https://example.com/img.png) and [link](https://boot.dev)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_ignores_links(self):
        matches = extract_markdown_images("This is a [link](https://boot.dev)")
        self.assertListEqual([], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev)")
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "This has [one](https://example.com/1) and [two](https://example.com/2)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("one", "https://example.com/1"),
                ("two", "https://example.com/2"),
            ],
            matches,
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is plain text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_text(self):
        matches = extract_markdown_links("[](https://boot.dev)")
        self.assertListEqual([("", "https://boot.dev")], matches)

    def test_extract_markdown_links_empty_url(self):
        matches = extract_markdown_links("[text]()")
        self.assertListEqual([("text", "")], matches)

    def test_extract_markdown_links_mixed(self):
        text = "![image](https://example.com/img.png) and [link](https://boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links("This is an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single(self):
        blocks = markdown_to_blocks("Just one paragraph")
        self.assertEqual(blocks, ["Just one paragraph"])

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = "\n\n  First paragraph  \n\nSecond paragraph\n\n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_markdown_to_blocks_blank_lines_with_whitespace(self):
        md = "First\n   \n\nSecond"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First", "Second"])

    def test_markdown_to_blocks_multiple_blank_lines(self):
        md = "First\n\n\n\nSecond"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First", "Second"])

    def test_markdown_to_blocks_empty(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace_only(self):
        blocks = markdown_to_blocks("   \n\n  ")
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_blank_line_with_tabs(self):
        md = "First\n\t\n\t\nSecond"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First", "Second"])

    def test_markdown_to_blocks_no_trailing_newline(self):
        md = "First\n\nSecond"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First", "Second"])

    def test_markdown_to_blocks_whitespace_inside_block(self):
        md = "First line\n   indented  \n\nSecond"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First line\n   indented", "Second"])

if __name__ == "__main__":
    unittest.main()
