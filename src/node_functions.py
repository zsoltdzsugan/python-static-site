import re
from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from blocktype import BlockType

def text_node_to_html_node(node: TextNode) -> LeafNode:
    match (node.text_type):
        case TextType.TEXT:
            return LeafNode(None, node.text)
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.LINK:
            return LeafNode("a", node.text, {"href": node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": node.url, "alt": node.text})
        case _:
            raise Exception("Invalid type")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: unclosed delimiter '{delimiter}'")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text: str) -> list[(str, str)]:
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)

def extract_markdown_links(text: str) -> list[(str, str)]:
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(old_node)
            continue

        for alt, url in images:
            sections = text.split(f"![{alt}]({url})", maxsplit=1)
            if len(sections) != 2 and text:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                break
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = sections[1]

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
        

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(old_node)
            continue

        for anchor, url in links:
            sections = text.split(f"[{anchor}]({url})", maxsplit=1)
            if len(sections) != 2 and text:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                break

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text = sections[1]

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)

    return filtered_blocks


def block_to_blocktype(block: str) -> BlockType:
    lines = block.split("\n")

    # heading
    is_heading = True
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # code
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    # quote
    if block.startswith(">") or block.startswith("> "):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # unordered list
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    # ordered list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    # everything else paragraph
    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    new_nodes = []
    
    for text_node in text_to_textnodes(text):
        node = text_node_to_html_node(text_node)
        new_nodes.append(node)

    return new_nodes

def block_to_html_node(block: str, blocktype: BlockType) -> HTMLNode:
    if blocktype is BlockType.HEADING:
        heading_count, text = block.split(" ", maxsplit=1)
        children = text_to_children(text)
        return ParentNode(f"h{len(heading_count)}", children)
    elif blocktype is BlockType.QUOTE:
        lines = block.split("\n")
        text = " ".join(line.lstrip("> ") for line in lines)
        children = text_to_children(text)
        return ParentNode("blockquote", children)
    elif blocktype is BlockType.ULIST:
        lines = block.split("\n")
        children = []
        for line in lines:
            text = line[2:]
            li_children = text_to_children(text)
            children.append(ParentNode("li", li_children))
        return ParentNode("ul", children)
    elif blocktype is BlockType.OLIST:
        lines = block.split("\n")
        children = []
        for line in lines:
            text = line.split(". ", maxsplit=1)[1]
            li_children = text_to_children(text)
            children.append(ParentNode("li", li_children))
        return ParentNode("ol", children)
    elif blocktype is BlockType.PARAGRAPH:
        text = " ".join(block.split("\n"))
        children = text_to_children(text)
        return ParentNode("p", children)
    elif blocktype is BlockType.CODE:
        lines = block.split("\n")
        code = "\n".join(lines[1:-1]) + "\n"
        text_node = TextNode(code, TextType.TEXT)
        code_node = text_node_to_html_node(text_node)

        return ParentNode("pre", [ParentNode("code", [code_node])])
    else:
        raise Exception("Wrong node tpye")



def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        blocktype = block_to_blocktype(block)
        node = block_to_html_node(block, blocktype)
        children.append(node)

    return ParentNode("div", children)

