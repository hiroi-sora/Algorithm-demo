// 测试用。让摄像机移动

cc.Class({
    extends: cc.Component,
    update(dt) {
        this.node.angle += dt * 5;
    }
});
