import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

from to_node import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node
from block import block_to_block_type, BlockType

class testTextNodeToHtmlNode(unittest.TestCase):
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def split_nodes(self):
        target = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([target], "`", TextType.CODE)
        exp = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, exp)

    def split_nodes(self):
        target1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        target2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([target1, target2], "`", TextType.CODE)
        exp = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, exp)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_link(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )    
    
    def test_text_to_textnodes(self):
        self.maxDiff = None
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_list = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node_list,
        )    
    
    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_is_heading(self):
        md1 = "# title"
        md2 = "## title"
        md3 = "### title"
        md4 = "#### title"
        md5 = "##### title"
        md6 = "###### title"
        md7 = "####### title"
        md_not = "#title"

        self.assertEqual(block_to_block_type(md1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md4), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md5), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md6), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md7), BlockType.PARAGRAP)
        self.assertEqual(block_to_block_type(md_not), BlockType.PARAGRAP)

    def test_block_to_block_type_is_code(self):
        md1 = "```code```"
        md2 = "``` code ```"
        md_not1 = "```code"
        md_not2 = "code```"


        self.assertEqual(block_to_block_type(md1), BlockType.CODE)
        self.assertEqual(block_to_block_type(md2), BlockType.CODE)
        self.assertEqual(block_to_block_type(md_not1), BlockType.PARAGRAP)
        self.assertEqual(block_to_block_type(md_not2), BlockType.PARAGRAP)

    def test_block_to_block_type_is_quote(self):
        md1 = ">quote\n>quote"
        md2 = ">quote"
        md_not1 = "quote\n>quote"
        md_not2 = ">quote\nquote"


        self.assertEqual(block_to_block_type(md1), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(md2), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(md_not1), BlockType.PARAGRAP)
        self.assertEqual(block_to_block_type(md_not2), BlockType.PARAGRAP)

    def test_block_to_block_type_is_unordered_list(self):
        md1 = "- unordered_list\n- unordered_list"
        md2 = "- unordered_list"
        md_not1 = "- unordered_list\n-unordered_list"
        md_not2 = "-unordered_list\n- unordered_list"


        self.assertEqual(block_to_block_type(md1), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(md2), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(md_not1), BlockType.PARAGRAP)
        self.assertEqual(block_to_block_type(md_not2), BlockType.PARAGRAP)

    def test_block_to_block_type_is_ordered_list(self):
        md1 = "1. ordered_list\n2. ordered_list"
        md2 = "1. ordered_list"
        md_not1 = "1. ordered_list\n2.ordered_list"
        md_not2 = "1.ordered_list\n2. ordered_list"
        md_not3 = "2. ordered_list\n1. ordered_list"
        md_not4 = "1. ordered_list\n1. ordered_list"


        self.assertEqual(block_to_block_type(md1), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(md2), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(md_not1), BlockType.PARAGRAP)
        self.assertEqual(block_to_block_type(md_not2), BlockType.PARAGRAP)
        self.assertEqual(block_to_block_type(md_not3), BlockType.PARAGRAP)
        self.assertEqual(block_to_block_type(md_not4), BlockType.PARAGRAP)


    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
