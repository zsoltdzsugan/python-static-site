import os
from node_functions import *

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    
    for block in blocks:
        blocktype = block_to_blocktype(block)

        if blocktype is BlockType.HEADING:
            if block.startswith("# "):
                title = block.split("# ", maxsplit=1)[1]
                return title

    raise Exception("No title")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        from_contents = f.read()

    with open(template_path, 'r') as f:
        template_contents = f.read()

    title = extract_title(from_contents)
    from_html_node = markdown_to_html_node(from_contents)
    content = from_html_node.to_html()
    
    html = template_contents.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    if not os.path.exists(dir_path_content):
        raise Exception("Content path not exists")

    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(source_path):
            os.makedirs(dest_path, exist_ok=True)

            generate_pages_recursive(source_path, template_path, dest_path, basepath)

        elif os.path.isfile(source_path):
            if not item.endswith(".md"):
                continue

            dest_path = os.path.splitext(dest_path)[0] + ".html"
            generate_page(source_path, template_path, dest_path, basepath)
