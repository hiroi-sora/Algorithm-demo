// 3d转2dUI显示

cc.Class({
    extends: cc.Component,

    properties: {
        camera: { type: cc.Camera, default: null, displayName: "摄像机节点" },
        target: { type: cc.Node, default: null, displayName: "目标节点" },
        ui: { type: cc.Node, default: null, displayName: "UI节点" },
    },

    // LIFE-CYCLE CALLBACKS:

    onLoad() {
    },

    // start () {

    // },

    update(dt) {
        this.ui.position = cc.Canvas.instance.node.convertToNodeSpaceAR(this.camera.getWorldToScreenPoint(this.target.position)); // 
        cc.log(this.camera.getWorldToScreenPoint(this.target.position).toString());
    },
});
