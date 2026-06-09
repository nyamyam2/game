import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="스트림릿 네온 배틀: 리밸런스", layout="centered")

st.title("⚔️ 스트림릿 2P 배틀: 리밸런스")
st.caption("캐릭터 크기 조정 및 사거리/공격 속도 밸런스 업데이트 완료!")

# 게임 로직 (HTML/JS)
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; background-color: #1a1a1a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; overflow: hidden; }
        canvas { background: #000; border: 3px solid #333; display: block; margin: 10px auto; box-shadow: 0 0 20px rgba(0,255,255,0.2); }
        .ui-overlay { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.85); 
                     padding: 30px; border: 2px solid #00f2ff; border-radius: 20px; width: 400px; z-index: 10; }
        .char-btn { padding: 15px; margin: 10px; cursor: pointer; border: none; border-radius: 10px; font-weight: bold; width: 120px; transition: 0.3s; }
        .main-btn { background: #1e90ff; color: white; }
        .miri-btn { background: #ff00ff; color: white; }
        .char-btn:hover { transform: scale(1.1); filter: brightness(1.2); }
        .restart-btn { background: #2ed573; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px; }
        .hidden { display: none; }
        .status-container { display: flex; justify-content: space-around; width: 800px; margin: 0 auto; font-size: 14px; color: #aaa; }
    </style>
</head>
<body>

    <div class="status-container">
        <div>1P: F(공격) / G(궁극기)</div>
        <div>2P: ↓(공격) / L(궁극기)</div>
    </div>

    <div id="select-screen" class="ui-overlay">
        <h2 id="select-title">1P 캐릭터 선택</h2>
        <button class="char-btn main-btn" onclick="selectChar('Main')">메인<br>(속공/근접)</button>
        <button class="char-btn miri-btn" onclick="selectChar('Mari')">마리<br>(초장거리)</button>
        <p style="font-size: 12px; color: #888; margin-top: 15px;">
            메인: 속도0.7s/범위8/궁10s<br>
            마리: 속도1.2s/범위20/궁12s
        </p>
    </div>

    <div id="result-screen" class="ui-overlay hidden">
        <h2 id="winner-text"></h2>
        <button class="restart-btn" onclick="resetGame()">다시하기 (Restart)</button>
    </div>

    <canvas id="gameCanvas" width="800" height="400"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        
        const GRID = 20; // 1칸 = 20px
        const GRAVITY = 0.6;
        
        let gameState = "SELECT";
        let p1Sel = null, p2Sel = null;

        const keys = {};
        window.addEventListener("keydown", (e) => { 
            keys[e.code] = true; 
            if(["Space", "ArrowUp", "ArrowDown"].includes(e.code)) e.preventDefault();
            if(gameState === "PLAY") {
                if(e.code === "KeyF") p1.attack(p2);
                if(e.code === "KeyG") p1.useUltimate(p2);
                if(e.code === "ArrowDown") p2.attack(p1);
                if(e.code === "KeyL") p2.useUltimate(p1);
            }
        });
        window.addEventListener("keyup", (e) => { keys[e.code] = false; });

        class Player {
            constructor(x, y, type, is1P) {
                this.is1P = is1P;
                this.type = type;
                this.x = x;
                this.y = y;
                // 캐릭터 크기 축소 (40x60 -> 30x45)
                this.width = 30;
                this.height = 45;
                this.vY = 0;
                this.facing = is1P ? 1 : -1;
                this.isJumping = false;
                
                if(type === "Main") {
                    this.name = "메인";
                    this.hp = 100;
                    this.maxHp = 100;
                    this.damage = 20;
                    this.range = 8 * GRID; // 사거리 8칸
                    this.atkDelay = 42; // 0.7초 (60fps * 0.7)
                    this.ultDamage = 30;
                    this.ultRange = 10 * GRID;
                    this.ultMaxCooldown = 600; // 10초
                    this.color = "#1e90ff";
                } else {
                    this.name = "마리";
                    this.hp = 90;
                    this.maxHp = 90;
                    this.damage = 8;
                    this.range = 20 * GRID; // 사거리 20칸 (화면 절반 이상)
                    this.atkDelay = 72; // 1.2초 (60fps * 1.2)
                    this.ultDamage = 20;
                    this.ultRange = 4 * GRID;
                    this.ultMaxCooldown = 720; // 12초
                    this.color = "#ff00ff";
                }

                this.atkCooldown = 0;
                this.ultCooldown = 0;
                this.effectTimer = 0;
                this.ultEffectTimer = 0;
            }

            draw() {
                ctx.shadowBlur = 15;
                ctx.shadowColor = this.color;
                ctx.fillStyle = this.color;
                ctx.fillRect(this.x, this.y, this.width, this.height);
                ctx.shadowBlur = 0;

                ctx.fillStyle = "white";
                if(this.type === "Main") {
                    ctx.fillRect(this.x + 5, this.y - 5, 20, 5);
                } else {
                    ctx.beginPath();
                    ctx.arc(this.x + 15, this.y - 5, 6, 0, Math.PI * 2);
                    ctx.fill();
                }

                ctx.fillStyle = "white";
                ctx.font = "11px Arial";
                ctx.fillText(this.name + (this.is1P ? "(1P)" : "(2P)"), this.x, this.y - 30);
                
                ctx.fillStyle = "#333";
                ctx.fillRect(this.x, this.y - 20, 30, 4);
                ctx.fillStyle = this.hp < 30 ? "red" : "lime";
                ctx.fillRect(this.x, this.y - 20, (this.hp / this.maxHp) * 30, 4);

                ctx.fillStyle = "rgba(255,255,255,0.3)";
                ctx.fillRect(this.x, this.y - 14, 30, 2);
                ctx.fillStyle = "yellow";
                let ultBar = (1 - this.ultCooldown / this.ultMaxCooldown) * 30;
                ctx.fillRect(this.x, this.y - 14, Math.max(0, ultBar), 2);

                if(this.effectTimer > 0) {
                    ctx.fillStyle = this.type === "Main" ? "rgba(30,144,255,0.4)" : "rgba(255,0,255,0.4)";
                    let rX = this.facing === 1 ? this.x + this.width : this.x - this.range;
                    ctx.fillRect(rX, this.y + 15, this.range, 8);
                    this.effectTimer--;
                }

                if(this.ultEffectTimer > 0) {
                    ctx.strokeStyle = "yellow";
                    ctx.lineWidth = 2;
                    if(this.type === "Main") {
                        let rX = this.facing === 1 ? this.x + this.width : this.x - this.ultRange;
                        ctx.strokeRect(rX, this.y, this.ultRange, this.height);
                    } else {
                        ctx.beginPath();
                        ctx.arc(this.x + 15, this.y + 22, this.ultRange, 0, Math.PI * 2);
                        ctx.stroke();
                    }
                    this.ultEffectTimer--;
                }
            }

            update() {
                this.vY += GRAVITY;
                this.y += this.vY;
                if (this.y >= canvas.height - this.height - 20) {
                    this.y = canvas.height - this.height - 20;
                    this.vY = 0;
                    this.isJumping = false;
                }
                if (this.x < 0) this.x = 0;
                if (this.x > canvas.width - this.width) this.x = canvas.width - this.width;
                
                if(this.atkCooldown > 0) this.atkCooldown--;
                if(this.ultCooldown > 0) this.ultCooldown--;
            }

            jump() {
                if (!this.isJumping) {
                    this.vY = -12;
                    this.isJumping = true;
                }
            }

            attack(opp) {
                if(this.atkCooldown > 0) return;
                this.effectTimer = 8;
                this.atkCooldown = this.atkDelay;
                
                let myL = this.facing === 1 ? this.x + this.width : this.x - this.range;
                let myR = this.facing === 1 ? this.x + this.width + this.range : this.x;

                if(myR >= opp.x && myL <= opp.x + opp.width && 
                   this.y + this.height >= opp.y && this.y <= opp.y + opp.height) {
                    opp.hp -= this.damage;
                }
            }

            useUltimate(opp) {
                if(this.ultCooldown > 0) return;
                this.ultEffectTimer = 15;
                this.ultCooldown = this.ultMaxCooldown;

                if(this.type === "Main") {
                    let myL = this.facing === 1 ? this.x + this.width : this.x - this.ultRange;
                    let myR = this.facing === 1 ? this.x + this.width + this.ultRange : this.x;
                    if(myR >= opp.x && myL <= opp.x + opp.width && 
                       this.y + this.height >= opp.y && this.y <= opp.y + opp.height) {
                        opp.hp -= this.ultDamage;
                    }
                } else {
                    let dx = (this.x + 15) - (opp.x + 15);
                    let dy = (this.y + 22) - (opp.y + 22);
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    if(dist < this.ultRange + 15) {
                        opp.hp -= this.ultDamage;
                    }
                    this.hp = Math.min(this.maxHp, this.hp + 10);
                }
            }
        }

        let p1, p2;

        function selectChar(type) {
            if(!p1Sel) {
                p1Sel = type;
                document.getElementById("select-title").innerText = "2P 캐릭터 선택";
            } else {
                p2Sel = type;
                document.getElementById("select-screen").classList.add("hidden");
                startGame();
            }
        }

        function startGame() {
            p1 = new Player(150, 200, p1Sel, true);
            p2 = new Player(620, 200, p2Sel, false);
            gameState = "PLAY";
        }

        function resetGame() {
            p1Sel = null; p2Sel = null;
            document.getElementById("select-title").innerText = "1P 캐릭터 선택";
            document.getElementById("select-screen").classList.remove("hidden");
            document.getElementById("result-screen").classList.add("hidden");
            gameState = "SELECT";
        }

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#333";
            ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

            if(gameState === "PLAY") {
                if (keys["KeyA"]) { p1.x -= 5; p1.facing = -1; }
                if (keys["KeyD"]) { p1.x += 5; p1.facing = 1; }
                if (keys["Space"]) p1.jump();

                if (keys["ArrowLeft"]) { p2.x -= 5; p2.facing = -1; }
                if (keys["ArrowRight"]) { p2.x += 5; p2.facing = 1; }
                if (keys["ArrowUp"]) p2.jump();

                p1.update(); p2.update();
                p1.draw(); p2.draw();

                if(p1.hp <= 0 || p2.hp <= 0) {
                    gameState = "END";
                    document.getElementById("result-screen").classList.remove("hidden");
                    document.getElementById("winner-text").innerText = p1.hp <= 0 ? "2P 승리!" : "1P 승리!";
                }
            } else if (gameState === "SELECT") {
                ctx.fillStyle = "#444";
                ctx.font = "20px Arial";
                ctx.fillText("캐릭터를 선택해주세요...", 300, 200);
            } else {
                p1.draw(); p2.draw();
            }
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
</body>
</html>
"""

# 스트림릿 출력
components.html(game_html, height=550)

st.markdown("""
### 📢 업데이트 로그
1. **크기 축소:** 캐릭터 크기가 약 25% 작아져서 더 넓은 전장 활용이 가능합니다.
2. **마리(Mari) 상향:** 
   - 사거리가 **20칸**으로 대폭 증가하여 멀리서 저격이 가능합니다.
   - 공격 속도 **1.2초**, 궁극기 쿨타임 **12초**로 조정되었습니다.
3. **메인(Main) 상향:** 
   - 공격 속도가 **0.7초**로 매우 빨라져 근접전 화력이 강화되었습니다.
   - 사거리 **8칸**으로 상향되어 접근이 용이해졌습니다.
""")
