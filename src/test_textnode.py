import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_uneq(self):
        node = TextNode("This is a a text node", TextType.BOLD)
        node2 = TextNode("This is a b text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_isNone(self):
        node = TextNode("This is a b text node", TextType.BOLD)
        self.assertEqual(None, node.url)
    
    def test_url(self):
        url = "url is this"
        node = TextNode("This is a b text node", TextType.BOLD, url)
        self.assertEqual(url, node.url)


if __name__ == "__main__":
    unittest.main()