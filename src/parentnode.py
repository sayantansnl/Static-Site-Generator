from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Put a proper tag")
        if self.children == None:
            raise ValueError("No children")
        children_string = ""
        for node in self.children:
            children_string += node.to_html()
        return f'<{self.tag}>{children_string}</{self.tag}>'

