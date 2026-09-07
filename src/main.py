import os
import shutil
from textnode import TextType, TextNode


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

def main():
    print("Copying static files...")
    copy_static("static", "public")
    print("Static files copied.")

if __name__ == "__main__":
    main()
