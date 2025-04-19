from enum import Enum

class BlockType(Enum):
    PARAGRAP = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def block_to_block_type(block):
    if block[0] == "#":
        count = 0
        for char in block:
            if char != "#" and char != " ":
                break
            elif char == "#":
                count += 1
            elif char == " ":
                if count <= 6:
                    return BlockType.HEADING
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    if block[0] == ">":
        temp = block.split("\n")
        is_link = True 
        for line in temp:
            if line[0] != ">":
                is_link = False
                break
        if is_link:
            return BlockType.QUOTE
        
    if block[:2] == "- ":
        temp = block.split("\n")
        is_unordered_list = True 
        for line in temp:
            if line[:2] != "- ":
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
    
    if block[:3] == "1. ":
        temp = block.split("\n")
        num = 1
        is_ordered_list = True 
        for line in temp:
            if line[:3] != f"{num}. ":
                is_ordered_list = False
                break
            num += 1
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAP
        

