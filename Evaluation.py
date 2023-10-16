import sys
import numpy as np

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QGraphicsScene

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class MyFigureCanvas(FigureCanvas):
    '''
    通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
    '''

    def __init__(self, parent=None, width=10, height=5,ucs=[0,0],greedy=[0,0],astar=[0,0]):
        # 创建一个Figure 如果不加figsize 显示图像过大 需要缩小
        self.fig = plt.Figure(figsize=(width, height), tight_layout=True)  # tight_layout: 用于去除画图时两边的空白
        FigureCanvas.__init__(self, self.fig)  # 初始化父类
        self.setParent(parent)

        self.xlabel=["UCS","Greedy","A*"]
        self.cost=[ucs[0],greedy[0],astar[0]]
        self.time=[ucs[1],greedy[1],astar[1]]

        axes1 = self.fig.add_subplot(211)  # 添加子图
        axes1.spines['top'].set_visible(False)  # 去掉绘图时上面的横线
        axes1.spines['right'].set_visible(False)  # 去掉绘图时右面的横线
        axes1.bar(self.xlabel,self.cost)
        axes1.set_title("The Cost of Each Algorithm")
        axes1.grid()
        for i in range(len(self.cost)):
            axes1.text(x=i-0.07, y=self.cost[i] + 1, s='%d' %self.cost[i])

        axes2 = self.fig.add_subplot(212)  # 添加子图
        axes2.spines['top'].set_visible(False)  # 去掉绘图时上面的横线
        axes2.spines['right'].set_visible(False)  # 去掉绘图时右面的横线
        axes2.bar(self.xlabel, self.time)
        axes2.set_title("Time Consumed /ms")
        axes2.grid()
        for i in range(len(self.time)):
            axes2.text(x=i - 0.07, y=self.time[i] + 1, s='%d' % self.time[i])



