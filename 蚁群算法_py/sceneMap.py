# 场景地图

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from array import array  # 高性能数组
from random import randint  # 随机整数

xl, yl = 1, 1  # 数组第一、二维的长度
def xy(x, y): return x + y * xl  # 将二维坐标化为一维


infoSub = 30  # 每帧减少信息素的量


def arrToStr(a):
    '''返回一个数组的格式化字符串'''
    str_ = ''
    for j in range(yl):
        for i in range(xl):
            # ('0' if a[xy(i, j)] < 10 else '') + str(a[xy(i, j)]) + " "
            str_ += ' ' if a[xy(i, j)] == 0 else str(a[xy(i, j)])
        str_ += "\n"
    return str_


class SceneMap():

    def __init__(self, x_=10, y_=10):
        '''输入长宽xy'''
        global xl, yl
        xl, yl = x_, y_
        self.xl, self.yl = x_, y_
        self.xh, self.yh = x_ / 2, y_ / 2
        self.s = 5  # 缩放倍率
        # 创建并初始化数组
        list_three = [0 for i in range(xl * yl)]  # 用列表来初始化
        self.map = array('b', list_three)  # 主地图，范围-128~127
        self.data = array('b', list_three)  # 数据地图
        self.infoHome = array('H', list_three)  # 家的信息素地图，0~65535
        self.infoFood = array('H', list_three)  # 食物的信息素地图，0~65535
        self.initMap()  # 初始化地图
        print("地图构造。", xl, "x", yl)
        # print(arrToStr(self.map))

    def initMap(self):
        '''初始化地图'''
        # 构造边界
        for i in range(xl):
            self.map[xy(i, 0)] = 1
            self.map[xy(i, yl - 1)] = 1
        for j in range(yl):
            self.map[xy(0, j)] = 1
            self.map[xy(xl - 1, j)] = 1
        # 随机障碍物
        num = self.xl // 6  # 障碍物数量
        while num > 0:
            x = randint(0, self.xl - 1)  # 随机一组坐标
            y = randint(0, self.yl - 1)
            w = randint(0, self.xl // 7)  # 随机宽
            if x + w > self.xl:  # 防止出界
                w = self.xl - x - 1
            h = randint(0, self.yl // 7)
            if y + h > self.yl:
                h = self.yl - y - 1
            for i in range(x, x + w):
                for j in range(y, y + h):
                    self.map[xy(i, j)] = 1
            num -= 1

    def update(self):
        '''刷新地图'''
        for i in range(xl * yl):
            if self.infoHome[i] == 0:
                continue
            if self.infoHome[i] > infoSub:
                self.infoHome[i] -= infoSub
                continue
            self.infoHome[i] = 0
        for i in range(xl * yl):
            if self.infoFood[i] == 0:
                continue
            if self.infoFood[i] > infoSub:
                self.infoFood[i] -= infoSub
                continue
            self.infoFood[i] = 0

    def draw(self, scale):
        '''绘制地图'''
        # 绘制主地图
        glPointSize(scale)  # 设置点的大小
        glBegin(GL_POINTS)  # 开始绘制点
        for j in range(self.yl):
            for i in range(self.xl):
                if self.map[xy(i, j)] != 0:  # 主地图
                    glColor3f(0.7, 0.7, 0.7)
                    glVertex2f(i - self.xh, j - self.yh)
        glEnd()
        # 绘制信息素地图
        glPointSize(scale)  # 设置点的大小
        glBegin(GL_POINTS)  # 开始绘制点
        for j in range(self.yl):
            for i in range(self.xl):
                if self.infoHome[xy(i, j)] > 0 or self.infoFood[xy(i, j)] > 0:  # 此格子存在信息素
                    glColor3f(
                        0, self.infoHome[xy(i, j)] / 65535, self.infoFood[xy(i, j)] / 65535)
                    glVertex2f(i - self.xh, j - self.yh)
        glEnd()


# 地图
sceneMap = SceneMap(150, 150)
