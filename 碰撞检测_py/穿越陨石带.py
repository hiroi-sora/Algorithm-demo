import pygame  # 绘图库
from pygame.locals import *  # 调用pygame中的所有常量
import time  # 时间库
import sys  # 系统相关
import random  # 随机数
import threading  # 多线程


class 粒子():
    '''管理粒子的类，不参与碰撞。'''
    # 本类只储存物理参数，不负责图形绘制

    def __init__(self, x, y, r, c, s):
        '''初始化，传入初始位置xy，半径r，颜色三元组c，速度二元组s'''
        self.X, self.Y, self.R, self.Color, self.Speed = x, y, r, c, s

    def 刷新函数(self):
        '''进行一帧的刷新'''
        self.X, self.Y = self.X + self.Speed[0], self.Y + self.Speed[1]
        if(self.X < -self.R):  # 当位置完全飞过屏幕最左边
            return False  # 返回F指令，表示本对象已经木大了
        return True  # 否则，返回T指令，表示本对象还活着


class 陨石():
    '''管理陨石的类，参与碰撞。'''
    # 本类只储存物理参数，不负责图形绘制

    def __init__(self, x, y, r, c, s, h):
        '''初始化，传入初始位置xy，半径r，颜色三元组c，速度二元组s，生命值h'''
        self.X, self.Y, self.R, self.Color, self.Speed, self.Hp = x, y, r, c, s, h

    def 刷新函数(self):
        '''进行一帧的刷新'''
        self.X, self.Y = self.X + self.Speed[0], self.Y + self.Speed[1]
        if(self.X < -self.R):  # 当位置完全飞出屏幕
            return False  # 返回F指令，表示本对象已经木大了
        return True  # 否则，返回T指令，表示本对象还活着


class 子弹():
    '''管理陨石的类，参与碰撞。'''
    # 本类只储存物理参数，不负责图形绘制

    def __init__(self, x, y, s, mx):
        '''初始化，传入初始位置xy，速度s，屏幕最右端mx'''
        self.X, self.Y, self.Speed, self.MaxX = x, y, s, mx + 10

    def 刷新函数(self):
        '''进行一帧的刷新'''
        self.X = self.X + self.Speed
        if(self.X > self.MaxX):  # 当位置完全飞出屏幕
            return False  # 返回F指令，表示本对象已经木大了
        return True  # 否则，返回T指令，表示本对象还活着


def 圆碰撞检测函数(x1, y1, r1, x2, y2, r2):  # 圆和圆的碰撞检测
    x = x1 - x2
    x *= x
    y = y1 - y2
    y *= y
    r = r1 + r2  # 计算两点距离的平方，若小于半径和的平方则碰撞
    r *= r
    # print("距离" + str(x + y) + ",半径和" + str(r))
    return x + y < r


def 点碰撞检测函数(x1, y1, r, x2, y2):  # 圆和点的碰撞检测
    x = x1 - x2
    x *= x
    y = y1 - y2
    y *= y
    r *= r
    # print("距离" + str(x + y) + ",半径和" + str(r))
    return x + y < r


