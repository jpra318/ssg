import os
import tempfile
import unittest

from gencontent import extract_title, generate_page


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_with_body(self):
        markdown = "# Hello\n\nThis is the body"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello   "), "Hello")

    def test_extract_title_not_first_line(self):
        markdown = "Some intro text\n\n# The Real Title\n\nBody"
        self.assertEqual(extract_title(markdown), "The Real Title")

    def test_extract_title_no_h1_raises(self):
        with self.assertRaises(ValueError):
            _ = extract_title("No title here")

    def test_extract_title_h2_is_not_h1(self):
        with self.assertRaises(ValueError):
            _ = extract_title("## Subtitle")


class TestGeneratePage(unittest.TestCase):
    def test_generate_page(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = os.path.join(tmpdir, "index.md")
            template_path = os.path.join(tmpdir, "template.html")
            dest_path = os.path.join(tmpdir, "index.html")

            with open(md_path, "w") as f:
                f.write("# Hello\n\nWorld")
            with open(template_path, "w") as f:
                f.write("{{ Title }}|{{ Content }}")

            generate_page("/", md_path, template_path, dest_path)

            with open(dest_path) as f:
                result = f.read()

            self.assertEqual(result, "Hello|<div><h1>Hello</h1><p>World</p></div>")

    def test_generate_page_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = os.path.join(tmpdir, "index.md")
            template_path = os.path.join(tmpdir, "template.html")
            # Parent directory does not exist yet; generate_page must create it.
            dest_path = os.path.join(tmpdir, "nested", "deep", "index.html")

            with open(md_path, "w") as f:
                f.write("# Hello\n\nWorld")
            with open(template_path, "w") as f:
                f.write("{{ Title }}|{{ Content }}")

            generate_page("/", md_path, template_path, dest_path)

            self.assertTrue(os.path.isfile(dest_path))
            with open(dest_path) as f:
                result = f.read()
            self.assertEqual(result, "Hello|<div><h1>Hello</h1><p>World</p></div>")


if __name__ == "__main__":
    unittest.main()