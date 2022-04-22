// 拖尾特效的脚本

// 储存一些属性
var startColor = "startColor";

cc.Class({
    extends: cc.Component,

    properties: {
        target: { type: cc.Node, default: null, displayName: "跟随节点" },
        debug: { type: cc.Label, default: null, displayName: "debug输出" },
    },

    onLoad() {
        // 初始化数据
        this.level = 5; // 柔化等级，即网格的层数
        this.soft = 5;// 拖尾的柔软度，值越大尾巴越柔软，拉伸的越长
        this.startPosition = cc.v3(0, 0, 0); // 起始坐标
        this._playing = false; // 是否在播放的标志
        this.followAngle = true; // 跟随目标角度
        // 初始化网格
        this.meshRenderer = this.node.getComponent(cc.MeshRenderer); // 获取网格渲染器组件
        this.mat = this.meshRenderer.getMaterial(0); // 获取渲染器的第一个材质
        this.setShape(); // 设置横截面形状
        this.setTarget(); // 设置跟随目标

        // let c = [1, 0, 0, 1];
        // this.mat.setProperty(startColor, c);
        cc.log("拖尾脚本初始化完毕");
    },

    // 设置横截面形状。逆时针，默认无需(不要)闭合。
    setShape() {
        this.polygon = [cc.v2(-0.5, -0.5), cc.v2(0.5, -0.5), cc.v2(0, 0.5)];
        // cc.log("顶点数组长度：" + this.polygon.length + "," + this.polygon[2].toString());
        this.createVerts(); // 根据截面形状和拖尾位置创建网格顶点
        this.createMesh(); // 创建网格数据
    },

    // 根据截面形状和拖尾位置创建网格顶点
    createVerts() {
        //顶点的Z轴偏移为0
        this.verts = []; // 实际分好组的顶点数组
        let nPolygon = this.polygon.length;
        for (let i = 0; i <= this.level; ++i) { // 循环柔化等级的数量
            for (let j = 0; j < nPolygon; ++j) { // 循环横截面形状的顶点数量
                // 将初始坐标的横截面形状上的顶点坐标加入verts数组
                this.verts.push(cc.v3(this.polygon[j].x, this.polygon[j].y, 0).addSelf(this.startPosition));
            }
            // 加完一批横截面形状顶点后，加入一个始起点坐标，使其成为封闭图形
            this.verts.push(cc.v3(this.polygon[0].x, this.polygon[0].y, 0).addSelf(this.startPosition));
        }
    },

    // 创建网格数据
    createMesh() {
        // let gfx = cc.renderer.renderEngine.gfx;
        let gfx = cc.gfx;
        // 定义顶点数据格式，只需要指明所需的属性，避免造成存储空间的浪费
        var vfmtPosColor = new gfx.VertexFormat([ // 点颜色
            // 用户需要创建一个三维的盒子，所以需要三个值来保存位置信息
            { name: gfx.ATTR_POSITION, type: gfx.ATTR_TYPE_FLOAT32, num: 3 }, // 位置属性
            { name: gfx.ATTR_UV0, type: gfx.ATTR_TYPE_FLOAT32, num: 2 }, // UV属性
            { name: gfx.ATTR_COLOR, type: gfx.ATTR_TYPE_UINT8, num: 4, normalize: true }, // 颜色属性，开启规范化
        ]);
        this.mesh = new cc.Mesh(); // 创建个网格文件
        this.meshRenderer.mesh = this.mesh; // 节点的网格渲染器的网格设为刚创建的网格

        let mesh = this.mesh; // 简写
        // 初始化网格信息
        mesh.init(vfmtPosColor, this.verts.length, true);
        // 根据顶点数组，修改 position 顶点数据
        mesh.setVertices(gfx.ATTR_POSITION, this.verts);
        // 修改 color 顶点数据
        let colors = [];
        for (let i = 0, c = this.verts.length; i < c; ++i) {
            colors.push(cc.Color.WHITE); // 每个顶点初始为白色
        }
        mesh.setVertices(gfx.ATTR_COLOR, colors);
        // 修改 uv 顶点数据
        let uv = [];
        let nPolygon = this.polygon.length;
        for (let i = 0; i <= this.level; ++i) { // 循环柔化等级次数
            let uv_x = 1 - i / this.level; // uv_x逐渐降低
            for (let j = 0; j <= nPolygon; ++j) { // 循环截面顶点次数
                uv.push(cc.v2(uv_x, j / nPolygon)); // 将uv_x和当前顶点/总顶点 加入uv数组
            }
        }
        mesh.setVertices(gfx.ATTR_UV0, uv);

        // 修改索引数据
        let frag = [];
        let p2 = nPolygon + 1; // 截面顶点+1
        let p3 = nPolygon + 2; // 截面顶点+2
        for (let i = 0; i < this.level; ++i) { // 循环柔化等级次数
            for (let j = 0; j < nPolygon; ++j) { // 循环截面顶点次数
                let index = i * nPolygon + i + j;
                frag.push(index, index + 1, index + p3);
                frag.push(index, index + p3, index + p2);
            }
        }
        mesh.setIndices(frag);
    },

    // 设置要跟随的目标，
    setTarget() {
        // 目标节点
        // this.target = target;
        // 拖尾中心点相对目标节点的坐标的偏移量
        this.offset = cc.v3(0, 0, 0);
    },


    start() {
        let v = cc.v3(10, 10, 10);
        this.play(cc.v3(this.target.x, this.target.y, 0)); // 开始播放



    },

    // 从指定的坐标开始播放
    play(startPosition) {
        if (this.polygon.length == 0) {
            cc.warn("拖尾特效未设置横截面形状！");
            return;
        }
        if (!this.target) {
            cc.warn("拖尾未设置跟随的目标节点！");
            return;
        }
        this._playing = true;
        this.startPosition.set(startPosition); // 设置起始坐标为指定
        this.resetMesh();
        cc.log("开始播放拖尾特效！");
    },

    // 重置网格数据
    resetMesh() {
        let nPolygon = this.polygon.length;
        for (let i = 0; i <= this.level; ++i) {
            for (let j = 0; j < nPolygon; ++j) {
                this.verts[i * nPolygon + i + j].set(cc.v3(this.polygon[j].x, this.polygon[j].y, 0).addSelf(this.startPosition));
            }
            this.verts[i * nPolygon + i + nPolygon].set(cc.v3(this.polygon[0].x, this.polygon[0].y, 0).addSelf(this.startPosition));
        }
        let gfx = cc.gfx;
        this.mesh.setVertices(gfx.ATTR_POSITION, this.verts);
    },

    update(dt) {
        if (!this._playing || !this.target) return; // 不播放或无目标则不更新
        let pos = cc.v3();
        this.target.getPosition(pos); // 获取目标当前坐标
        pos.addSelf(this.offset); // 加上偏移量
        if (!this.followAngle) {
            this.moveTo(pos);
        } else {
            this.moveTo(pos, this.target.eulerAngles);
        }



        // let gfx = cc.gfx;
        // let p = [cc.v3(0, 0, 100 * Math.random()), cc.v3(10, 10, 0), cc.v3(-10, 10, 100)];
        // this.mesh.setVertices(gfx.ATTR_POSITION, p);
        // cc.log("up" + p[0].z);

    },

    // 移动到
    moveTo(pos, angle) {
        this.startPosition = pos;
        let maxIndex = this.polygon.length - 1; // 横截面顶点数
        if (undefined === angle) {
            for (let i = maxIndex; i >= 0; --i) {
                // 分组的实际顶点数组，赋值为，开始坐标加顶点坐标(在空间中产生一组顶点)
                this.verts[i].x = this.startPosition.x + this.polygon[i].x;
                this.verts[i].y = this.startPosition.y + this.polygon[i].y;
                this.verts[i].z = this.startPosition.z;
            }
            maxIndex++;
            this.verts[maxIndex].x = this.startPosition.x + this.polygon[0].x;
            this.verts[maxIndex].y = this.startPosition.y + this.polygon[0].y;
            this.verts[maxIndex].z = this.startPosition.z;
        } else {
            for (let i = maxIndex; i >= 0; --i) {
                let offset = cc.v3(this.polygon[i].x, this.polygon[i].y, 0);
                offset = this.rotatePos(offset, angle); // 将一个三维向量旋转角度
                this.verts[i].x = this.startPosition.x + offset.x;
                this.verts[i].y = this.startPosition.y + offset.y;
                this.verts[i].z = this.startPosition.z + offset.z;
            }
            maxIndex++;
            let offset = cc.v3(this.polygon[0].x, this.polygon[0].y, 0);
            offset = this.rotatePos(offset, angle);
            this.verts[maxIndex].x = this.startPosition.x + offset.x;
            this.verts[maxIndex].y = this.startPosition.y + offset.y;
            this.verts[maxIndex].z = this.startPosition.z + offset.z;
        }
        this.updateMesh(); // 更新网格形状
        // cc.log("正在移动拖尾" + pos.toString());
    },

    // 将一个三维向量旋转三个角度
    rotatePos(p, angle) {
        //旋转顺序：Y-X-Z
        let p1 = cc.v2(p.x, p.z);
        this.rotateV2(p1, angle.y);
        let p2 = cc.v2(p.y, p1.y);
        this.rotateV2(p2, angle.x);
        let p3 = cc.v2(p1.x, p2.x);
        this.rotateV2(p3, angle.z);
        p.x = p3.x;
        p.y = p3.y;
        p.z = p2.y;
        return p;
    },
    // 将一个二维向量旋转一个角度
    rotateV2(p, angle) {
        let radian = angle * 0.017453; // 角度转弧度，低精度高效
        let sin = Math.sin(radian);
        let cos = Math.cos(radian);
        let x = p.x;
        let y = p.y;
        p.x = x * cos - y * sin;
        p.y = x * sin + y * cos;
    },

    // 更新网格形状
    updateMesh() {
        let rate = this.soft == 0 ? 0.2 : (1 / this.soft); // 根据柔软度设置
        let nPolygon = this.polygon.length;
        let offset = nPolygon + 1;
        for (let i = 1; i <= this.level; ++i) {
            let index = i * offset;
            for (let j = 0; j <= nPolygon; ++j) {
                let previousVert = this.verts[index - offset + j];
                let nextVert = this.verts[index + j];
                this.interpolationPos(nextVert, previousVert, rate);
            }
        }

        // let p = [cc.v3(0, 0, 1000 * Math.random()), cc.v3(10, 10, 0), cc.v3(-10, 10, 100)];

        let gfx = cc.gfx;
        this.mesh.setVertices(gfx.ATTR_POSITION, this.verts);

        // this.debug.string = this.verts[1].toString() + "," + this.verts[2].toString();
    },
    interpolationPos(p1, p2, rate) { // 两个v3根据rate插值
        p1.x += this.getInterpplation(p1.x, p2.x, rate);
        p1.y += this.getInterpplation(p1.y, p2.y, rate);
        p1.z += this.getInterpplation(p1.z, p2.z, rate);
    },
    getInterpplation(a, b, r) { // 对两个数插值
        return (b - a) * r;
    },
});

    // // 初始化，现在暂时不需要
    // init() {
    //     this.initPosition(); // 初始化位置
    //     this.initPolygon(); // 初始化多边形，暂时无用
    //     this.initMat(); // 初始化网格
    // },

    // // 初始化位置
    // initPosition() {
    //     this.startPosition = cc.v3(0, 0, 0);
    // },

    // // 初始化多边形：TODO……

    // // 初始化网格
    // initMat() {
    //     this.mat = this.meshRenderer.getMaterial(0);
    //     let c = [this.startColor.r / 255, this.startColor.g / 255, this.startColor.b / 255, this.startColor.a / 255];
    //     this.mat.setProperty(startColor, c);
    //     c = [this.endColor.r / 255, this.endColor.g / 255, this.endColor.b / 255, this.endColor.a / 255];
    //     this.mat.setProperty(endColor, c);
    //     if (!!this.diffuseTexture) {
    //         this.mat.setProperty(diffuseTexture, this.diffuseTexture);
    //     }
    // }