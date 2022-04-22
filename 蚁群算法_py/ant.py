# 蚂蚁

from sceneMap import *
from random import randint, random, choice  # 随机数

# 所有方向，从12点开始顺时针
allF = ((0, 1), (1, 0), (0, -1), (-1, 0))

infoMax = 65000  # 信息素最大携带量
infoConsume = 50  # 信息素释放量


class Ant():

    def __init__(self, name_, x_=0, y_=0):
        self.name = name_  # 名字
        self.x, self.y = x_, y_  # 当前位置
        # 朝向
        self.fa = allF[randint(0, 3)]
        # 视距
        self.seeLen = 1
        # 信息素
        self.infoHome = infoMax
        self.infoFood = 0
        # 任务类型，0回家 1找食物
        self.type = 1
        # 上一步
        self.last = (x_, y_)

    def updateInfo(self):
        '''刷新信息素'''
        what = sceneMap.data[xy(self.x, self.y)]  # 读取数据地图

        if self.type == 1:  # 找食物状态
            if what == 2:  # 找到食物
                self.infoHome = 0
                self.infoFood = infoMax
                self.type = 0  # 转换到找家
                return
            elif what == 1:  # 路过家
                self.infoHome = infoMax  # 补充信息素
            if self.infoHome > 0:  # 释放家信息素
                if sceneMap.infoHome[xy(self.x, self.y)] > self.infoHome:
                    return  # 当本来残留的信息素大于自身储存时，不释放
                sceneMap.infoHome[xy(self.x, self.y)] = self.infoHome
                self.infoHome -= infoConsume
            # elif random() < 0.05:  # 没找到，信息素又用完了，有概率直接回家
            #     self.type = 0  # 转换到找家
        elif self.type == 0:  # 找家状态
            if what == 1:  # 找到家
                self.infoHome = infoMax
                self.infoFood = 0
                self.type = 1  # 转换到找食物
                return
            elif what == 2:
                self.infoFood = infoMax  # 补充信息素
            if self.infoFood > 0:  # 释放食物信息素
                if sceneMap.infoFood[xy(self.x, self.y)] > self.infoFood:
                    return  # 当本来残留的信息素大于自身储存时，不释放
                sceneMap.infoFood[xy(self.x, self.y)] = self.infoFood
                self.infoFood -= infoConsume

    def goFood(self):
        '''找食物'''
        # 记录信息素和墙
        maxN, maxF = 0, 0  # 记录信息素的最大值和最大方向
        canGo = []  # 记录能走的方向元组
        noT = 0
        for f in range(4):
            if self.fa == allF[f]:
                noT = (f + 2) % 4
                break
        for f in range(4):  # 遍历身旁四个方向
            if f == noT:
                continue
            # 探测目的地
            if sceneMap.data[xy(self.x + allF[f][0], self.y + allF[f][1])] == 2:  # 若该方向上有食物
                self.fa = (allF[f][0], allF[f][1])  # 直接去那个方向
                self.x, self.y = self.x + self.fa[0], self.y + self.fa[1]
                return
            # 探测信息素
            n = sceneMap.infoFood[xy(
                self.x + allF[f][0], self.y + allF[f][1])]  # 记录信息素
            if n > maxN:  # 浓度大于以往
                maxN, maxF = n, f  # 记录值和方向
            # 探测墙
            if sceneMap.map[xy(self.x + allF[f][0], self.y + allF[f][1])] == 0:  # 若该方向上无墙
                canGo.append((allF[f][0], allF[f][1]))  # 元组写入列表
        # 计算方向
        if not canGo:  # 没有能走的路，则回头
            self.fa = allF[noT]
        elif maxN > 0 and random() < 0.85:  # 若周围存在信息素，有概率沿着信息素走
            self.fa = allF[maxF]  # 方向为浓度最大的方向
        else:  # 周围没有信息素
            if self.fa not in canGo or random() < 0.15:  # 前进方向上不能走或0.2概率，随机一个新方向。否则直行。
                self.fa = choice(canGo)  # random模块，从能走列表中随机取一位
        # 行动
        self.x, self.y = self.x + self.fa[0], self.y + self.fa[1]

    def goHome(self):
        '''回家状态'''
        # 记录信息素和墙
        maxN, maxF = 0, 0  # 记录信息素的最大值和最大方向
        canGo = []  # 记录能走的方向元组
        noT = 0
        for f in range(4):
            if self.fa == allF[f]:
                noT = (f + 2) % 4
                break
        for f in range(4):  # 遍历身旁四个方向
            if f == noT:
                continue
            n = sceneMap.infoHome[xy(
                self.x + allF[f][0], self.y + allF[f][1])]  # 记录信息素
            if n > maxN:  # 浓度大于以往
                maxN, maxF = n, f  # 记录值和方向
            if sceneMap.map[xy(self.x + allF[f][0], self.y + allF[f][1])] == 0:  # 若该方向上无墙
                canGo.append((allF[f][0], allF[f][1]))  # 元组写入列表
            if sceneMap.data[xy(self.x + allF[f][0], self.y + allF[f][1])] == 1:  # 若该方向上有家
                self.fa = (allF[f][0], allF[f][1])  # 直接去那个方向
                self.x, self.y = self.x + self.fa[0], self.y + self.fa[1]
                return
        # 计算方向
        if maxN > 0 and random() < 0.85:  # 若周围存在信息素，有概率沿着信息素走
            self.fa = allF[maxF]  # 方向为浓度最大的方向
        else:  # 周围没有信息素
            if self.fa not in canGo or random() < 0.2:  # 前进方向上不能走或0.2概率，随机一个新方向。否则直行。
                self.fa = choice(canGo)  # random模块，从能走列表中随机取一位
        # 行动
        self.x, self.y = self.x + self.fa[0], self.y + self.fa[1]
        # print(self.name, "-x", self.x, " y", self.y, " fa", self.fa)

    def update(self):
        '''刷新'''
        # 放信息素
        self.updateInfo()
        # 移动
        if self.type == 1:
            self.goFood()
        if self.type == 0:
            self.goHome()
