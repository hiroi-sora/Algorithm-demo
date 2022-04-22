from manager import *
from sceneMap import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# from time import sleep


thisMouseStart = 0  # 本次鼠标拖动的起始参数。鼠标起始xy，地图中心起始xy。0=False=空
winW, winH = 500, 500  # 窗口的宽高
scale = 3  # 缩放倍率
cantre = (0, 0)  # 地图中心
isRun = False  # 标记播放
isFast = False  # 标记快进
fastNum = 100  # 快进倍数


def Draw():
    '''绘制'''
    glClear(GL_COLOR_BUFFER_BIT)  # 擦除屏幕
    sceneMap.draw(scale)
    manager.draw(scale)
    glutSwapBuffers()  # 刷新缓冲。glFlush/glutSwapBuffers 适用于单/双缓冲


def update():
    '''逻辑刷新'''
    sceneMap.update()  # 刷新地图
    manager.update()  # 刷新管理


def Update():
    '''总刷新'''
    if isRun:  # 播放
        update()
        if isFast:  # 快进
            for i in range(fastNum):
                update()
    glutPostRedisplay()  # 标记当前窗口需要重新绘制
    # sleep(0.2)
    # print("刷新！")


def Reshape(w, h):
    '''窗口调整大小事件'''
    global winW, winH
    winW, winH = w, h
    wh = w / 1 if h == 0 else h  # 新窗口的宽高比。h为0时除数为1。
    w2, h2 = w / 2, 1 if h == 0 else h / 2  # h2不为0
    glViewport(0, 0, w, h)  # 设置视口 铺满整个窗口
    glMatrixMode(GL_PROJECTION)  # 在Projection矩阵上操作
    glLoadIdentity()  # 重置投影矩阵
    gluOrtho2D((cantre[0] - w2) / scale, (cantre[0] + w2) /
               scale, (cantre[1] - h2) / scale, (cantre[1] + h2) / scale)


def onMouseClick(button, state, x, y):
    '''鼠标点击事件'''
    global thisMouseStart
    if button == 0 and state == 0:  # 按下左键
        thisMouseStart = ((x, y), cantre)  # 记录起始参数
    elif button == 0 and state == 1:  # 松开左键
        thisMouseStart = 0  # 覆盖参数
    # print("1 b", button, " s", state, " x", x, " y", y, " tm", thisMouseStart)


def onMouseWheel(button, state, x, y):
    '''鼠标滚轮事件'''
    global scale, cantre
    scale += state
    if scale <= 0:
        scale = 1
    Reshape(winW, winH)
    print("缩放倍数：", scale)
    # print("2 b", button, " s", state, " x", x, " y", y)


def onMouseClickMove(x, y):
    '''鼠标拖动事件'''
    if thisMouseStart:
        global cantre
        cantre = (-x + thisMouseStart[0][0] + thisMouseStart[1]
                  [0], y - thisMouseStart[0][1] + thisMouseStart[1][1])
        Reshape(winW, winH)
        # print("T x", x, " y", y, " tm", thisMouseStart)


def onKeyClick(key, x, y):
    '''键盘点击事件'''
    global isFast, fastNum, isRun, sceneMap, manager
    if key == b' ':
        isRun = not isRun  # 取反
        print("播放" if isRun else "暂停")
    elif key == b'1':
        isFast = not isFast
        print(f"开启快进，速率{fastNum}" if isFast else "关闭快进")
    elif key == b'2' and fastNum > 0:
        fastNum -= 1 if fastNum < 15 else 5  # 减少快进倍数
        print("快进倍数：", fastNum)
    elif key == b'3':
        fastNum += 1 if fastNum < 15 else 5
        print("快进倍数：", fastNum)
    elif key == b'4':  # 重置
        python = sys.executable
        os.execl(python, python, * sys.argv)
    # else:
    #     print("key ", key, " x", x, " y", y)


def initOpenGL():
    '''初始化OpenGL'''
    glutInit()
    # 指定显示模式的类型。GLUT_SINGLE/GLUT_DOUBLE 单/双缓冲
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(winW, winH)
    glutInitWindowPosition(300, 60)
    glutCreateWindow("Ant Colony Optimization demo")
    # 注册一个绘图函数
    glutDisplayFunc(Draw)
    # 注册全局的回调函数
    glutIdleFunc(Update)
    # 注册窗口重新调整事件的回调处理程序
    glutReshapeFunc(Reshape)
    # 设置擦除颜色
    glClearColor(0, 0, 0, 0)
    # glScaled(s, s, 1) # 缩放
    # 进入GLUT事件处理循环
    glutMouseFunc(onMouseClick)  # 注册鼠标点击事件
    glutMouseWheelFunc(onMouseWheel)  # 注册鼠标滚轮事件
    glutMotionFunc(onMouseClickMove)  # 注册鼠标拖动事件
    glutKeyboardFunc(onKeyClick)  # 注册键盘点击事件
    print("opengl初始化完毕。")
    print("按空格播放/暂停，按1进入/退出快进，2、3调整快进倍率，4重新生成地图。")
    print("左键拖拽地图，滚轮缩放地图。")
    glutMainLoop()


def main():
    '''程序入口'''
    initOpenGL()


if __name__ == "__main__":
    main()
