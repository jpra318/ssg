from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict[str,str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or not len(self.tag):
            raise ValueError("missing tag")
        if not len(self.children):
            raise ValueError("missing children")
        value = ""
        for child in self.children:
            value += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{value}</{self.tag}>'

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def __eq__(self, other):
        if self.tag != other.tag:
            return False
        if self.children != other.children:
            return False
        if self.props != other.props:
            return False
        return True
