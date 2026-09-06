import re
from enum import Enum
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    text_to_children,
)
from parentnode import ParentNode

class BlockType(Enum):
    P = "paragraph"
    H = "heading"
    C = "code"
    Q = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def block_to_block_type(block: str) -> "BlockType":
    lines = block.split("\n")

    headings = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    code = "```"
    quotes = ">"
    ulist = "- "

    if lines[0].startswith(headings):
        return BlockType.H

    if lines[0].startswith(code) and lines[-1].endswith(code):
        return BlockType.C

    if all(line.startswith(quotes) for line in lines):
        return BlockType.Q

    if all(line.startswith(ulist) for line in lines):
        return BlockType.UL

    if all(
            line.startswith(f"{index}. ")
            for index, line in enumerate(lines, start=1)
    ):
        return BlockType.OL

    return BlockType.P


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = re.split(r"\n[ \t]*\n", markdown)
    return [block.strip() for block in blocks if block.strip()]

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_t = block_to_block_type(block)

        match block_t:
            case BlockType.P:
                text = " ".join(block.splitlines())
                children = text_to_children(text)
                block_nodes.append(ParentNode("p", children))
            case BlockType.H:
                level = 0
                while block.startswith("#"):
                    block = block[1:]
                    level += 1
                block = block[1:]
                children = text_to_children(block)
                block_nodes.append(ParentNode(f"h{level}", children))
            case BlockType.C:
                block = block[4:-3]
                node = TextNode(block, TextType.TEXT)
                node = text_node_to_html_node(node)
                node = ParentNode("code", [node])
                block_nodes.append(ParentNode("pre", [node]))
            case BlockType.Q:
                lines = block.splitlines()
                for i in range(len(lines)):
                    lines[i] = lines[i][1:]
                    if lines[i].startswith(" "):
                        lines[i] = lines[i][1:]
                text = " ".join(lines)
                children = text_to_children(text)
                block_nodes.append(ParentNode("blockquote", children))
            case BlockType.UL:
                lines = block.splitlines()
                li_nodes = []
                for line in lines:
                    line = line[2:]
                    children = text_to_children(line)
                    li_nodes.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ul", li_nodes))
            case BlockType.OL:
                lines = block.splitlines()
                li_nodes = []
                for line in lines:
                    line = line.split(". ", 1)[1]
                    children = text_to_children(line)
                    li_nodes.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ol", li_nodes))

    return ParentNode("div", block_nodes)
