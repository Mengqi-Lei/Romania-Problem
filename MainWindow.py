import copy

from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

from PySide2.QtGui import QPainter, QPen, QColor
from PySide2.QtWidgets import QWidget, QMainWindow
from collections import deque
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from Node import Node, Graph
import time
from time import sleep
import functools
from Evaluation import MyFigureCanvas
import numpy as np
import math
import random


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        # 界面设置
        self.setFrame()
        # 槽函数初始化
        self.signal_connect()
        # 图数据初始化
        self.vex = {}
        self.cities = {}
        self.dict = {}
        self.graph = Graph()
        self.h = {}
        self.location = {}
        self.visit = {}
        self.build_map()
        self.constructGraph()
        # 起点与终点：
        self.start = None
        self.end = None
        for item in self.graph.nodes:
            if item.name == "Arad":
                self.start = item
            if item.name == "Bucharest":
                self.end = item
        # 过程记录：
        self.close_width = None
        self.open_width = None
        self.cost_width = 0
        self.time_width = 0

        self.close_greed = None
        self.open_greed = None
        self.cost_greed = 0
        self.time_greed = 0

        self.close_Astar = None
        self.open_Astar = None
        self.cost_Astar = 0
        self.time_Astar = 0

        self.open_log=[]
        # 初始化下拉框选项：
        i = 0
        for name in self.visit.keys():
            if name != "Arad":
                self.comboBox.addItem(name, i)
        # 绘图窗口：
        # 初始化 gv_visual_data 的显示
        self.visual_data = None

    # UI界面设置：
    def setFrame(self):
        # 初始化控件
        self.resize(1500, 940)
        self.setWindowTitle(QCoreApplication.translate("Form", u"罗马尼亚度假问题", None))

        self.textEdit = QTextEdit(self)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(80, 640, 861, 201))
        # 按钮：
        self.bfsButton = QPushButton(self)
        self.bfsButton.setObjectName(u"bfsButton")
        self.bfsButton.setGeometry(QRect(470, 850, 111, 41))
        self.greedyButton = QPushButton(self)
        self.greedyButton.setObjectName(u"greedyButton")
        self.greedyButton.setGeometry(QRect(590, 850, 111, 41))
        self.clearButton = QPushButton(self)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setGeometry(QRect(830, 850, 111, 41))
        self.aStarButton = QPushButton(self)
        self.aStarButton.setObjectName(u"aStarButton")
        self.aStarButton.setGeometry(QRect(710, 850, 111, 41))
        # combo box
        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(170, 850, 141, 41))


        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 610, 111, 21))

        self.graphicsView = QGraphicsView(self)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(1020, 41, 440, 851))

        # 设置节点位置
        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(170, 40, 81, 18))
        self.label_3 = QLabel(self)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(110, 100, 81, 18))
        self.label_4 = QLabel(self)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(65, 170, 95, 18))
        self.label_5 = QLabel(self)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(100, 260, 81, 18))
        self.label_6 = QLabel(self)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(180, 340, 81, 18))
        self.label_7 = QLabel(self)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(190, 410, 81, 18))
        self.label_8 = QLabel(self)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(190, 500, 81, 18))
        self.label_9 = QLabel(self)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(350, 480, 81, 18))
        self.label_10 = QLabel(self)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(530, 580, 81, 18))
        self.label_11 = QLabel(self)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(930, 540, 81, 18))
        self.label_12 = QLabel(self)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(290, 210, 81, 18))
        self.label_13 = QLabel(self)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(460, 220, 81, 18))
        self.label_14 = QLabel(self)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(680, 110, 81, 18))
        self.label_15 = QLabel(self)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(800, 180, 81, 18))
        self.label_16 = QLabel(self)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(860, 270, 81, 18))
        self.label_17 = QLabel(self)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(350, 320, 131, 18))
        self.label_18 = QLabel(self)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(470, 400, 81, 18))
        self.label_19 = QLabel(self)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(600, 450, 81, 18))
        self.label_20 = QLabel(self)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(730, 410, 81, 18))
        self.label_21 = QLabel(self)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(900, 410, 81, 18))
        self.chooseStart = QLabel(self)
        self.chooseStart.setObjectName(u"chooseStart")
        self.chooseStart.setGeometry(QRect(80, 850, 71, 41))
        self.chooseAlgo = QLabel(self)
        self.chooseAlgo.setObjectName(u"chooseAlgo")
        self.chooseAlgo.setGeometry(QRect(380, 850, 71, 41))
        # 设置标签

        self.greedyButton.setText(QCoreApplication.translate("Form", u"Greedy", None))
        self.bfsButton.setText(QCoreApplication.translate("Form", u"UCS", None))
        self.label.setText(QCoreApplication.translate("Form", u"OutPut:", None))
        self.clearButton.setText(QCoreApplication.translate("Form", u"Clear", None))
        self.aStarButton.setText(QCoreApplication.translate("Form", u"A*", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Oradea", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Zerind", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Arad(Start)", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Timisoara", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Lugoj", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Mehadia", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Dobreta", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Craiova", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Glurgiu", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Eforie", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Sibiu", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Fagaras", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Neamt", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"Iasi", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"Vaslui", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"Rimmicu Vicea", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"Pitesti", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"Bucharest", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"Urziceni", None))
        self.label_21.setText(QCoreApplication.translate("Form", u"Hirsova", None))
        self.chooseStart.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u7ec8\u70b9\uff1a", None))
        self.chooseAlgo.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u7b97\u6cd5\uff1a", None))

    # 信号槽连接
    def signal_connect(self):

        self.bfsButton.clicked.connect(self.bfs_deal)
        self.greedyButton.clicked.connect(self.greedy_deal)
        self.aStarButton.clicked.connect(self.a_star_deal)
        self.clearButton.clicked.connect(self.clear_checked)
        self.comboBox.currentIndexChanged.connect(self.choose_end)

    # 从下拉框选择并确定终点
    def choose_end(self):
        index = self.comboBox.currentIndex()
        end_name=self.comboBox.itemText(index)
        self.clear_checked()

        # 终点修改时，重置各记录：
        if end_name != self.end.name:
            self.close_width = None
            self.open_width = None
            self.cost_width = 0
            self.time_width = 0

            self.close_greed = None
            self.open_greed = None
            self.cost_greed = 0
            self.time_greed = 0

            self.close_Astar = None
            self.open_Astar = None
            self.cost_Astar = 0
            self.time_Astar = 0
            self.paintPlt()
            self.open_log=[]
        for item in self.graph.nodes:
            if item.name == end_name:
                self.end = item
        self.repaint()



    # 绘制统计图：
    def paintPlt(self):
        self.visual_data = MyFigureCanvas(width=self.graphicsView.width() / 101,
                                          height=self.graphicsView.height() / 101,
                                          ucs=[self.cost_width, self.time_width],
                                          greedy=[self.cost_greed, self.time_greed],
                                          astar=[self.cost_Astar, self.time_Astar])

        # 加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        self.graphicsScene = QGraphicsScene()  # 创建一个QGraphicsScene
        # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.graphicsScene.addWidget(self.visual_data)
        # 把QGraphicsScene放入QGraphicsView中
        # self.ui 后跟的是对象的名字 这里QGraphicsView对象的名字是graphicsView
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsView.show()  # 调用show方法呈现图形

    # 绘图事件
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)  # 消除锯齿
        painter.begin(self)
        self.draw_map(painter)
        painter.end()

    # drawMap函数：
    def draw_map(self, painter):

        for i in self.cities.keys():
            v1 = i
            for j in self.cities[i]:
                v2 = j[0]
                p1 = self.location[v1]
                p2 = self.location[v2]
                x1, y1 = p1[0], p1[1]
                x2, y2 = p2[0], p2[1]
                # 绘制边
                pen = QPen(QColor(192, 192, 192), 3)
                if self.visit[v1] == 0 or self.visit[v2] == 0:
                    pen = QPen(QColor(192, 192, 192), 3)
                elif self.visit[v1] == 2 and self.visit[v2] == 2:
                    pen = QPen(QColor(0, 201, 87), 4)
                elif self.visit[v1] != 0 and self.visit[v2] != 0:
                    pen = QPen(QColor(244, 164, 96), 4)
                painter.setPen(pen)
                painter.drawLine(x1, y1, x2, y2)
                # 标注长度
                pen = QPen(QColor(160, 160, 160), 3)
                painter.setPen(pen)  # 对画笔进行设置，QColor参数为颜色的rgb值，后面3为点的大小
                distance = str(j[1])
                rect = QRect((x1 + x2) / 2, (y1 + y2) / 2, 70, 50)
                painter.drawText(rect, distance)

        for key in self.location:
            p = self.location[key]
            x = p[0]
            y = p[1]
            if self.visit[key] == 0:
                pen = QPen(QColor(150, 150, 150), 3)  # 灰色
                brush = QBrush(QColor(192, 192, 192))
            elif self.visit[key] == 1:
                pen = QPen(QColor(237, 145, 33), 3)  # 橙色
                brush = QBrush(QColor(252, 230, 201))
            else:
                pen = QPen(QColor(0, 201, 87), 3)
                brush = QBrush(QColor(189, 252, 201))
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawEllipse(QPointF(x, y), 10, 10)

    # 处理bfs信号
    def bfs_deal(self):
        self.UCS()

    # 处理greedy信号
    def greedy_deal(self):
        self.greedy()

    # 处理a*信号
    def a_star_deal(self):
        self.AstarAlgorithm()

    # 处理清除信号
    def clear_checked(self):
        for item in self.visit.keys():
            self.visit[item] = 0
        str = ""
        self.textEdit.setText(str)
        self.open_log=[]
        self.repaint()

    # 打印路径：
    def printPath(self, close=[]):
        cost = 0
        endNode = close[-1]
        path = [endNode.name]
        # 从终点向前找
        while path[-1] != self.start.name:
            if endNode.prev:
                for item in self.cities[endNode.name]:
                    if item[0] == endNode.prev.name:
                        cost += item[1]
                path.append(endNode.prev.name)
                endNode = endNode.prev
        path.reverse()

        txt = "路径为：\n"
        for i in path[:-1]:
            self.visit[i] = 2
            txt = txt + i
            txt += " -> "
        txt = txt + path[-1] + "\n\n"
        self.visit[path[-1]] = 2
        self.repaint()

        txt += "路径长度："
        txt += str(cost)
        txt += "\n\n"

        txt += "Close表：\n"
        for i in close:
            txt = txt + i.name
            txt += "  "
        txt += "\n\n"
        self.textEdit.setText(txt)

        txt += "Open表历史记录：\n"
        for line in self.open_log:
            txt+="[ "
            for i in line:
                txt+=i.name
                txt+="  "
            txt+="]\n"
        txt += "\n\n"
        self.textEdit.setText(txt)


        return cost

    # 打印open、close表：
    def print_close_open(self, close=[]):
        txt=""
        txt += "Close表：\n"
        for i in close:
            txt = txt + i.name
            txt += "  "
        txt += "\n\n"
        txt += "Open表：\n"
        for line in self.open_log:
            txt += "[ "
            for i in line:
                txt += i.name
                txt += "  "
            txt += "]\n"
        txt += "\n\n"
        self.textEdit.setText(txt)


    # 构造图
    def constructGraph(self):
        for i in self.cities.keys():
            node = Node()
            node.name = i
            node.hn = self.h[node.name]
            node.next = self.cities[i]  # 包含了 邻居城市与它们之间的距离
            self.graph.nodes.append(node)

    def build_map(self):
        self.visit = {"Arad": 0, "Bucharest": 0, "Craiova": 0,
                      "Doberta": 0, "Eforie": 0, "Fagaras": 0,
                      "Glurgiu": 0, "Hirsova": 0, "Iasi": 0,
                      "Lugoj": 0, "Mehadia": 0, "Neamt": 0,
                      "Oradea": 0, "Pitesti": 0, "Rimmicu_Vikea": 0,
                      "Sibiu": 0, "Timisoara": 0, "Urziceni": 0,
                      "Vaslui": 0, "Zerind": 0
                      }
        self.dict = {1: "Arad", 2: "Bucharest", 3: "Craiova",
                     4: "Doberta", 5: "Eforie", 6: "Fagaras",
                     7: "Glurgiu", 8: "Hirsova", 9: "Iasi",
                     10: "Lugoj", 11: "Mehadia", 12: "Neamt",
                     13: "Oradea", 14: "Pitesti", 15: "Rimmicu_Vikea",
                     16: "Sibiu", 17: "Timisoara", 18: "Urziceni",
                     19: "Vaslui", 20: "Zerind"
                     }
        self.cities = {'Arad': [['Zerind', 75], ['Timisoara', 118], ['Sibiu', 140]],
                       'Bucharest': [['Urziceni', 85], ['Glurgiu', 90], ['Pitesti', 101], ['Fagaras', 211]],
                       'Craiova': [['Doberta', 120], ['Pitesti', 138], ['Rimmicu_Vikea', 146]],
                       'Doberta': [['Mehadia', 75], ['Craiova', 120]],
                       'Eforie': [['Hirsova', 86]],
                       'Fagaras': [['Sibiu', 99], ['Bucharest', 211]],
                       'Glurgiu': [['Bucharest', 90]],
                       'Hirsova': [['Eforie', 86], ['Urziceni', 98]],
                       'Iasi': [['Neamt', 87], ['Vaslui', 92]],
                       'Lugoj': [['Mehadia', 70], ['Timisoara', 111]],
                       'Mehadia': [['Lugoj', 70], ['Doberta', 75]],
                       'Neamt': [['Iasi', 87]],
                       'Oradea': [['Zerind', 71], ['Sibiu', 151]],
                       'Pitesti': [['Rimmicu_Vikea', 97], ['Bucharest', 101], ['Craiova', 138]],
                       'Rimmicu_Vikea': [['Sibiu', 80], ['Pitesti', 97], ['Craiova', 146]],
                       'Sibiu': [['Rimmicu_Vikea', 80], ['Fagaras', 99], ['Arad', 140], ['Oradea', 151]],
                       'Timisoara': [['Lugoj', 111], ['Arad', 118]],
                       'Urziceni': [['Bucharest', 85], ['Hirsova', 98], ['Vaslui', 142]],
                       'Vaslui': [['Iasi', 92], ['Urziceni', 142]],
                       'Zerind': [['Oradea', 71], ['Arad', 75]]
                       }
        self.h = {"Arad": 366, "Bucharest": 0, "Craiova": 160, "Doberta": 242, "Eforie": 161, "Fagaras": 176,
                  "Glurgiu": 77,
                  "Hirsova": 151, "Iasi": 226, "Lugoj": 244, "Mehadia": 241, "Neamt": 234, "Oradea": 380,
                  "Pitesti": 100,
                  "Rimmicu_Vikea": 193, "Sibiu": 253, "Timisoara": 329, "Urziceni": 80, "Vaslui": 199, "Zerind": 374
                  }
        self.location = {"Arad": [50, 170], "Bucharest": [580, 450], "Craiova": [330, 480], "Doberta": [170, 490],
                         "Eforie": [910, 540], "Fagaras": [440, 220],
                         "Glurgiu": [510, 580],
                         "Hirsova": [880, 410], "Iasi": [790, 180], "Lugoj": [160, 340], "Mehadia": [170, 410],
                         "Neamt": [660, 110], "Oradea": [140, 40], "Pitesti": [450, 400],
                         "Rimmicu_Vikea": [330, 320], "Sibiu": [270, 210], "Timisoara": [70, 260],
                         "Urziceni": [730, 400], "Vaslui": [840, 258], "Zerind": [90, 100]
                         }

    # 一致代价的宽搜:
    def compare_gn(self, node1, node2):
        # 小的排右边
        if node1.gn < node2.gn:
            return 1
        elif node1.gn > node2.gn:
            return -1
        else:
            return 0

    def UCS(self):
        t1 = time.time()
        self.open_log=[]
        for i in self.visit.keys():
            self.visit[i] = 0
        startNode = self.start
        endNode = self.end
        self.visit[startNode.name] = 1

        close = []
        open = deque()
        open.append(startNode)

        while open:
            tmp=copy.deepcopy(open)
            self.open_log.append(tmp)
            self.print_close_open(close)
            # 对叶子结点以gn为标准进行排序
            open = sorted(open, key=functools.cmp_to_key(self.compare_gn))
            city = open.pop()
            if city not in close:
                close.append(city)
                self.visit[city.name] = 1
                self.halt()
                if city == endNode:
                    # print("\n贪婪搜索路径为：")
                    self.cost_width = self.printPath(close)
                    # print("贪婪搜索close表为：")
                    # for i in close:
                    #     print(i.name, end=" ")
                    # print("\n搜索总代价为：", close[-1].gn)
                    self.close_greed = close
                    t2 = time.time()
                    self.time_width = ((t2 - t1) * 1000)
                    self.paintPlt()
                    return
                for i in city.next:
                    for j in self.graph.nodes:
                        if i[0] == j.name:
                            cost = i[1]
                            i = j
                            if i not in open and i not in close:
                                i.prev = city  # 更新前置结点之前判断是否路径更佳，而不是简单的判断是否被访问
                                open.append(i)  # append是浅拷贝
                                while i.prev:
                                    for j in i.next:
                                        if j[0] == i.prev.name:
                                            i.gn = j[1] + i.prev.gn
                                            i = i.prev
                                            break
                            elif i.gn > (city.gn + cost):
                                i.prev = city  # 更新前置结点之前判断是否路径更佳，而不是简单的判断是否被访问
                                open.append(i)  # append是浅拷贝
                                while i.prev:
                                    for j in i.next:
                                        if j[0] == i.prev.name:
                                            i.gn = j[1] + i.prev.gn
                                            i = i.prev
                                            break
                            break

    # Greedy:比较的是仅hn
    def compare_hn(self, node1, node2):
        # 小的排右边
        if node1.hn < node2.hn:
            return 1
        elif node1.hn > node2.hn:
            return -1
        else:
            return 0

    def greedy(self):
        t1 = time.time()
        self.open_log = []
        for i in self.visit.keys():
            self.visit[i] = 0
        startNode = self.start
        endNode = self.end
        self.visit[startNode.name] = 1

        close = []
        open = deque()
        open.append(startNode)

        while open:
            tmp = copy.deepcopy(open)
            self.open_log.append(tmp)
            self.print_close_open(close)
            # 对叶子结点以gn为标准进行排序
            open = sorted(open, key=functools.cmp_to_key(self.compare_hn))
            city = open.pop()
            if city not in close:
                close.append(city)
                self.visit[city.name] = 1
                self.halt()
                if city == endNode:
                    # print("\n贪婪搜索路径为：")
                    self.cost_greed = self.printPath(close)
                    # print("贪婪搜索close表为：")
                    # for i in close:
                    #     print(i.name, end=" ")
                    # print("\n搜索总代价为：", close[-1].gn)
                    self.close_greed = close
                    t2 = time.time()
                    self.time_greed = ((t2 - t1) * 1000)
                    self.paintPlt()
                    return
                for i in city.next:
                    for j in self.graph.nodes:
                        if i[0] == j.name:
                            i = j
                            if i not in open and i not in close:
                                i.prev = city  # 更新前置结点之前判断是否路径更佳，而不是简单的判断是否被访问
                                open.append(i)  # append是浅拷贝
                            break

    # A*:
    def compare_fn(self, node1, node2):
        if node1.fn > node2.fn:
            return 1
        else:
            return -1

    def AstarAlgorithm(self):
        self.open_log = []
        t1 = time.time()
        # 获取h(n)
        h = self.h
        for i in self.visit.keys():
            self.visit[i] = 0
        startNode = self.start
        endNode = self.end
        self.visit[startNode.name] = 1

        close = []
        open = deque()
        open.append(startNode)

        while open:
            tmp = copy.deepcopy(open)
            self.open_log.append(tmp)
            self.print_close_open(close)
            # 对open表排序
            open = deque(sorted(open, key=functools.cmp_to_key(self.compare_fn)))
            city = open.popleft()
            # city结点不在close里面则扩展
            if city not in close:
                close.append(city)
                self.visit[city.name] = 1
                self.halt()
                if city == endNode:
                    self.close_Astar = close
                    self.cost_Astar = self.printPath(close)
                    t2 = time.time()
                    self.time_Astar = ((t2 - t1) * 1000)
                    self.paintPlt()
                    return
                for i in city.next:
                    for j in self.graph.nodes:
                        if i[0] == j.name:
                            cost = i[1]
                            i = j
                            if i not in open and i not in close:
                                # 判断是否被访问
                                i.prev = city
                                # print(f"{i.name}<-{city.name}")
                                open.append(i)
                                # 计算当前结点到起点已经走过的代价并且加上欧式距离 获取f(n)=g(n)+h(n)
                                # g(n):节点n距离起点的代价 这个代价是已知的，只需要把走过的路花费的代价加起来

                                while i.prev:
                                    for j in i.next:
                                        if j[0] == i.prev.name:
                                            i.gn = j[1] + i.prev.gn
                                            i.fn = i.gn + i.hn
                                            i = i.prev
                                            break
                            elif i.gn > (city.gn + cost):
                                i.prev = city  # 更新前置结点之前判断是否路径更佳，而不是简单的判断是否被访问
                                # print(f"{i.name}<-{city.name}")
                                open.append(i)  # append是浅拷贝
                                while i.prev:
                                    for j in i.next:
                                        if j[0] == i.prev.name:
                                            i.gn = j[1] + i.prev.gn
                                            i.fn = i.gn + i.hn
                                            i = i.prev
                                            break
                            break

    # 用于停顿并更新图
    def halt(self, t=0.5):
        self.repaint()
        sleep(t)
