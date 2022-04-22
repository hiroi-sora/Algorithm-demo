# 管理者

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from sceneMap import *
from ant import *


class Manager():

    def __init__(self, x_=0, y_=0):
        self.nestX, self.nestY = x_, y_  # 巢穴位置
        self.foodX, self.foodY = sceneMap.xl - x_, sceneMap.yl - y_  # 食物位置
        sceneMap.data[xy(self.nestX, self.nestY)] = 1
        sceneMap.data[xy(self.foodX, self.foodY)] = 2
        sceneMap.data[xy(self.foodX + 1, self.foodY)] = 2
        sceneMap.data[xy(self.foodX - 1, self.foodY)] = 2
        sceneMap.data[xy(self.foodX, self.foodY + 1)] = 2
        sceneMap.data[xy(self.foodX, self.foodY - 1)] = 2
        # 构造蚂蚁
        self.antNum = 0
        self.antList = []
        for i in range(40):
            a = Ant(i, self.nestX, self.nestY)
            self.antList.append(a)
            self.antNum += 1
        print("管理构造。")

    def update(self):
        '''刷新'''
        for a in self.antList:
            a.update()

    def draw(self, scale):
        # 绘制巢穴和食物
        glPointSize(scale * 3)  # 设置点的大小
        glBegin(GL_POINTS)  # 开始绘制点
        glColor3f(0.5, 0.7, 0.2)  # 指定颜色
        glVertex2f(self.nestX - sceneMap.xh, self.nestY - sceneMap.yh)
        glColor3f(0.5, 0.2, 0.7)  # 指定颜色
        glVertex2f(self.foodX - sceneMap.xh, self.foodY - sceneMap.yh)
        glEnd()
        # 绘制蚂蚁
        glPointSize(scale * 0.75)
        glColor3f(1, 1, 1)
        glBegin(GL_POINTS)  # 开始绘制点
        for a in self.antList:
            glVertex2f(a.x - sceneMap.xh, a.y - sceneMap.yh)
        glEnd()
        # 绘制巢穴和食物2层
        glPointSize(scale * 1)  # 设置点的大小
        glBegin(GL_POINTS)  # 开始绘制点
        glColor3f(0.2, 1, 0.2)  # 指定颜色
        glVertex2f(self.nestX - sceneMap.xh, self.nestY - sceneMap.yh)
        glColor3f(0.2, 0.2, 1)  # 指定颜色
        glVertex2f(self.foodX - sceneMap.xh, self.foodY - sceneMap.yh)
        glEnd()


# 母巢位置左下角1/8处，食物位置右上角1/8处
manager = Manager(sceneMap.xl // 8, sceneMap.yl // 8)
