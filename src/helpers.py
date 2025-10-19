from textnode import TextNode, TextType
from leafnode import LeafNode

import re

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text, None)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text, None)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text, None)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else: 
        return "Not a valid type"
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_title(markdown):
    if not markdown.split("\n")[0].startswith("# "):
        raise Exception("not a valid title")
    return markdown.lstrip("# ").strip()


def extract_markdown_images(text):
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_regex, text)
    return matches

def extract_markdown_links(text):
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_regex, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        matches = extract_markdown_images(old_node_text)
        if len(matches) == 0 and len(old_node_text) != 0:
            new_nodes.append(old_node)
        else:
            sections = re.split(image_regex, old_node_text)
            node_arr = []
            for i in range(0, len(sections)):
                if sections[i] == "":
                    continue
                if i % 3 == 0:
                    node_arr.append(TextNode(sections[i], TextType.TEXT))
                else:
                    if i % 3 == 1:
                        alt = sections[i]
                        url = sections[i + 1]
                        node_arr.append(TextNode(alt, TextType.IMAGE, url))
                    elif i % 3 == 2:
                        continue
            new_nodes.extend(node_arr)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        matches = extract_markdown_links(old_node_text)
        if len(matches) == 0 and len(old_node_text) != 0:
            new_nodes.append(old_node)
        else:
            sections = re.split(link_regex, old_node_text)
            node_arr = []
            for i in range(0, len(sections)):
                if sections[i] == "":
                    continue
                if i % 3 == 0:
                    node_arr.append(TextNode(sections[i], TextType.TEXT))
                else:
                    if i % 3 == 1:
                        alt = sections[i]
                        url = sections[i + 1]
                        node_arr.append(TextNode(alt, TextType.LINK, url))
                    elif i % 3 == 2:
                        continue
            new_nodes.extend(node_arr)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes