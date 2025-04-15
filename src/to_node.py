from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
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
        case TextType.IMAGES:
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