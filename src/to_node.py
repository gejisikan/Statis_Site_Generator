from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from block import BlockType, block_to_block_type

import re

re_image = r"!\[(.+?)\]\((https?://[^\s)]+)\)"
re_link = r"[^!]?\[(.+?)\]\((https?://[^\s)]+)\)"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)       
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            props = {"href":text_node.url}
            return LeafNode("a", text_node.text, props)
        case TextType.IMAGE:
            props = {"src":text_node.text,
                     "url":text_node.url
                     }
            return LeafNode("a", "", props)           
        
        case _:
            raise Exception("type error")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        target = old_node.text.split(delimiter)
        lenght = len(target)
        if lenght%2 == 0:
            raise Exception("text error", target)
        for i in range(lenght):
            text = target[i]
            if text == "":
                continue
            if i%2 != 0:
                target[i] = TextNode(text, text_type)
            else:
                target[i] = TextNode(text, TextType.TEXT)
        result += target
    return result

def split_nodes_link(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        link_target = extract_markdown_links(node.text)
        if len(link_target) == 0:
            result.append(node)
            continue

        target_text = re.sub(re_link, " ~~", node.text)

        old_text = ""
        for text in target_text:
            if text == "~" and old_text[-1] == "~":
                result.append(TextNode(old_text[:-1], TextType.TEXT))
                link = link_target.pop(0)
                result.append(TextNode(link[0], TextType.LINK, link[1]))
                old_text = ""
                continue

            old_text += text
        if old_text != "":
            result.append(TextNode(old_text, TextType.TEXT))
    return result

def split_nodes_image(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        image_target = extract_markdown_images(node.text)
        if len(image_target) == 0:
            result.append(node)
            continue
        target_text = re.sub(re_image, "~~", node.text)

        old_text = ""
        for text in target_text:
            if text == "~" and old_text[-1] == "~":
                result.append(TextNode(old_text[:-1], TextType.TEXT))
                image = image_target.pop(0)
                result.append(TextNode(image[0], TextType.IMAGE, image[1]))
                old_text = ""
                continue

            old_text += text
        if old_text != "":
            result.append(TextNode(old_text, TextType.TEXT))
    return result

def extract_markdown_images(text):
    return re.findall(re_image, text)

def extract_markdown_links(text):
    return re.findall(re_link, text)


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([node], "`", TextType.CODE), "_", TextType.ITALIC), "**", TextType.BOLD)
        ))

def markdown_to_blocks(markdown):
    result = []
    blok_list = markdown.split("\n\n")
    
    for blok in blok_list:
        blok = blok.split("\n")
        temp = []
        for item in blok:
            item = item.strip()
            if item == "":
                continue
            temp.append(item)
        if len(temp) != 0:
            result.append("\n".join(temp))
    return result

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node_div = ParentNode("div", [])

    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAP:
                block = block.replace("\n", " ")
                values = text_to_textnodes(block)
                html_node_div.children.append(ParentNode("p", list(map(text_node_to_html_node, values))))
            case BlockType.CODE:
                if block[3] == "\n":
                    block = block[4:-3]
                else:
                    block = block[3:-3]
                html_node_div.children.append(ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(block, TextType.TEXT))])]))
            case BlockType.HEADING:
                count = 0
                for char in block:
                    if char == "#":
                        count += 1
                    else:
                        break
                values = text_to_textnodes(block[count + 1:])
                html_node_div.children.append(ParentNode(f"h{count}", list(map(text_node_to_html_node, values))))
            case BlockType.QUOTE:
                temp = block.split("\n")
                for i in range(len(temp)):
                    temp[i] == temp[i][1:]
                values = text_to_textnodes("\n".join(temp))
                html_node_div.children.append(ParentNode("blockquote", list(map(text_node_to_html_node, values))))
            case BlockType.UNORDERED_LIST:
                values = ParentNode("ul", [])
                temp = block.split("\n")
                for value in temp:
                    values.children.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(value[2:])))))
                html_node_div.children.append(ParentNode("blockquote", values))
            case BlockType.ORDERED_LIST:
                values = ParentNode("ol", [])
                temp = block.split("\n")
                for value in temp:
                    values.children.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(value[3:])))))
                html_node_div.children.append(ParentNode("blockquote", values))
    
    return html_node_div

