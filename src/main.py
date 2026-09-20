from textnode import *
from generate_page import *
import os
import shutil

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
    tn = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(tn)
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")
    

if __name__ == "__main__":
    main()
