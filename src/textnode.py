class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text=text
        self.text_type=text_type # "bold","italic",etc.
        self.url=url

    def __eq__(self,other_TextNode) -> bool:
        # check if two textnodes have same text type
        if self.text_type==other_TextNode.text_type:
            return True
        return False # fallback case
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"