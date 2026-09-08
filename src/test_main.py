import os
import tempfile
import unittest

from main import copy_static, generate_pages_recursive


class TestGeneratePagesRecursive(unittest.TestCase):
    def test_generate_pages_recursive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = os.path.join(tmpdir, "content")
            dest_dir = os.path.join(tmpdir, "public")
            template_path = os.path.join(tmpdir, "template.html")

            os.mkdir(content_dir)
            os.mkdir(os.path.join(content_dir, "blog"))
            os.mkdir(dest_dir)

            with open(template_path, "w") as f:
                f.write("<title>{{ Title }}</title>\n<body>{{ Content }}</body>")

            with open(os.path.join(content_dir, "index.md"), "w") as f:
                f.write("# Home\n\nWelcome home")
            with open(os.path.join(content_dir, "blog", "first.md"), "w") as f:
                f.write("# First Post\n\nHello")
            with open(os.path.join(content_dir, "blog", "second.md"), "w") as f:
                f.write("# Second Post\n\nWorld")
            with open(os.path.join(content_dir, "notes.txt"), "w") as f:
                f.write("not markdown")

            generate_pages_recursive("/", content_dir, template_path, dest_dir)

            # Top-level markdown becomes an HTML page.
            self.assertTrue(os.path.isfile(os.path.join(dest_dir, "index.html")))
            # Nested markdown mirrors the directory structure.
            self.assertTrue(os.path.isfile(os.path.join(dest_dir, "blog", "first.html")))
            self.assertTrue(os.path.isfile(os.path.join(dest_dir, "blog", "second.html")))
            # Non-markdown files are not converted to HTML.
            self.assertFalse(os.path.isfile(os.path.join(dest_dir, "notes.html")))

            with open(os.path.join(dest_dir, "index.html")) as f:
                index_content = f.read()
            self.assertIn("<title>Home</title>", index_content)

            with open(os.path.join(dest_dir, "blog", "first.html")) as f:
                first_content = f.read()
            self.assertIn("<title>First Post</title>", first_content)


class TestCopyStatic(unittest.TestCase):
    def test_copy_static(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = os.path.join(tmpdir, "src")
            dest_dir = os.path.join(tmpdir, "dest")

            os.makedirs(os.path.join(src_dir, "images"))
            with open(os.path.join(src_dir, "index.css"), "w") as f:
                f.write("body {}")
            with open(os.path.join(src_dir, "images", "pic.png"), "w") as f:
                f.write("png-bytes")

            copy_static(src_dir, dest_dir)

            self.assertTrue(os.path.isfile(os.path.join(dest_dir, "index.css")))
            self.assertTrue(os.path.isfile(os.path.join(dest_dir, "images", "pic.png")))

            with open(os.path.join(dest_dir, "index.css")) as f:
                self.assertEqual(f.read(), "body {}")

    def test_copy_static_overwrites_existing_dest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = os.path.join(tmpdir, "src")
            dest_dir = os.path.join(tmpdir, "dest")

            os.makedirs(src_dir)
            with open(os.path.join(src_dir, "a.txt"), "w") as f:
                f.write("a")

            copy_static(src_dir, dest_dir)
            self.assertTrue(os.path.isfile(os.path.join(dest_dir, "a.txt")))

            # Simulate an artifact from a previous run that should be removed.
            with open(os.path.join(dest_dir, "stale.txt"), "w") as f:
                f.write("stale")

            copy_static(src_dir, dest_dir)

            self.assertTrue(os.path.isfile(os.path.join(dest_dir, "a.txt")))
            self.assertFalse(os.path.isfile(os.path.join(dest_dir, "stale.txt")))


if __name__ == "__main__":
    unittest.main()