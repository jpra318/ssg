

class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str,str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        fmt = ""
        for key, value in self.props.items():
            fmt = f'{fmt} {key}="{value}"'
        return fmt

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if self.tag != other.tag:
            return False

        if self.value != other.value:
            return False

        if self.children != other.children:
            return False

        if self.props != other.props:
            return False

        return True
