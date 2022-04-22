// 碰撞管理

cc.Class({
    extends: cc.Component,

    properties: {
        label3: { type: cc.Label, default: null, displayName: "文字显示3" },
    },

    // LIFE-CYCLE CALLBACKS:

    onLoad() {
        // 获取碰撞检测系统
        var manager = cc.director.getCollisionManager();
        // 开启碰撞检测系统
        manager.enabled = true;
        // 开启 debug 绘制：
        manager.enabledDebugDraw = true;
        // 开启碰撞box显示
        manager.enabledDrawBoundingBox = true;

        this.label3.string = "";
    },

    start() {

    },

    // 碰撞发生
    onCollisionEnter: function (other, self) {
        this.label3.string = "[" + self.node.name + "]与[" + other.node.name + "]发生碰撞";
    },

    // 碰撞结束
    onCollisionExit: function (other, self) {
        this.label3.string = "";
    }
});
