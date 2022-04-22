# 无需物理组件的3d触摸选择 / 摄像机射线检测

[原帖（本人发的）](https://forum.cocos.org/t/3d/95686)

> 本demo使用 cocos creator 引擎

![](https://tupian.li/images/2022/04/22/-1f680da5c6f8414bd.gif)

本算法适用于伪3d游戏，即游戏所有逻辑判断、碰撞检测都是在2d平面上进行，但物体节点上挂载了3d模型，使用透视摄像机观察画面。

很多俯视角游戏、某些卡牌类、横板类都可以是伪3d，既有3d效果的华丽，也从逻辑判定上砍掉一个z轴而节省不少性能。

在3d环境下，触摸屏幕点选物体，一般用射线检测，从3d摄像机向触点发射一条射线，康康命中了什么物体。cocos需要启用物理组件和让节点挂载物理碰撞体才能被射线检测。但我有一个轻量的项目，既不需要物理系统，也不需要3d碰撞体。仅仅为了触摸检测而开物理就太亏了。于是稍微改了下传统射线检测的算法，写了个在轻量级伪3d环境下可用的触摸检测。原理很简单，

首先一个空节点拉满屏幕，接收触摸输入：
![](https://tupian.li/images/2022/04/22/3d-1.png)

触摸板节点挂载脚本，注册触摸按下、移动、离开的监听；获取3d摄像机组件。当触摸按下时，生成一条从摄像机向触点的射线`camera.getRay()函数`，传递给后面的功能函数。

```js
onLoad() {
    // 注册本节点的触摸监听
    this.node.on(cc.Node.EventType.TOUCH_START, this.touchOn, this);
    this.node.on(cc.Node.EventType.TOUCH_MOVE, this.touchMove, this);
    this.node.on(cc.Node.EventType.TOUCH_END, this.touchOff, this);
    this.node.on(cc.Node.EventType.TOUCH_CANCEL, this.touchOff, this);
    // 获取摄像机组件
    this.CCcamera = this.camera.getComponent(cc.Camera);
}

/*** 触摸监控 ***/
touchOn(event) { // 按下
    // 获取当前触点的位置
    let v2 = event.getLocation();
    // 获取一条从摄像机到触点的射线
    let ray = this.CCcamera.getRay(v2);
    // 传递给功能函数
    this.getRayPoint(ray);
},

touchOff() {…}, // 松开
touchMove(event) {…}, // 移动
```

随后，计算这条射线跟平面的交点。由于要做检测的平面是地面，即z高度为0、法线垂直xy；所以并不需要复杂的立体几何求交公式。

一条射线的参数包含了出发点和角度系数两个vec3。要获取该射线上的一个点，只需代入一个偏移量(即该点离出发点偏移了多远)；出发点(x,y,z)+角度系数(x,y,z)×偏移量=射线上的一个点(x,y,z)。

![](https://tupian.li/images/2022/04/22/3d-2.png)

求交的平面是地面，所以交点的z必然为0。因此单独抽出z值，推出偏移量t。然后将t代入原射线方程，得到与平面的交点p。

1. 出发.z + 角度.z * t = 0 ----> t = - (出发.z) / 角度.z
2. 交点(vec3) = 出发(vec3)+角度(vec3)×t
3. 取交点(vec3)的xy，即为在2d平面上的一个点(vec2)。

```js
// 获取射线与地面的交点
getRayPoint(ray) // 传入一条射线
{
    // 求出偏移系数t
    let t = (-ray.o.z) / (ray.d.z); // t=-o(z)/d(z)
    // 按照t偏移，得到目标点p
    let p = ray.o.add(ray.d.mul(t)); // p=o+d*t
},
```

然后判断这个2d坐标与什么物体碰撞就行了~~我是用一个节点作为“准星”，在上面挂载一个CircleCollider组件，半径调为0；平时禁用准星节点，碰撞发生时启用它 并把位置设置为交点坐标。哦还有，交点坐标是世界坐标；还得先用convertToNodeSpaceAR()转为节点坐标系。如果准星节点发生了碰撞，会通知给挂载的脚本。
（准星不一定要挂载个图片，空节点+圆形碰撞体就行了。）

![](https://tupian.li/images/2022/04/22/3d-3.png)

END.