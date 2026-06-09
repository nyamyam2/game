import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="스트림릿 네온 배틀: 파이널 오버홀", layout="centered")

st.title("⚔️ 스트림릿 2P 배틀: 파이널 오버홀")
st.caption("마리의 저격 능력 조정 및 메인의 초고속 공격 & 디버프 궁극기 업데이트!")

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
        <button class="char-btn main-btn" onclick="selectChar('Main')">메인<br>(광속/디버프)</button>
        <button class="char-btn miri-btn" onclick="selectChar('Mari')">마리<br>(저격/고위력궁)</button>
        <p style="font-size: 12px; color: #888; margin-top: 15px;">
            메인: HP110/이속+8%/속도0.5s/범위6/궁9s(감속)<br>
            마리: HP 90/속도1.3s/범위18/궁12s(피해25)
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
        
        const GRID = 20; 
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
                this.width = 30;
                this.height = 45;
                this.vY = 0;
                this.facing = is1P ? 1 : -1;
                this.isJumping = false;
                
                // 디버프 관련 상태
                this.slowTimer = 0;
                this.baseSpeed = 5;

                if(type === "Main") {
                    this.name = "메인";
                    this.hp = 110;          // 체력 상향
                    this.maxHp = 110;
                    this.damage = 20;
                    this.range = 6 * GRID;  // 사거리 6칸
                    this.atkDelay = 30;     // 0.5초 (60fps * 0.5)
                    this.baseSpeed = 5 * 1.08; // 이동속도 8% 증가 (5.4)
                    this.ultDamage = 20;    // 궁극기 데미지 조정
                    this.ultRange = 8 * GRID; 
                    this.ultMaxCooldown = 540; // 궁극기 쿨타임 9초 (60fps * 9)
                    this.color = "#1e90ff";
                } else {
                    this.name = "마리";
                    this.hp = 90;
                    this.maxHp = 90;
                    this.damage = 8;
                    this.range = 18 * GRID; // 사거리 18칸
                    this.atkDelay = 78;     // 1.3초 (60fps * 1.3)
                    this.ultDamage = 25;    // 궁극기 데미지 25
                    this.ultRange = 4 * GRID;
                    this.ultMaxCooldown = 720; // 궁극기 쿨타임 12초
                    this.color = "#ff00ff";
                }

                this.atkCooldown = 0;
                this.ultCooldown = 0;
                this.effectTimer = 0;
                this.ultEffectTimer = 0;
            }

            // 현재 이동 속도 계산 (디버프 반영)
            get currentSpeed() {
                if (this.slowTimer > 0) {
                    return this.baseSpeed * 0.85; // 15% 감속
                }
                return this.baseSpeed;
            }

            draw() {
                ctx.shadowBlur = 15;
                ctx.shadowColor = this.color;
                
                // 슬로우 상태일 때 캐릭터 색상 보라/하얗게 변조 효과
                if (this.slowTimer > 0) {
                    ctx.fillStyle = "#57606f"; 
                } else {
                    ctx.fillStyle = this.color;
                }
                
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
                
                // 감속 디버프 표시
                if (this.slowTimer > 0) {
                    ctx.fillStyle = "#00f2ff";
                    ctx.font = "9px Arial";
                    ctx.fillText("SLOW", this.x, this.y - 38);
                }

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
                    ctx.strokeStyle = this.type === "Main" ? "#00f2ff" : "yellow";
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
                if(this.slowTimer > 0) this.slowTimer--; // 슬로우 타이머 감소
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
                        opp.slowTimer = 90; // 1.5초간 감속 디버프 (60fps * 1.5 = 90)
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
                if (keys["KeyA"]) { p1.x -= p1.currentSpeed; p1.facing = -1; }
                if (keys["KeyD"]) { p1.x += p1.currentSpeed; p1.facing = 1; }
                if (keys["Space"]) p1.jump();

                if (keys["ArrowLeft"]) { p2.x -= p2.currentSpeed; p2.facing = -1; }
                if (keys["ArrowRight"]) { p2.x += p2.currentSpeed; p2.facing = 1; }
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

components.html(game_html, height=550)

st.markdown("""
### 📢 밸런스 패치 노트 (최종 하이라이트)
* **마리 (Mari):**
  - 일반 사거리가 **18칸**으로 미세 조정되었고, 공격 속도가 **1.3초**로 변경되어 거리 조절의 중요성이 커졌습니다.
  - 대신 궁극기(L키) 직격 피해량이 **25**로 상향되어 결정력이 강화되었습니다.
* **메인 (Main):**
  - 체력이 **110**으로 증가하고 기본 이동 속도가 **8%** 빨라져 인파이팅 능력이 극대화되었습니다.
  - 일반 사거리가 **6칸**으로 좁혀진 대신, 공격 속도가 **0.5초**로 가공할 만한 속사형으로 변모했습니다.
  - 궁극기 쿨타임이 **9초**로 대폭 감소하고 피해량이 **20**이 된 대신, 적중 시 **1.5초간 적의 이동속도를 15% 느리게 만듭니다** (적중 시 상대 위에 `SLOW` 표시).
""")
