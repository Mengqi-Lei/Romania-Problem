class Node:
    def __init__(self,name='',next=[],prev=None,fn=0,gn=0,hn=0):
        self.name = name
        self.next = next
        self.prev = prev
        self.fn = fn    # �ۺϴ��ۣ�fn=hn+gn
        self.gn = gn    # ��㵽��ǰ�ڵ��·������
        self.hn = hn    # ����ʽ����

class Graph:
    def __init__(self):
        # ���н�㹹��ͼ
        self.nodes = []