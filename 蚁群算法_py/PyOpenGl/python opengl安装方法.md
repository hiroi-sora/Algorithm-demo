1. 下载对应python版本的两个包。
`PyOpenGL-3.1.6-cp310-cp310-win_amd64.whl`
`PyOpenGL_accelerate-3.1.6-cp310-cp310-win_amd64.whl`
[下载地址](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl)

2. 在下载好的文件夹，按住shift+右键，“在此处打开powershell窗口”。或打开控制台cd到此。

3. 安装这两个包。
```sh
pip install PyOpenGL-3.1.6-cp310-cp310-win_amd64.whl
pip install PyOpenGL_accelerate-3.1.6-cp310-cp310-win_amd64.whl
```

- 测试是否安装好：茶壶demo

```python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def Draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(0.5, 0, 1, 0)
    glutWireTeapot(0.5)
    glFlush()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowSize(400, 400)
glutCreateWindow("test")
glutDisplayFunc(Draw)
glutIdleFunc(Draw)
glutMainLoop()
```