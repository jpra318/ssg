import unittest
from markdown import extract_markdown_images, extract_markdown_links


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


if __name__ == "__main__":
    unittest.main()