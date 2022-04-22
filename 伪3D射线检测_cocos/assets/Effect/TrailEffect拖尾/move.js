// 简单的移动

cc.Class({
    extends: cc.Component,

    properties: {
    },

    // LIFE-CYCLE CALLBACKS:

    onLoad() {
        this.t = 0;
    },

    // start() {

    // },

    update(dt) {
        this.t += dt;
        // this.node.x = Math.sin(this.t) * 10;
        // this.node.y = Math.sin(this.t * 0.5) * 10;
        // this.node.z = Math.sin(this.t * 3) * 2;
    },
});
