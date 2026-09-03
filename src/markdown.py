import re
from enum import Enum

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
    code = ("```")
    quotes = (">")
    ulist = ("- ")

    if lines[0].startswith(headings):
        return BlockType.H

    if lines[0].startswith(code) and lines[-1].endswith(code):
        return BlockType.C

    is_quote = True
    for line in lines:
        if not line.startswith(quotes):
            is_quote = False
            break
    if is_quote:
        return BlockType.Q

    is_ulist = True
    for line in lines:
        if not line.startswith(ulist):
            is_ulist = False
            break
    if is_ulist:
        return BlockType.UL

    is_olist = True
    for index, line in enumerate(lines, start=1):
        if not line.startswith(f"{index}. "):
            is_olist = False
            break
    if is_olist:
        return BlockType.OL

    return BlockType.P


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = re.split(r"\n[ \t]*\n", markdown)
    return [block.strip() for block in blocks if block.strip()]
