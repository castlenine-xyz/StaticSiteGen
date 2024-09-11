import re
import os
from textnode import TextNode
from htmlnode import HTMLNode,LeafNode,ParentNode

def main():
    txt_node=TextNode("This is a text node", "bold", "https://www.boot.dev")
    node = TextNode("This is text with a `code block` word", "text")
    generate_page("./content/index.md","./template.html","public/index.html")
    
    # markdown_to_html(mrkdwn)


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    markdown_from=read_markdown_file(from_path)
    markdown_template=read_markdown_file(template_path)
    html_str=markdown_to_html(markdown_from)
    title=extract_title(markdown_from)
    filled_html = markdown_template.replace('{{ Title }}', title)
    filled_html = filled_html.replace('{{ Content }}', html_str)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(filled_html)
    print(f'Page generated and saved to {dest_path}')
    
def read_markdown_file(file_path):
    try:
        with open(file_path, 'r') as file:
            markdown_content = file.read()
        return markdown_content
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        raise

def extract_title(markdown):
    blocks=markdown_to_blocks(markdown)
    for block in blocks:
        block_type=get_block_tag(block)
        print(block_type)
        if block_type=="h1":
            return block[2:]
    raise Exception("no title make a h1")

def markdown_to_html(markdown):
    #first conver markdown to blocks
    blocks=markdown_to_blocks(markdown)
    # nice_printing_text_node_list(blocks)
    # next get a list of block types
    block_types=[]
    block_text_nodes=[]
    html_nodes=[]
    for block in blocks:
        block_type=get_block_tag(block)
        block_types.append(block_type)
        if block_type!="p":
            txt=block[2:]
        else:
            # print("hey not a p")
            txt=block
        # print(txt)
        text_nodes=text_to_textnodes(txt)
        block_text_nodes.append(text_nodes)
        html_str=""
        for text_node in text_nodes:
            html_str+=text_node_to_html_node(text_node).to_html()
        html_str=f"<{block_type}>"+html_str+f"</{block_type}>"
        html_nodes.append(html_str)
            # html_nodes.append(text_node_to_html_node(text_node).to_html())
        # print(block[2:])
    # nice_printing_text_node_list(block_types)
    # nice_printing_text_node_list(block_text_nodes)
    # nice_printing_text_node_list(html_nodes)
    # print(text_node_to_html_node(block_text_nodes[0][0]).to_html())


    #init god
    children=[]
    index=-1
    while index < len(html_nodes)-1:
        index+=1
        # handle lists
        # print(block_types,index)
        if block_types[index] in {"ul","ol"}:
            reference=block_types[index]
            kids=""
            while index<len(html_nodes) and block_types[index]==reference :
                kids+="<li>"+html_nodes[index][4:-5].lstrip()+"</li>"
                index+=1
            children.append(f'<{reference}>{kids}</{reference}>')
        elif block_types[index]=="code":
            children.append(f'<pre>{html_nodes[index]}</pre>')
        else:
            children.append(html_nodes[index])
    # nice_printing_text_node_list(children)


    final_ans="<div>"
    for entry in children:
        final_ans+=entry
    final_ans+="</div>"
    return final_ans
    # lastly put all kids in a main div
    # god=HTMLNode("div",None,children,None)
    # print(god)
    # return god

# ---------- text node functions, should prolly move to other file ---------
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
            
def split_nodes_images_and_links(text_node):
    ans=[]
    images=extract_markdown_images(text_node.text)
    image_index=0
    links=extract_markdown_links(text_node.text)
    link_index=0
    index=-1
    # print(text_node.text.split('['))
    prev=0
    in_link_or_image=False
    while index< len(text_node.text)-1:
        index+=1
        if in_link_or_image==False:
            if text_node.text[index]=='[': # found a link
                # add previous textnode
                txt=text_node.text[prev:index]
                new_node=TextNode(txt,"text")
                ans.append(new_node)
                prev=index
                in_link_or_image=True
            elif text_node.text[index]=='!': # found a image
                # add previous textnode
                txt=text_node.text[prev:index]
                new_node=TextNode(txt,"text")
                ans.append(new_node)
                prev=index
                in_link_or_image=True
            else: continue #
        else: # in a image or link div
            if text_node.text[index]==')': #end of an image or link
                if text_node.text[prev]=='[': # close a link tag
                    link=links[link_index]
                    link_index+=1
                    txt=link[0]
                    url=link[1]
                    new_node=TextNode(txt,"link",url)
                    ans.append(new_node)
                    index+=1
                    prev=index
                    in_link_or_image=False
                elif text_node.text[prev]=='!'and text_node.text[prev+1]=='[]': # found a image
                    # print(images,image_index)
                    image=images[image_index]
                    image_index+=1
                    txt=image[0]
                    url=image[1]
                    new_node=TextNode(txt,"image",url)
                    ans.append(new_node)
                    index+=1
                    prev=index
                    in_link_or_image=False
                else:continue
            else: continue #
    # print(text_node.text[0:index])
    if ans==[]:
        return [text_node]
    return ans
    
def text_to_textnodes(text):
    inital=TextNode(text,"text")
    txt_nodes1=split_nodes(inital)
    # nice_printing(txt_nodes1)
    ans=[]
    for node in txt_nodes1:
        ans+=split_nodes_images_and_links(node)
    return ans

def nice_printing_text_node_list(nodes):
    print("[")
    for node in nodes:
        print("\t"+str(node)+",")
    print("]")



def markdown_to_blocks(markdown:str):
    temp= markdown.split("\n") # split by newlines
    return [x.rstrip().lstrip() for x in temp if x!=''] # remove blank lines and extra whitespace

# unused in final
def block_to_block_type(block):
    types={
        "#":"heading",
        "`":"code",
        ">":"qoute",
        "*":"unordered_list",
        "-":"unordered_list",
    }
    try:
        return types[block[0]]
    except:
        # check for ordered list
        if block[0].isdigit() and block[1]==".":
            return "ordered_list"
        else:
            return "paragraph"


def get_block_tag(block):
    types={
        "#":"heading",
        "`":"code",
        ">":"qoute",
        "*":"unordered_list",
        "-":"unordered_list",
    }
    #heading type
    if block[0]=="#":
        temp=block.split()
        temp=len(temp[0])
        return f'h{temp}'
    if block[0:3]=="```":
        return "code"
    if block[0]==">":
        return "blockquote"
    if block[0:2]=="* " or block[0:2]=="- ":
        return "ul"
    if block[0].isdigit() and block[1]==".":
        return "ol"
    return "p" # paragraph fallback case
main()