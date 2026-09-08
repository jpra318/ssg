import os
import shutil
import sys

from gencontent import generate_page


def copy_static(src_dir: str, dest_dir: str) -> None:
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        print(f"{src_path} -> {dest_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            copy_static(src_path, dest_path)


def generate_pages_recursive(basepath: str, dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(src_path) and src_path.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, os.path.splitext(entry)[0] + ".html")
            generate_page(basepath, src_path, template_path, dest_path)
        elif os.path.isdir(src_path):
            new_dest = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(basepath, src_path, template_path, new_dest)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    dest_dir = sys.argv[2] if len(sys.argv) > 2 else "docs"
    print("Copying static files...")
    copy_static("static", dest_dir)
    print("Static files copied.")
    print("Generating pages...")
    generate_pages_recursive(basepath, "content", "template.html", dest_dir)
    print("Pages generated.")


if __name__ == "__main__":
    main()
