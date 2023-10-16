class Node:
    def __init__(self,name='',next=[],prev=None,fn=0,gn=0,hn=0):
        self.name = name
        self.next = next
        self.prev = prev
        self.fn = fn    # 综合代价，fn=hn+gn
        self.gn = gn    # 起点到当前节点的路径代价
        self.hn = hn    # 启发式函数

class Graph:
    def __init__(self):
        # 所有结点构成图
        self.nodes = []