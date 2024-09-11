import re
from textnode import TextNode
from htmlnode import HTMLNode,LeafNode,ParentNode

def main():
    txt_node=TextNode("This is a text node", "bold", "https://www.boot.dev")
    node = TextNode("This is text with a `code block` word", "text")
    # print(txt_node)
    # print(text_node_to_html_node(txt_node))
    #print(split_nodes(node))


def text_node_to_html_node(text_node):
    if text_node.text_type=="text":
        return LeafNode(None,text_node.text)
    elif text_node.text_type=="bold":
        return LeafNode("b",text_node.text)
    elif text_node.text_type=="italic":
        return LeafNode("i",text_node.text)
    elif text_node.text_type=="code":
        return LeafNode("code",text_node.text)
    elif text_node.text_type=="link":
        return LeafNode("a",text_node.text,props={"href":text_node.url})
    elif text_node.text_type=="image":
        return LeafNode("img","",props={"src":text_node.url,"alt":text_node.text})
    else:
        raise Exception(f"invalid type for text node {text_node.text_type}")

def split_nodes(old_node: TextNode):
    ans=[]
    delims={"**":"bold", "*":"italic","`":"code",}
    nested_node_types=[old_node.text_type]
    prev=0
    index=-1
    while index < len(old_node.text):
        index+=1
        keyword=None
        try:
            key=old_node.text[index:index+2]
            keyword=delims[key]# bold
        except: # if not bold
            try:
                key=old_node.text[index]
                keyword=delims[key]# italic or code
            except:
                continue
        # if here we have a keyword
        # print("keyword", index)
        if keyword!=nested_node_types[-1]: # new tag starting
                rebuilt_text=old_node.text[prev:index]
                if rebuilt_text=="":
                    nested_node_types.append(keyword)
                    index+=len(key)
                    prev=index
                    continue
                # print(rebuilt_text)
                ans.append(TextNode(rebuilt_text, nested_node_types[-1]))
                nested_node_types.append(keyword)
                index+=len(key)
                prev=index

        else:# end of a node
            # print("end of a block")
            temp=nested_node_types.pop(-1)
            # print(prev,index)
            rebuilt_text=old_node.text[prev:index+1]
            # print(rebuilt_text)
            #print(keyword)
            rebuilt_text=rebuilt_text[:-1]# strip keyword
            # print(rebuilt_text)
            ans.append(TextNode(rebuilt_text, temp))
            index+=len(key)
            prev=index
    rebuilt_text=old_node.text[prev:]
    if rebuilt_text!="":
        temp=nested_node_types.pop(-1)
        ans.append(TextNode(rebuilt_text, temp))
    # print(ans)
    # if nested_node_types!=[]:
    #     raise Exception(f"invalid deliminator somewhere {nested_node_types} should be[] at end")
    return ans
            
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return matches
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)
    return matches
            

main()