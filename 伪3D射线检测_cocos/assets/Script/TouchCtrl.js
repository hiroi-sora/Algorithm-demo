// 触摸控制


cc.Class({
    extends: cc.Component,

    properties: {
        camera: { type: cc.Node, default: null, displayName: "摄像机节点" },
        star: { type: cc.Node, default: null, displayName: "准星节点" },
        label1: { type: cc.Label, default: null, displayName: "文字显示1" },
        label2: { type: cc.Label, default: null, displayName: "文字显示2" },
    },

    onLoad() {
        // 注册本节点的触摸监听
        this.node.on(cc.Node.EventType.TOUCH_START, this.touchOn, this);
        this.node.on(cc.Node.EventType.TOUCH_MOVE, this.touchMove, this);
        this.node.on(cc.Node.EventType.TOUCH_END, this.touchOff, this);
        this.node.on(cc.Node.EventType.TOUCH_CANCEL, this.touchOff, this);
        // 获取摄像机组件
        this.CCcamera = this.camera.getComponent(cc.Camera);
        // 关闭准星
        this.star.active = false;
        cc.log("加载完成");
    },
    onDestroy() {
        // 退出时取消监听
        this.node.off(cc.Node.EventType.TOUCH_START, this.touchOn, this);
        this.node.off(cc.Node.EventType.TOUCH_MOVE, this.touchMove, this);
        this.node.off(cc.Node.EventType.TOUCH_END, this.touchOff, this);
        this.node.off(cc.Node.EventType.TOUCH_CANCEL, this.touchOff, this);
    },

    // 触摸监控
    touchOn(event) { // 按下
        // 当前触点的位置
        let v2 = event.getLocation();
        // 激活准星
        this.star.active = true;
        // 获取一条射线
        let ray = this.CCcamera.getRay(v2);
        this.label1.string = "触点" + v2 + "；射线 始" + ray.o + "方向" + ray.d;
        this.getRayPoint(ray);
    },
    touchOff() { // 松开
        // 关闭准星
        this.star.active = false;
    },
    touchMove(event) { // 移动
        // 当前触点的位置
        let v2 = event.getLocation();
        // 获取一条射线
        let ray = this.CCcamera.getRay(v2);
        this.label1.string = "触点" + v2 + "；射线 始" + ray.o + "方向" + ray.d;
        this.getRayPoint(ray);
    },

    // 获取射线偏移一定距离后的点
    getRayPoint(ray) {
        // t是偏移系数，在射线上按照t偏移可以得到一个z=0的点，其xy值为咱所求。
        let t = (-ray.o.z) / (ray.d.z); // t=-o(z)/d(z) 
        // 按照t偏移，得到目标点p
        let p = ray.o.add(ray.d.mul(t)); // point=o+d*t
        this.label2.string = "映射世界坐标" + p.toString();
        // 移动准星
        this.moveStar(cc.v2(p.x, p.y));
    },

    // 移动准星~~输入世界坐标v2
    moveStar(v) {
        // 先将世界坐标v转换为canvas坐标系
        let v2 = this.node.convertToNodeSpaceAR(v);
        // 将转换后的坐标设置给准星节点
        this.star.setPosition(v2);
    },
});
