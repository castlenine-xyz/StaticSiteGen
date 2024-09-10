class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag=tag # str representing html tag ex: <p>
        self.value=value # str representing text in tag
        self.children=children # list of HTMLNode for nested tags
        self.props=props # dict of attributes ex {"href":www.google.com}

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props==None:
            return ""
        ans=""
        for prop in self.props:
            val=self.props[prop]
            ans="".join([ans,f' {prop}="{val}"'])
        return ans
    def __repr__(self) -> str:
        l1="HTMLNode:\n"
        l2=f"\t tag={self.tag}\n"
        l3=f"\t value={self.value}\n"
        l4=f"\t children={self.children}\n"
        l5=f"\t props={self.props}"
        return l1+l2+l3+l4+l5
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value==None:
            raise ValueError("invalid html, no value")
        if self.tag==None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'