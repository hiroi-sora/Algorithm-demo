## 说明

Python蚁群算法演示程序
![](https://tupian.li/images/2022/04/09/GIF-2022-4-9-11-07-20.gif)

## 准备

程序依赖OpenGL渲染，因此需要先安装pyOpenGL模块。

1. [在这里下载](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl) 对应python版本的两个安装包。以3.10为例，需要下载：
`PyOpenGL-3.1.6-cp310-cp310-win_amd64.whl`
`PyOpenGL_accelerate-3.1.6-cp310-cp310-win_amd64.whl`


2. 在下载好的文件夹，按住shift+右键，“在此处打开powershell窗口”。或打开控制台cd到此。

3. 安装这两个包。
```sh
pip install PyOpenGL-3.1.6-cp310-cp310-win_amd64.whl
pip install PyOpenGL_accelerate-3.1.6-cp310-cp310-win_amd64.whl
```

## 运行

启动 `main.py`

## 操作

##### 键盘：
`空格`：播放/暂停
`1`：开启/关闭快进
`2`：减少快进倍数
`3`：增加快进倍数
`4`：重置地图

##### 鼠标：
`左键拖拽`：移动地图视角
`滚轮`：缩放地图视角

## 开发说明

- `main.py`中修改键盘操作键位
- `ant.py`中修改蚂蚁信息素携带量和每帧释放量
- `manager.py`中修改家和食物位置
- `sceneMap.py`中修改每帧信息素减少量和地图大小

玩得开心~