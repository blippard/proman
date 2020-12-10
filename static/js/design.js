let Snow = {
    el: "#snow",
    density: 10000,
    maxHSpeed: 5,
    minFallSpeed: 2,
    canvas: null,
    ctx: null,
    particles: [],
    colors: [],
    mp: 1,
    quit: false,
    init() {
        this.canvas = document.querySelector(this.el);
        this.ctx = this.canvas.getContext("2d");
        this.reset();
        requestAnimationFrame(this.render.bind(this));
        window.addEventListener("resize", this.reset.bind(this));
    },
    reset() {
        let contents = document.getElementById('contents');
        this.w = window.innerWidth;
        this.h = contents.clientHeight;

        this.canvas.width = this.w;
        this.canvas.height = this.h;
        this.particles = [];
        this.mp = Math.ceil(this.w * this.h / this.density);
        for (let i = 0; i < this.mp; i++) {
            let size = Math.random() * 4 + 5;
            this.particles.push({
                x: Math.random() * this.w,
                y: Math.random() * this.h,
                w: size,
                h: size,
                vy: this.minFallSpeed + Math.random(),
                vx: (Math.random() * this.maxHSpeed) - this.maxHSpeed / 2,
                fill: "#ffffff",
                s: (Math.random() * 0.2) - 0.1
            });
        }
    },

    render() {
        this.ctx.clearRect(0, 0, this.w, this.h);
        this.particles.forEach((p, i) => {
            p.y += p.vy;
            p.x += p.vx;
            this.ctx.fillStyle = p.fill;
            this.ctx.fillRect(p.x, p.y, p.w, p.h);
            if (p.x > this.w + 5 || p.x < -5 || p.y > this.h) {
                p.x = Math.random() * this.w;
                p.y = -10;
            }
        });
        if (this.quit) {
            return;
        }
        requestAnimationFrame(this.render.bind(this));
    }

};

Snow.init();

function lastChristmas() {
    let audio = document.getElementById('audio');
    let myAudio = document.createElement("audio");
    let play = false;
    audio.onclick = function () {
        myAudio.src = "/static/css/music/wham.mp3";
        if (play === false) {
            myAudio.play();
            play = true;
            audio.src = "/static/css/images/mute1.png";
        } else {
            myAudio.pause();
            myAudio.currentTime = 0;
            play = false;
            audio.src = "/static/css/images/audio.png";
        }
    }

}

lastChristmas();