class 主场景():
    '''游戏主场景的类'''

    def __init__(self):
        #  ==================== 初始化pygame ====================
        pygame.init()  # 初始化pygame
        self.SizeX = 400  # 设置窗口大小
        self.SizeY = 300
        self.Screen = pygame.display.set_mode((self.SizeX, self.SizeY))  # 注册窗口
        pygame.display.set_caption("Pygame随机圆")
        #  ==================== 初始化数据结构 ====================
        self.运行 = True  # 标记程序运行状态，为F时终止所有线程
        self.粒子列表 = []  # 这个列表储存了所有粒子对象
        self.生成一波星函数()
        星线程 = threading.Thread(target=self.不断生成星函数)
        星线程.start()
        self.陨石列表 = []
        陨石线程 = threading.Thread(target=self.不断生成陨石函数)
        陨石线程.start()
        self.子弹列表 = []
        #  ==================== 初始化自机及玩家控制 ====================
        self.CtrlW = False  # 控制输入键值
        self.CtrlS = False
        self.CtrlA = False
        self.CtrlD = False
        self.CtrlFire = False
        self.PlayerX = 50  # 自机当前位置
        self.PlayerY = self.SizeY // 2
        self.PlayerR = 20  # 自机碰撞域大小
        self.PlayerSpeedX = 4
        self.PlayerSpeedY = 6
        self.FireCd = 0  # 距离下一次开火的时间(帧)
        self.FireCdTime = 3  # cd间隔
        self.Hp = 3  # 生命值
        self.Score = 0  # 积分
        self.提示时间 = 100
        #  ==================== 初始化文字 ====================
        self.Text = pygame.font.SysFont('微软雅黑', 30)
        print("执行")
        while True:
            if self.刷新函数() == False:
                break
            time.sleep(0.05)
        # 退出循环，说明玩家挂掉了
        t1 = self.Text.render(("YOU DIED !"), 1, (255, 0, 0))
        self.Screen.blit(t1, (self.SizeX // 2 - 55, self.SizeY // 2 - 30))
        t1 = self.Text.render((f"SCORE: {self.Score}"), 1, (255, 0, 0))
        self.Screen.blit(t1, (self.SizeX // 2 - 55, self.SizeY // 2 + 20))
        t2 = self.Text.render(("please close the window"), 1, (255, 255, 255))
        self.Screen.blit(t2, (self.SizeX // 2 - 120, self.SizeY // 2 + 60))
        pygame.display.update()
        while True:
            for event in pygame.event.get():  # 等待关闭窗口事件
                if event.type == QUIT:
                    sys.exit()

    def 刷新函数(self):
        '''执行一次刷新'''
        # ==================== 事件接收 ====================
        for event in pygame.event.get():
            # 关闭窗口事件
            if event.type == QUIT:
                print("关闭")
                self.运行 = False  # 设运行标志为F
                sys.exit()
            # 键盘按下事件
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.CtrlA = True
                elif event.key == K_RIGHT:
                    self.CtrlD = True
                elif event.key == K_UP:
                    self.CtrlW = True
                elif event.key == K_DOWN:
                    self.CtrlS = True
                elif event.key == K_SPACE:
                    self.CtrlFire = True
                elif event.key == K_r:
                    self.运行 = False  # 设运行标志为F
                    return False  # 退出无限循环
            # 键盘松开事件
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.CtrlA = False
                elif event.key == K_RIGHT:
                    self.CtrlD = False
                elif event.key == K_UP:
                    self.CtrlW = False
                elif event.key == K_DOWN:
                    self.CtrlS = False
                elif event.key == K_SPACE:
                    self.CtrlFire = False
        # ==================== 玩家控制 ====================
        if self.CtrlW:
            self.PlayerY -= self.PlayerSpeedY
        elif self.CtrlS:
            self.PlayerY += self.PlayerSpeedY
        if self.PlayerY < 0:
            self.PlayerY = 0
        elif self.PlayerY > self.SizeY:
            self.PlayerY = self.SizeY
        if self.CtrlA:
            self.PlayerX -= self.PlayerSpeedX
        elif self.CtrlD:
            self.PlayerX += self.PlayerSpeedX
        if self.PlayerX < 0:
            self.PlayerX = 0
        elif self.PlayerX > self.SizeX:
            self.PlayerX = self.SizeX
        if self.FireCd <= 0:  # 开火cd好了
            if self.CtrlFire:
                self.FireCd = self.FireCdTime
                self.生成一个子弹函数(self.PlayerX, self.PlayerY)
        else:  # cd没好，刷新cd
            self.FireCd -= 1
        # ==================== 绘制 ====================
        self.Screen.fill((0, 0, 50))  # 填充背景色，相当于清屏
        # 遍历、刷新、并绘制粒子列表
        for i in self.粒子列表:
            if(i.刷新函数() == False):  # 刷新返回F指令，表示这个对象木大了。删除它
                self.粒子列表.remove(i)  # 将i移出列表(但此时并没有删除它)
                del i  # 删除i本身
            else:  # 刷新返回T指令，表示这个对象正常。绘制它
                pygame.draw.circle(self.Screen, i.Color, (i.X, i.Y), i.R)
        # 遍历、刷新、碰撞检测、并绘制陨石列表
        for i in self.陨石列表:
            if(i.刷新函数() == False):
                self.陨石列表.remove(i)
                del i
            elif(圆碰撞检测函数(i.X, i.Y, i.R, self.PlayerX, self.PlayerY, self.PlayerR)):
                # print("碰撞命中！！！")
                self.Hp -= 1
                if self.Hp <= 0:
                    print("退出循环")
                    self.运行 = False  # 设运行标志为F
                    return False  # 退出无限循环
                self.陨石列表.remove(i)
                del i
            else:
                pygame.draw.circle(self.Screen, i.Color, (i.X, i.Y), i.R)
        # 遍历、刷新、碰撞检测、并绘制子弹列表
        for i in self.子弹列表:
            if(i.刷新函数() == False):
                self.子弹列表.remove(i)
                del i
            else:
                flag = True
                for ii in self.陨石列表:  # 遍历陨石列表
                    if(点碰撞检测函数(ii.X, ii.Y, ii.R, i.X, i.Y)):
                        ii.Hp -= 1  # 陨石扣血
                        if ii.Hp <= 0:  # 陨石没血，删除陨石
                            self.陨石列表.remove(ii)
                            self.Score += 1
                            del ii
                        else:  # 还有血，用红色重绘命中陨石
                            pygame.draw.circle(
                                self.Screen, (255, 0, 0), (ii.X, ii.Y), ii.R)
                        self.子弹列表.remove(i)  # 删除子弹
                        del i
                        flag = False
                        break
                if flag:
                    pygame.draw.rect(self.Screen, (230, 255, 0),
                                     (i.X - 3, i.Y - 1, 6, 2))
        # 绘制玩家
        self.绘制自机(self.PlayerX, self.PlayerY)
        # 绘制文字
        t = self.Text.render((f"HP:{str(self.Hp)}"), 1, (255, 0, 0))
        self.Screen.blit(t, (self.SizeX - 55, 4))
        t = self.Text.render((f"SC:{str(self.Score)}"), 1, (150, 150, 255))
        self.Screen.blit(t, (5, 4))
        if self.提示时间 > 0:
            t = self.Text.render(
                ("Move: Up Down Left Right, Fire: Space"), 1, (255, 255, 255))
            self.Screen.blit(t, (10, self.SizeY - 20))
            self.提示时间 -= 1
        # 刷新屏幕
        pygame.display.update()
        return True

    def 绘制自机(self, x, y):
        # 绘制舰体中段长方形
        pygame.draw.rect(self.Screen, (176, 194, 255), (x - 18, y - 3, 20, 6))
        # 绘制舰体后段连接处长方形
        pygame.draw.rect(self.Screen, (176, 194, 255), (x - 18, y - 10, 4, 20))
        # 绘制舰体后段连接处双引擎
        pygame.draw.rect(self.Screen, (243, 247, 166), (x - 27, y - 11, 18, 3))
        pygame.draw.rect(self.Screen, (243, 247, 166), (x - 27, y + 8, 18, 3))
        # 绘制舰体头部椭圆
        pygame.draw.ellipse(self.Screen, (212, 239, 255),
                            (x - 5, y - 13, 30, 26))
        # 绘制中心点及碰撞域
        # pygame.draw.circle(self.Screen, (255, 0, 0), (x, y), 1, 1)
        # pygame.draw.circle(self.Screen, (255, 255, 255), (x, y), self.PlayerR, 1)

    def 生成一个星函数(self, x=-1):  # x不填参数时为指令值：-1
        if(x == -1):  # 若x为指令值-1，则x固定在屏幕最右边以外
            x = self.SizeX + 50
        elif(x == 1):  # 若x为指令值1，则随机一个x
            x = random.randint(0, self.SizeY)  # y值随机
        y = random.randint(0, self.SizeY)  # y值随机
        r = random.randint(1, 3)  # 随机大小
        self.粒子列表.append(粒子(x, y, r, (100, 100, 100), (-3, 0)))

    def 不断生成星函数(self):
        剩余时间 = 0  # 储存距离下一次生成的剩余时间
        生成帧 = 0.1  # 记录本线程每隔多久刷新一次
        while self.运行:   # 每隔"生成帧"检查一次运行标志，若为F时退出循环，终止本子线程
            if(剩余时间 <= 0):  # 到时间，调用生成
                self.生成一个星函数()  # 不填参数：指令值-1（固定x值）
                剩余时间 = random.uniform(0.1, 0.8)  # 记录一段新的生成时间(随机)
            else:
                剩余时间 -= 生成帧
            time.sleep(生成帧)

    def 生成一波星函数(self):
        for i in range(random.randint(6, 16)):
            self.生成一个星函数(1)  # 填入参数：指令值1（随机x值）

    def 生成一个陨石函数(self):
        r = random.randint(10, 40)  # 随机大小
        x = self.SizeX + r
        y = random.randint(-100, self.SizeY + 100)  # y值随机
        s = (random.randint(-10, 0), random.randint(-4, 4))
        c = (random.randint(150, 255), random.randint(
            50, 200), random.randint(0, 100))
        h = random.randint(3, 10)
        self.陨石列表.append(陨石(x, y, r, c, s, h))

    def 不断生成陨石函数(self):
        剩余时间 = 0
        生成帧 = 0.1
        while self.运行:
            if(剩余时间 <= 0):
                self.生成一个陨石函数()
                剩余时间 = random.uniform(0.1, 0.8)
            else:
                剩余时间 -= 生成帧
            time.sleep(生成帧)

    def 生成一个子弹函数(self, x, y):
        self.子弹列表.append(子弹(x, y, 10, self.SizeX))


if __name__ == "__main__":
    主场景()
