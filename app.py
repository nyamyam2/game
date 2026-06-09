import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="스트림릿 네온 배틀", layout="centered")

st.title("⚔️ 스트림릿 2P 배틀: 어웨이크닝")
st.caption("새로운 캐릭터 '미리'와 강력한 '궁극기'가 추가되었습니다!")

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
        <button class="char-btn main-btn" onclick="selectChar('Main')">메인<br>(근접/폭발)</button>
        <button class="char-btn miri-btn" onclick="selectChar('Miri')">미리<br>(원거리/회복)</button>
        <p style="font-size: 12px; color: #888; margin-top: 15px;">메인: 공20/범위4/궁30<br>미리: 공8/범위8/궁20+힐</p>
    </div>

    <div id="result-screen" class="ui-overlay hidden">
        <h2 id="winner-text"></h2>
        <button class="restart-btn" onclick="resetGame()">다시하기 (Restart)</button>
    </div>

    <canvas id="gameCanvas" width="800" height="400"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        
        const GRID = 20;
        const GRAVITY = 0.6;
        
        let gameState = "SELECT"; // SELECT, PLAY, END
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
                this.width = 40;
                this.height = 60;
                this.vY = 0;
                this.facing = is1P ? 1 : -1;
                this.isJumping = false;
                
                // 캐릭터별 스탯 설정
                if(type === "Main") {
                    this.name = "메인";
                    this.hp = 100;
                    this.maxHp = 100;
                    this.damage = 20;
                    this.range = 4 * GRID;
                    this.atkDelay = 60; // 1초 (60fps)
                    this.ultDamage = 30;
                    this.ultRange = 6 * GRID;
                    this.ultMaxCooldown = 600; // 10초
                    this.color = "#1e90ff";
                } else {
                    this.name = "미리";
                    this.hp = 90;
                    this.maxHp = 90;
                    this.damage = 8;
                    this.range = 8 * GRID;
                    this.atkDelay = 90; // 1.5초
                    this.ultDamage = 20;
                    this.ultRange = 4 * GRID; // AoE 범위 (반경)
                    this.ultMaxCooldown = 780; // 13초
                    this.color = "#ff00ff";
                }

                this.atkCooldown = 0;
                this.ultCooldown = 0;
                this.effectTimer = 0;
                this.ultEffectTimer = 0;
            }

            draw() {
                // 몸체
                ctx.shadowBlur = 10;
                ctx.shadowColor = this.color;
                ctx.fillStyle = this.color;
                ctx.fillRect(this.x, this.y, this.width, this.height);
                ctx.shadowBlur = 0;

                // 머리 장식 (메인은 뿔, 미리는 리본 느낌)
                ctx.fillStyle = "white";
                if(this.type === "Main") {
                    ctx.fillRect(this.x + 10, this.y - 5, 20, 5);
                } else {
                    ctx.beginPath();
                    ctx.arc(this.x + 20, this.y - 5, 8, 0, Math.PI * 2);
                    ctx.fill();
                }

                // UI (이름, HP, 쿨다운)
                ctx.fillStyle = "white";
                ctx.font = "12px Arial";
                ctx.fillText(this.name + (this.is1P ? "(1P)" : "(2P)"), this.x, this.y - 30);
                
                // HP Bar
                ctx.fillStyle = "#333";
                ctx.fillRect(this.x, this.y - 20, 40, 5);
                ctx.fillStyle = this.hp < 30 ? "red" : "lime";
                ctx.fillRect(this.x, this.y - 20, (this.hp / this.maxHp) * 40, 5);

                // Ult Cooldown Bar
                ctx.fillStyle = "rgba(255,255,255,0.3)";
                ctx.fillRect(this.x, this.y - 12, 40, 3);
                ctx.fillStyle = "yellow";
                let ultBar = (1 - this.ultCooldown / this.ultMaxCooldown) * 40;
                ctx.fillRect(this.x, this.y - 12, Math.max(0, ultBar), 3);

                // 공격 이펙트
                if(this.effectTimer > 0) {
                    ctx.fillStyle = "rgba(255,255,255,0.5)";
                    let rX = this.facing === 1 ? this.x + this.width : this.x - this.range;
                    ctx.fillRect(rX, this.y + 20, this.range, 10);
                    this.effectTimer--;
                }

                // 궁극기 이펙트
                if(this.ultEffectTimer > 0) {
                    ctx.strokeStyle = "yellow";
                    ctx.lineWidth = 3;
                    if(this.type === "Main") {
                        let rX = this.facing === 1 ? this.x + this.width : this.x - this.ultRange;
                        ctx.strokeRect(rX, this.y, this.ultRange, this.height);
                    } else {
                        // 미리 AoE (원형)
                        ctx.beginPath();
                        ctx.arc(this.x + 20, this.y + 30, this.ultRange, 0, Math.PI * 2);
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
                    this.vY = -13;
                    this.isJumping = true;
                }
            }

            attack(opp) {
                if(this.atkCooldown > 0) return;
                this.effectTimer = 10;
                this.atkCooldown = this.atkDelay;
                
                let hit = false;
                let myL = this.facing === 1 ? this.x + this.width : this.x - this.range;
                let myR = this.facing === 1 ? this.x + this.width + this.range : this.x;

                if(myR >= opp.x && myL <= opp.x + opp.width && 
                   this.y + this.height >= opp.y && this.y <= opp.y + opp.height) {
                    opp.hp -= this.damage;
                }
            }

            useUltimate(opp) {
                if(this.ultCooldown > 0) return;
                this.ultEffectTimer = 20;
                this.ultCooldown = this.ultMaxCooldown;

                if(this.type === "Main") {
                    let myL = this.facing === 1 ? this.x + this.width : this.x - this.ultRange;
                    let myR = this.facing === 1 ? this.x + this.width + this.ultRange : this.x;
                    if(myR >= opp.x && myL <= opp.x + opp.width && 
                       this.y + this.height >= opp.y && this.y <= opp.y + opp.height) {
                        opp.hp -= this.ultDamage;
                    }
                } else {
                    // 미리 궁극기: 주변 원형 범위
                    let dx = (this.x + 20) - (opp.x + 20);
                    let dy = (this.y + 30) - (opp.y + 30);
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    if(dist < this.ultRange + 20) {
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
            p1 = new Player(100, 200, p1Sel, true);
            p2 = new Player(660, 200, p2Sel, false);
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
            
            // 바닥
            ctx.fillStyle = "#333";
            ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

            if(gameState === "PLAY") {
                // 1P 이동
                if (keys["KeyA"]) { p1.x -= 5; p1.facing = -1; }
                if (keys["KeyD"]) { p1.x += 5; p1.facing = 1; }
                if (keys["Space"]) p1.jump();

                // 2P 이동
                if (keys["ArrowLeft"]) { p2.x -= 5; p2.facing = -1; }
                if (keys["ArrowRight"]) { p2.x += 5; p2.facing = 1; }
                if (keys["ArrowUp"]) p2.jump();

                p1.update();
                p2.update();
                p1.draw();
                p2.draw();

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
### 🎮 조작법 안내
| 기능 | 1P (좌측) | 2P (우측) |
| :--- | :--- | :--- |
| **이동/점프** | A, D / Space | ◀, ▶ / ▲ |
| **일반 공격** | **F** | **▼ (아래 화살표)** |
| **궁극기** | **G** | **L** |

**캐릭터 특징:**
- **메인:** 높은 체력과 강력한 공격력. 궁극기는 전방의 적에게 큰 피해를 줍니다.
- **미리:** 긴 사거리로 견제에 능합니다. 궁극기는 주변 적에게 피해를 주고 자신의 체력을 회복합니다.
""")
