let mouseDown = true

class Drawer {
    constructor(id, pixelPerMeter) {
        this.canvas = document.getElementById(id)
        this.ctx = this.canvas.getContext("2d")
        this.pixelPerMeter = pixelPerMeter
    }

    clearScreen() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawBoxes(50, "100, 100, 100, 1")
    }

    drawBall(centerX, centerY, radius, color) {
        centerX *= this.pixelPerMeter
        centerY *= this.pixelPerMeter
        radius *= this.pixelPerMeter
        let ctx = this.ctx
        ctx.fillStyle = "rgba(" + color + ")"
        ctx.beginPath()
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2, true)
        ctx.fill()
        ctx.closePath()
    }

    drawCircle(centerX, centerY, radius, color) {
        centerX *= this.pixelPerMeter
        centerY *= this.pixelPerMeter
        radius *= this.pixelPerMeter
        let ctx = this.ctx
        ctx.beginPath()
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2, true)
        ctx.lineWidth = 3
        ctx.strokeStyle = "rgba(" + color + ")"
        ctx.stroke()
        ctx.closePath()
    }

    drawLine(startPointX, startPointY, endPointX, endPointY, color) {
        let ctx = this.ctx
        ctx.beginPath()
        ctx.moveTo(startPointX, startPointY)
        ctx.lineTo(endPointX, endPointY)
        ctx.strokeStyle = "rgba(" + color + ")"
        ctx.stroke()
        ctx.closePath()
    }

    drawBoxes(color) {
        /* Vertical */
        for (let i = 0; i < this.canvas.height / this.pixelPerMeter; i ++) {
            let startX = 0
            let startY = i * this.pixelPerMeter
            let endX = this.canvas.width
            let endY = i * this.pixelPerMeter

            this.drawLine(startX, startY, endX, endY, color)
        }
        /* Horizontal */
        for (let i = 0; i < this.canvas.width / this.pixelPerMeter; i ++) {
            let startX = i * this.pixelPerMeter
            let startY = 0
            let endX = i * this.pixelPerMeter
            let endY = this.canvas.height

            this.drawLine(startX, startY, endX, endY, color)
        }
    }
}

class Satelite {
    constructor(x, y, radius, color) {
        this.x = x
        this.y = y
        this.radius = radius
        this.color = color
    }
}

class SateliteDrawer {
    constructor(id, size, pixelPerMeter) {
        this.drawer = new Drawer(id, pixelPerMeter)
        this.satelites = []
        this.size = size
        this.targetElem = -1
        this.pixelPerMeter = pixelPerMeter
        let selff = this
        this.drawer.canvas.onmouseup = e => {
            if (e.button === 0) {
                mouseDown = false
                selff.targetElem = -1
            }
        }
 
        this.drawer.canvas.onmousedown = e => {
            if (e.button === 0) {
                mouseDown = true
                let canvas = selff.drawer.canvas
                let rect = canvas.getBoundingClientRect()

                let mouseX = (e.clientX - rect.left) / this.pixelPerMeter
                let mouseY = (e.clientY - rect.top) / this.pixelPerMeter

                let minVal = -1
                for (let sat in selff.satelites) {
                    let satelite = selff.satelites[sat]
                    let distance = Math.sqrt((mouseX - satelite.x)**2 + (mouseY - satelite.y)**2)
                    if (distance < selff.size && (distance < minVal || minVal == -1)) {
                        selff.targetElem = sat
                        minVal = distance
                    }
                }
            }
        }

        this.drawer.canvas.onmousemove = e => {
            if (selff.targetElem !== -1) {
                let canvas = selff.drawer.canvas
                let rect = canvas.getBoundingClientRect()
                let mouseX = (e.clientX - rect.left) / this.pixelPerMeter
                let mouseY = (e.clientY - rect.top) / this.pixelPerMeter

                selff.satelites[selff.targetElem] = new Satelite(mouseX, mouseY, selff.satelites[selff.targetElem].radius, selff.satelites[selff.targetElem].color)
            }
        }
    }

    addSatelite(satelite) {
        this.satelites.push(satelite)
    }

    setSatelite(index, newSatelite) {
        this.satelites[index] = newSatelite
    }

    setSatelites(satelites) {
        this.satelites = satelites
    }

    setRadius(index, radius) {
        this.satelites[index].radius = radius
    }

    tick() {
        this.drawer.clearScreen()
        for (let sat in this.satelites) {
            let satelite = this.satelites[sat]
            this.drawer.drawBall(satelite.x, satelite.y, this.size, satelite.color)
            if (satelite.radius > 0) {
                this.drawer.drawCircle(satelite.x, satelite.y, satelite.radius, "0, 0, 0, 1")
            }
        }
    }
}

let vue = new Vue({
    el: '#app',
    data() {
        return {
            name: "Test",
            settings: {
                delay: 2,
                frequency: 10000,
                timeRecording: ""
            },
            error: {
                canvas: "Canvas couldnt be loaded"
            },
            satelites: null
        }
    },
    methods: {
        resizeCanvas(id) {
            let canvas = document.getElementById(id)
            canvas.width = canvas.offsetWidth
            canvas.height = canvas.offsetHeight
        },
    },
    created() {
        this.resizeCanvas("canvasDisplay")
        this.satelites = [new Satelite(3, 2.26, 1, "0, 0, 255, 0.4"), new Satelite(4, 4, 1, "0, 255, 0, 0.4"), new Satelite(2, 4, 1, "255, 0, 0, 0.4")]
    }
})

let sateliteDrawer = new SateliteDrawer("canvasDisplay", 0.3, 100)
setInterval(() => {
    sateliteDrawer.setSatelites(vue.satelites)
    sateliteDrawer.tick()
    console.log(vue.satelites)
}, 10)
