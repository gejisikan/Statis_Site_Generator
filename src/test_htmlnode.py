import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        props = {
            "name":"names",
            "class":"new_class"
        }
        node = HTMLNode("tag","value","children", props)
        node2 = HTMLNode("tag","value","children", props)
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.children, node2.children)
        self.assertEqual(node.props, node2.props)
        self.assertEqual(node.value, node2.value)
    
    def test_uneq(self):
        node = HTMLNode("tag","value")
        node2 = HTMLNode("tag")
        self.assertNotEqual(node, node2)

    def test_isNone(self):
        node = HTMLNode()
        self.assertEqual(None, node.tag)
        self.assertEqual(None, node.value)
        self.assertEqual(None, node.children)
        self.assertEqual(None, node.props)
    
    def test_props_to_html(self):
        props = {
            "name":"names",
            "class":"new_class"
        }
        exp = "name=\"names\" class=\"new_class\""
        node = HTMLNode("tag","value", HTMLNode(), props)

        self.assertEqual(exp, node.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_not_chile(self):
        node = LeafNode("p", "Hello, world!")
        self.assertIsNone(node.children)
    
    def test_leaf_to_html_have_props(self):
        props = {
            "name":"names",
            "class":"new_class"
        }
        node = LeafNode("p", "Hello, world!", props)
        self.assertEqual(node.to_html(), "<p name=\"names\" class=\"new_class\">Hello, world!</p>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()

