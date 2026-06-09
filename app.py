import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="스트림릿 네온 배틀: 덤불 버프", layout="centered")

st.title("⚔️ 스트림릿 2P 배틀: 덤불 버프 업데이트")
st.caption("네온 미로의 덤불 속에서 재장전 가속과 지속 회복 효과를 누리세요!")

# 게임 로직 (HTML/JS)
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; background-color: #1a1a1a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; overflow: hidden; }
        canvas { background: #000; border: 3px solid #333; display: block; margin: 10px auto; box-shadow: 0 0 20px rgba(0,255,255,0.2); }
        .ui-overlay { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.9); 
                     padding: 25px; border: 2px solid #00f2ff; border-radius: 20px; width: 550px; z-index: 10; box-shadow: 0 0 30px rgba(0,0,0,0.8); }
        
        .char-container { display: flex; justify-content: center; gap: 15px; margin: 15px 0; }
        .char-card { background: #222; border: 2px solid #444; border-radius: 12px; padding: 10px; width: 140px; cursor: pointer; transition: 0.3s; text-align: center; }
        .char-card:hover { transform: scale(1.05); border-color: #00f2ff; }
        .char-face { width: 60px; height: 60px; margin: 0 auto 8px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; }
        
        .face-main { background: #1e90ff; border: 2px solid #00f2ff; color: #fff; text-shadow: 0 0 5px #00f2ff; }
        .face-mari { background: #ff00ff; border: 2px solid #ff77ff; color: #fff; text-shadow: 0 0 5px #ff77ff; }
        .face-star { background: #ffca28; border: 2px solid #fff; color: #000; }

        .map-container { display: flex; justify-content: center; gap: 20px; margin: 15px 0; }
        .map-btn { padding: 12px 25px; cursor: pointer; border: 2px solid #555; background: #333; color: white; font-weight: bold; border-radius: 8px; transition: 0.2s; }
        .map-btn.selected { border-color: #2ed573; background: #1e4620; }
        
        .start-action-btn { background: #2ed573; color: white; padding: 12px 30px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 15px; }
        .restart-btn { background: #2ed573; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px; }
        .hidden { display: none; }
        .status-container { display: flex; justify-content: space-around; width: 800px; margin: 0 auto; font-size: 14px; color: #aaa; }
    </style>
</head>
<body>

    <div class="status-container">
        <div>1P: A/D(이동), Space(점프), F(공격), G(궁극기)</div>
        <div>2P: ◀/▶(이동), ▲(점프), ↓(공격), L(궁극기)</div>
    </div>

    <div id="select-screen" class="ui-overlay">
        <h2 id="select-title" style="color:#00f2ff; margin-bottom: 5px;">1P 캐릭터 선택</h2>
        <p id="select-subtitle" style="font-size:13px; color:#aaa; margin:0;">플레이어는 원하는 캐릭터 카드를 클릭하세요.</p>
        
        <div class="char-container">
            <div class="char-card" onclick="selectChar('Main')">
                <div class="char-face face-main">⚡🕶️</div>
                <strong style="color:#1e90ff;">메인</strong>
                <div style="font-size:10px; color:#bbb; margin-top:5px;">공속 0.4s | 범위 4<br>궁: 10s(감속)</div>
            </div>
            <div class="char-card" onclick="selectChar('Mari')">
                <div class="char-face face-mari">🌸🎀</div>
                <strong style="color:#ff00ff;">마리</strong>
                <div style="font-size:10px; color:#bbb; margin-top:5px;">공속 1.2s | 범위 16<br>궁: 12s(적중시 힐)</div>
            </div>
            <div class="char-card" onclick="selectChar('Star')">
                <div class="char-face face-star">⭐👑</div>
                <strong style="color:#ffca28;">스타</strong>
                <div style="font-size:10px; color:#bbb; margin-top:5px;">공속 0.5s | 범위 7<br>궁: 13s(공/이속 버프)</div>
            </div>
        </div>

        <hr style="border: 1px solid #333; margin: 15px 0;">
        <h3 style="margin: 5px 0;">전장(맵) 선택</h3>
        <div class="map-container">
            <button id="map0-btn" class="map-btn selected" onclick="selectMap(0)">평지 아레나</button>
            <button id="map1-btn" class="map-btn" onclick="selectMap(1)">네온 미로 (낮은 벽 & 덤불)</button>
        </div>

        <button id="start-game-btn" class="start-action-btn hidden" onclick="confirmStart()">전장으로 진입</button>
    </div>

    <div id="result-screen" class="ui-overlay hidden">
        <h2 id="winner-text" style="font-size: 30px;"></h2>
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
        let selectedMapIndex = 0;

        const mapObstacles = [
            { x: 180, y: 330, w: 50, h: 50 }, 
            { x: 570, y: 330, w: 50, h: 50 }, 
            { x: 320, y: 240, w: 160, h: 25 } 
        ];

        const mapBushes = [
            { x: 60, y: 320, w: 80, h: 60 },
            { x: 660, y: 320, w: 80, h: 60 },
            { x: 370, y: 180, w: 60, h: 60 }
        ];

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
                
                this.slowTimer = 0;
                this.buffTimer = 0;
                this.inBush = false;     // 현재 덤불 안에 있는지 여부
                this.bushHealTimer = 0;  // 덤불 자생 타이머 (3초 = 180프레임)
                this.healTextTimer = 0;  // 힐 텍스트 팝업 연출용

                if(type === "Main") {
                    this.name = "메인";
                    this.hp = 100;
                    this.maxHp = 100;
                    this.damage = 9;
                    this.range = 4 * GRID;
                    this.atkDelay = 24; 
                    this.baseSpeed = 5 * 1.13; 
                    this.ultDamage = 15;
                    this.ultRange = 8 * GRID; 
                    this.ultMaxCooldown = 600; 
                    this.color = "#1e90ff";
                    this.faceSymbol = "⚡";
                } else if(type === "Mari") {
                    this.name = "마리";
                    this.hp = 90;
                    this.maxHp = 90;
                    this.damage = 8;
                    this.range = 16 * GRID;
                    this.atkDelay = 72; 
                    this.baseSpeed = 5 * 0.97; 
                    this.ultDamage = 20;
                    this.ultRange = 4 * GRID;
                    this.ultMaxCooldown = 720; 
                    this.color = "#ff00ff";
                    this.faceSymbol = "🌸";
                } else { 
                    this.name = "스타";
                    this.hp = 130;
                    this.maxHp = 130;
                    this.damage = 5;
                    this.range = 7 * GRID;
                    this.atkDelay = 30; 
                    this.baseSpeed = 5;
                    this.ultDamage = 0; 
                    this.ultRange = 0;
                    this.ultMaxCooldown = 780; 
                    this.color = "#ffca28";
                    this.faceSymbol = "⭐";
                }

                this.atkCooldown = 0;
                this.ultCooldown = 0;
                this.effectTimer = 0;
                this.ultEffectTimer = 0;
            }

            get currentSpeed() {
                let speed = this.baseSpeed;
                if (this.slowTimer > 0) speed *= 0.85; 
                if (this.buffTimer > 0) speed *= 1.20; 
                return speed;
            }

            get currentAtkDelay() {
                if (this.buffTimer > 0) return this.atkDelay * 0.80; 
                return this.atkDelay;
            }

            checkBushIntersection() {
                if (selectedMapIndex !== 1) {
                    this.inBush = false;
                    return;
                }
                let inside = false;
                for(let b of mapBushes) {
                    if(this.x + this.width > b.x && this.x < b.x + b.w &&
                       this.y + this.height > b.y && this.y < b.y + b.h) {
                        inside = true;
                        break;
                    }
                }
                this.inBush = inside;
            }

            draw() {
                ctx.save();
                if(this.inBush) ctx.globalAlpha = 0.4; // 은신 시 반투명

                ctx.shadowBlur = 15;
                ctx.shadowColor = this.color;
                
                if (this.slowTimer > 0) ctx.fillStyle = "#57606f"; 
                else if (this.buffTimer > 0) ctx.fillStyle = "#fff200"; 
                else ctx.fillStyle = this.color;
                
                ctx.fillRect(this.x, this.y, this.width, this.height);
                ctx.shadowBlur = 0;

                ctx.fillStyle = "white";
                ctx.font = "12px Arial";
                ctx.fillText(this.faceSymbol, this.x + 8, this.y + 25);

                ctx.fillStyle = "white";
                ctx.font = "11px Arial";
                ctx.fillText(this.name + (this.is1P ? "(1P)" : "(2P)"), this.x, this.y - 30);
                
                if (this.slowTimer > 0) { ctx.fillStyle = "#00f2ff"; ctx.fillText("SLOW", this.x, this.y - 38); }
                if (this.buffTimer > 0) { ctx.fillStyle = "#ffca28"; ctx.fillText("BUFF!!", this.x, this.y - 38); }

                // 덤불 전용 버프 텍스트 UI
                if (this.inBush) {
                    ctx.fillStyle = "#2ed573";
                    ctx.font = "9px Arial";
                    ctx.fillText("BUSH +15% ⚡", this.x, this.y - 46);
                }

                // 🌿 초록색 틱 회복 팝업 연출
                if (this.healTextTimer > 0) {
                    ctx.fillStyle = "#2ed573";
                    ctx.font = "bold 12px Arial";
                    ctx.fillText("+2", this.x + this.width + 5, this.y + 10);
                    this.healTextTimer--;
                }

                // HP Bar
                ctx.fillStyle = "#333";
                ctx.fillRect(this.x, this.y - 20, 30, 4);
                ctx.fillStyle = this.hp < (this.maxHp * 0.3) ? "red" : "lime";
                ctx.fillRect(this.x, this.y - 20, (this.hp / this.maxHp) * 30, 4);

                // Ult Cooldown Bar
                ctx.fillStyle = "rgba(255,255,255,0.3)";
                ctx.fillRect(this.x, this.y - 14, 30, 2);
                ctx.fillStyle = "yellow";
                let ultBar = (1 - this.ultCooldown / this.ultMaxCooldown) * 30;
                ctx.fillRect(this.x, this.y - 14, Math.max(0, ultBar), 2);

                if(this.effectTimer > 0) {
                    ctx.fillStyle = "rgba(255,255,255,0.4)";
                    let rX = this.facing === 1 ? this.x + this.width : this.x - this.range;
                    ctx.fillRect(rX, this.y + 15, this.range, 6);
                    this.effectTimer--;
                }

                if(this.ultEffectTimer > 0) {
                    ctx.strokeStyle = "yellow";
                    ctx.lineWidth = 2;
                    if(this.type === "Main") {
                        let rX = this.facing === 1 ? this.x + this.width : this.x - this.ultRange;
                        ctx.strokeRect(rX, this.y, this.ultRange, this.height);
                    } else if(this.type === "Mari") {
                        ctx.beginPath();
                        ctx.arc(this.x + 15, this.y + 22, this.ultRange, 0, Math.PI * 2);
                        ctx.stroke();
                    } else { 
                        ctx.strokeStyle = "#ffca28";
                        ctx.strokeRect(this.x - 5, this.y - 5, this.width + 10, this.height + 10);
                    }
                    this.ultEffectTimer--;
                }
                ctx.restore();
            }

            update() {
                this.vY += GRAVITY;
                this.y += this.vY;
                
                if (this.y >= canvas.height - this.height - 20) {
                    this.y = canvas.height - this.height - 20;
                    this.vY = 0;
                    this.isJumping = false;
                }

                if (selectedMapIndex === 1) {
                    for(let obs of mapObstacles) {
                        if (this.x + this.width > obs.x && this.x < obs.x + obs.w &&
                            this.y + this.height > obs.y && this.y < obs.y + obs.h) {
                            
                            if (this.y + this.height - this.vY <= obs.y) {
                                this.y = obs.y - this.height;
                                this.vY = 0;
                                this.isJumping = false;
                            } else if (this.y - this.vY >= obs.y + obs.h) {
                                this.y = obs.y + obs.h;
                                this.vY = 0;
                            } else {
                                if (this.x + this.width/2 < obs.x + obs.w/2) {
                                    this.x = obs.x - this.width;
                                } else {
                                    this.x = obs.x + obs.w;
                                }
                            }
                        }
                    }
                }

                if (this.x < 0) this.x = 0;
                if (this.x > canvas.width - this.width) this.x = canvas.width - this.width;
                
                // 덤불 상호작용 검사 추가
                this.checkBushIntersection();

                // ⏳ 덤불 안에서는 공격 및 궁극기 재장전(쿨타임)이 15% 더 빠르게 참
                let cooldownSpeed = this.inBush ? 1.15 : 1.0;

                if(this.atkCooldown > 0) this.atkCooldown = Math.max(0, this.atkCooldown - cooldownSpeed);
                if(this.ultCooldown > 0) this.ultCooldown = Math.max(0, this.ultCooldown - cooldownSpeed);
                
                // 🌿 덤불 상시 지속 힐 메커니즘 (3초 = 180프레임마다 HP 2 회복)
                if(this.inBush && this.hp < this.maxHp) {
                    this.bushHealTimer++;
                    if(this.bushHealTimer >= 180) {
                        this.hp = Math.min(this.maxHp, this.hp + 2);
                        this.bushHealTimer = 0;
                        this.healTextTimer = 30; // 0.5초 동안 초록색 팝업 노출
                    }
                } else {
                    this.bushHealTimer = 0;
                }

                if(this.slowTimer > 0) this.slowTimer--;
                if(this.buffTimer > 0) this.buffTimer--;
            }

            jump() {
                let 온그라운드 = (this.y >= canvas.height - this.height - 20);
                if (selectedMapIndex === 1) {
                    for(let obs of mapObstacles) {
                        if (this.x + this.width > obs.x && this.x < obs.x + obs.w && Math.abs((this.y + this.height) - obs.y) < 2) {
                            온그라운드 = true;
                        }
                    }
                }
                if (!this.isJumping || 온그라운드) {
                    this.vY = -12;
                    this.isJumping = true;
                }
            }

            attack(opp) {
                if(this.atkCooldown > 0) return;
                this.effectTimer = 6;
                this.atkCooldown = this.currentAtkDelay; 
                
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
                        opp.slowTimer = 90; 
                    }
                } else if(this.type === "Mari") {
                    let dx = (this.x + 15) - (opp.x + 15);
                    let dy = (this.y + 22) - (opp.y + 22);
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    
                    if(dist < this.ultRange + 15) {
                        opp.hp -= this.ultDamage;
                        this.hp = Math.min(this.maxHp, this.hp + 10); 
                    }
                } else if(this.type === "Star") {
                    this.buffTimer = 150;
                }
            }
        }

        let p1, p2;

        function selectChar(type) {
            if(!p1Sel) {
                p1Sel = type;
                document.getElementById("select-title").innerText = "2P 캐릭터 선택";
            } else if(!p2Sel) {
                p2Sel = type;
                document.getElementById("select-title").innerText = "전장 확정 및 진입";
                document.getElementById("select-subtitle").innerText = "원하는 맵을 마우스로 클릭하고 아래 버튼을 누르세요.";
                document.getElementById("start-game-btn").classList.remove("hidden");
            }
        }

        function selectMap(index) {
            selectedMapIndex = index;
            document.getElementById("map0-btn").classList.remove("selected");
            document.getElementById("map1-btn").classList.remove("selected");
            document.getElementById("map" + index + "-btn").classList.add("selected");
        }

        function confirmStart() {
            document.getElementById("select-screen").classList.add("hidden");
            p1 = new Player(120, 200, p1Sel, true);
            p2 = new Player(650, 200, p2Sel, false);
            gameState = "PLAY";
        }

        function resetGame() {
            p1Sel = null; p2Sel = null;
            document.getElementById("select-title").innerText = "1P 캐릭터 선택";
            document.getElementById("select-subtitle").innerText = "플레이어는 원하는 캐릭터 카드를 클릭하세요.";
            document.getElementById("select-screen").classList.remove("hidden");
            document.getElementById("result-screen").classList.add("hidden");
            document.getElementById("start-game-btn").classList.add("hidden");
            gameState = "SELECT";
        }

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            if(selectedMapIndex === 1) {
                ctx.fillStyle = "rgba(46, 213, 115, 0.35)";
                for(let b of mapBushes) {
                    ctx.fillRect(b.x, b.y, b.w, b.h);
                }
                ctx.fillStyle = "#4a4a4a"; 
                for(let obs of mapObstacles) {
                    ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
                }
            }

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
                ctx.fillStyle = "#222";
                ctx.font = "18px Arial";
                ctx.fillText("대기실에서 세팅을 조율 중입니다...", 260, 200);
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

components.html(game_html, height=560)
