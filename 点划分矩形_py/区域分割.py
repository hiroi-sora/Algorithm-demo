from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import threading  # 线程
import time
import random  # 随机数

OutputScreenList = []  # 输出点列表
isDraw = False  # 标记当前是否需要刷新
rectangle = [1000, 600]  # 长方形
workPoints = [  # 工作点列表。[ x,y,[color] ]
    [0, 0, [0, 0, 1]],
    [800, 0, [0, 0.5, 0.5]],
    [500, 300, [0.5, 0.5, 0]],
    [300, 500, [1, 0, 0]],
    [950, 550, [0, 1, 0]],
]

'''
1000 600
0 0
1000 0
500 600
ok

1000 600
0 0
0 600
1000 0
1000 600
500 300
ok

1100 600
30 70
450 100
670 550
990 400
60 500
ok

1100 700
random 10
ok

1100 700
random 5
ok

'''

sizeX, sizeY = map(int, input('输入矩形区域的 长 宽 ：\n').split())
rectangle = [sizeX, sizeY]
workPointsLen = 1
print("依次输入每个目标点的 x y 坐标。")
print("结束请输入“ok”。")
print("若要添加随机点，请输入“random 个数”。")
workPoints = []
while True:
    print('第', workPointsLen, '个目标点：')
    strIn = input()
    if strIn == 'ok' or strIn == 'OK':
        break
    if 'random' in strIn:
        nList = strIn.split()
        n = int(nList[1])
        print("添加了", n, "个随机点，分别为：")
        for i in range(n):
            pX, pY = random.randint(
                0, rectangle[0]), random.randint(0, rectangle[1])
            pC = [random.uniform(0.1, 1), random.uniform(
                0.1, 1), random.uniform(0.1, 1)]
            workPoints.append([pX, pY, pC])
            print(pX, ' ', pY)
            workPointsLen += 1
        continue
    pX, pY = map(int, strIn.split())
    pC = [random.random(), random.random(), random.random()]
    workPoints.append([pX, pY, pC])
    workPointsLen += 1
# print("地图：", rectangle)
# print("工作点 ", workPoints)


def work():
    global isDraw
    print("主要计算开始！")
    # 描边
    # for i in range(rectangle[0]):
    #     addPoint(i, -7)
    #     addPoint(i, -8)
    #     addPoint(i, rectangle[1]+7)
    #     addPoint(i, rectangle[1]+8)
    # for i in range(rectangle[1]):
    #     addPoint(-7, i)
    #     addPoint(-8, i)
    #     addPoint(rectangle[0]+7, i)
    #     addPoint(rectangle[0]+8, i)
    timeStart = time.perf_counter()
    for y in range(rectangle[1]):
        for x in range(rectangle[0]):
            # 初始化最近距离
            minPoi = -1
            minLen2 = len2 = getLen2(
                0, 0, rectangle[0], rectangle[1])
            # 遍历工作点集，求距离最近
            for p in range(len(workPoints)):
                len2 = getLen2(
                    x, y, workPoints[p][0], workPoints[p][1])
                if len2 < minLen2:
                    minLen2 = len2
                    minPoi = p
            # 记录最近距离。将最近的工作点的颜色添加进当前屏幕点
            if not minPoi == -1:
                addPoint(x, y, workPoints[minPoi][2])
            # if y > rectangle[1]*0.4:
            #     time.sleep(0.01)
            # isDraw = True
    # 记录时间
    timeEnd = time.perf_counter()
    timeSpend = timeEnd - timeStart
    print("主要计算完成，耗时", timeSpend, "秒。\n请稍等绘图完成。")
    # 标记点
    pl = 40
    for p in workPoints:
        for i in range(0, pl+1):
            addPoint(p[0]-0.5*pl+i, p[1]-0.5*pl+i)
            addPoint(p[0]-0.5*pl+i, p[1]+0.5*pl-i)
    isDraw = True


def getLen2(x1, y1, x2, y2):
    xx = x1-x2
    yy = y1-y2
    return xx*xx+yy*yy
# (x1-x2)²+(y1-y2)²


def addPoint(x, y, color=[1, 1, 1], scale=0.03, deviation=[-15, -10]):
    '''添加一个点'''
    global OutputScreenList
    x = x*scale+deviation[0]
    y = y*scale+deviation[1]
    OutputScreenList.append([x, y, color])


def Update():
    glutPostRedisplay()  # 标记当前窗口需要重新绘制


def drawPoint():
    '''绘制所有点'''
    glPointSize(2)  # 指定点的大小
    glBegin(GL_POINTS)  # 开始定制多个点
    for i in range(len(OutputScreenList)):  # 遍历点集列表
        glColor3f(OutputScreenList[i][2][0], OutputScreenList[i]
                  [2][1], OutputScreenList[i][2][2])  # 指定颜色
        glVertex2f(OutputScreenList[i][0], OutputScreenList[i][1])  # 绘制
    glEnd()  # 结束一次定制


def Draw():
    global isDraw
    if not isDraw:
        return
    isDraw = False
    glClear(GL_COLOR_BUFFER_BIT)  # 擦除屏幕
    drawPoint()
    glutSwapBuffers()  # 刷新缓冲。glFlush/glutSwapBuffers 适用于单/双缓冲
    # print("绘制！")


def drawTest():
    pass


def Reshape(w, h):
    '''窗口调整大小事件'''
    wh = w / 1 if h == 0 else h  # 新窗口的宽高比。h为0时除数为1。
    w2, h2 = w / 2, 1 if h == 0 else h / 2  # h2不为0
    glViewport(0, 0, w, h)  # 设置视口 铺满整个窗口
    glMatrixMode(GL_PROJECTION)  # 在Projection矩阵上操作
    glLoadIdentity()  # 重置投影矩阵
    cantre = (1, 0)
    scale = 20
    gluOrtho2D((cantre[0] - w2) / scale, (cantre[0] + w2) /
               scale, (cantre[1] - h2) / scale, (cantre[1] + h2) / scale)


def initOpenGL():
    '''初始化OpenGL'''
    glutInit()
    # 指定显示模式的类型。GLUT_SINGLE/GLUT_DOUBLE 单/双缓冲
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(800, 500)
    # glutInitWindowPosition(0, 0)
    glutCreateWindow("Fenge")
    # 注册一个绘图函数
    glutDisplayFunc(Draw)
    # 注册全局的回调函数
    glutIdleFunc(Update)
    # 注册窗口重新调整事件的回调处理程序
    glutReshapeFunc(Reshape)
    # 设置擦除颜色
    glClearColor(0, 0, 0, 0)
    # 进入GLUT事件处理循环
    glutMainLoop()
    print("opengl初始化完毕。")


def main():
    '''程序入口'''
    # workThread = threading.Thread(target=work)  # 工作线程
    # workThread.setDaemon(True)  # 设置为守护线程，即它工作完后主线程才退出
    # workThread.start()  # 开始活动
    work()
    initOpenGL()  # 初始化并开始运行绘图


if __name__ == "__main__":
    main()
