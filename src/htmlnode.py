
class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.value = value
        self.tag = tag
        self.props = props
        self.children = children
    
    def to_html(self):
        raise NotImplementedError("NotImplemented")
    
    def props_to_html(self):
        result = ""
        if self.props is not None:
            for prop in self.props:
                result += " "
                result += f"{prop}=\"{self.props[prop]}\""
            result = result[1:]
        return result
    
    def __repr__(self):
        return f"""tag:{self.tag}\n
                   value:{self.value}\n
                   children:{self.children}\n
                   props:{self.props}\n
                """

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        else:
            prop = self.props_to_html()
            if prop != "":
                prop = " " + prop
            return f"<{self.tag}{prop}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children=[], value=None, props=None):
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("All Parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All Parent nodes must have a children")
        result = ""
        
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}>{result}</{self.tag}>"
    
