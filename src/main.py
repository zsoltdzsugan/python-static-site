from textnode import *
from generate_page import *
import os
import shutil
import sys

def copy_static_to_public(static="static", public="public"):
    if not os.path.exists(static):
        return

    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)

    copy_directory(static, public)


def copy_directory(from_directory, to_copy_directory):
    for item in os.listdir(from_directory):
        from_path = os.path.join(from_directory, item)
        to_path = os.path.join(to_copy_directory, item)

        print(f"Copying {from_path} -> {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            if not os.path.exists(to_path):
                os.mkdir(to_path)
            copy_directory(from_path, to_path)



def main():
    basepath = "."
    if len(sys.argv) > 1 and sys.argv[1]:
        basepath = sys.argv[1]

    static = os.path.join(basepath, "static")
    public = os.path.join(basepath, "docs")
    content = os.path.join(basepath, "content")
    template = os.path.join(basepath, "template.html")

    copy_static_to_public(static, public)
    generate_pages_recursive(content, template, public)
    

if __name__ == "__main__":
    main()
