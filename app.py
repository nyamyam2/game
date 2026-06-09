import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="스트림릿 네온 배틀: 스타의 등장", layout="centered")

st.title("⚔️ 스트림릿 2P 배틀: 스타의 등장")
st.caption("신규 캐릭 '스타', 맵 선택 시스템, 그리고 정밀해진 스탯 밸런스 업데이트!")

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
        
        /* 캐릭터 카드 스타일 */
        .char-container { display: flex; justify-content: center; gap: 15px; margin: 15px 0; }
        .char-card { background: #222; border: 2px solid #444; border-radius: 12px; padding: 10px; width: 140px; cursor: pointer; transition: 0.3s; text-align: center; }
        .char-card:hover { transform: scale(1.05); border-color: #00f2ff; }
        .char-face { width: 60px; height: 60px; margin: 0 auto 8px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; }
        
        /* 캐릭터별 얼굴 색상 */
        .face-main { background: #1e90ff; border: 2px solid #00f2ff; color: #fff; text-shadow: 0 0 5px #00f2ff; }
        .face-mari { background: #ff00ff; border: 2px solid #ff77ff; color: #fff; text-shadow: 0 0 5px #ff77ff; }
        .face-star { background: #ffca28; border: 2px solid #fff; color: #000; }

        /* 맵 선택 버튼 스타일 */
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
            <button id="map1-btn" class="map-btn" onclick="selectMap(1)">네온 미로 (벽&덤불)</button>
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
        
        let gameState = "SELECT"; // SELECT, PLAY, END
        let p1Sel = null, p2Sel = null;
        let selectedMapIndex = 0;

        // 구조물 정의 (Map 1용: 벽 구조물 리스트)
        // x, y, width, height
        const mapObstacles = [
            { x: 200, y: 260, w: 40, h: 120 },
            { x: 560, y: 260, w: 40, h: 120 },
            { x: 340, y: 200, w: 120, h: 30 }
        ];

        // 덤불 정의 (Map 1용: 안으로 들어가면 반투명해짐)
        const mapBushes = [
            { x: 80, y: 300, w: 80, h: 80 },
            { x: 640, y: 300, w: 80, h: 80 },
            { x: 370, y: 120, w: 60, h: 80 }
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
                this.buffTimer = 0; // 스타용 버프 타이머

                if(type === "Main") {
                    this.name = "메인";
                    this.hp = 100;
                    this.maxHp = 100;
                    this.damage = 9;
                    this.range = 4 * GRID;
                    this.atkDelay = 24; // 0.4초 (60fps * 0.4)
                    this.baseSpeed = 5 * 1.13; // 기본 5에서 최종적으로 약 13% 상향(기존 8% + 추가 5%) -> 5.65
                    this.ultDamage = 15;
                    this.ultRange = 8 * GRID; 
                    this.ultMaxCooldown = 600; // 10초
                    this.color = "#1e90ff";
                    this.faceSymbol = "⚡";
                } else if(type === "Mari") {
                    this.name = "마리";
                    this.hp = 90;
                    this.maxHp = 90;
                    this.damage = 8;
                    this.range = 16 * GRID;
                    this.atkDelay = 72; // 1.2초
                    this.baseSpeed = 5 * 0.97; // 이동속도 3% 다운 -> 4.85
                    this.ultDamage = 20;
                    this.ultRange = 4 * GRID;
                    this.ultMaxCooldown = 720; // 12초
                    this.color = "#ff00ff";
                    this.faceSymbol = "🌸";
                } else { // Star
                    this.name = "스타";
                    this.hp = 130;
                    this.maxHp = 130;
                    this.damage = 5;
                    this.range = 7 * GRID;
                    this.atkDelay = 30; // 0.5초
                    this.baseSpeed = 5;
                    this.ultDamage = 0; // 자가 버프기
                    this.ultRange = 0;
                    this.ultMaxCooldown = 780; // 13초
                    this.color = "#ffca28";
                    this.faceSymbol = "⭐";
                }

                this.atkCooldown = 0;
                this.ultCooldown = 0;
                this.effectTimer = 0;
                this.ultEffectTimer = 0;
            }

            // 실시간 이동 속도 반환 (디버프 및 버프 계산)
            get currentSpeed() {
                let speed = this.baseSpeed;
                if (this.slowTimer > 0) speed *= 0.85; // 메인 궁극기 감속 15%
                if (this.buffTimer > 0) speed *= 1.20; // 스타 궁극기 가속 20%
                return speed;
            }

            // 실시간 공격 속도(딜레이) 반환 (스타 버프 반영)
            get currentAtkDelay() {
                if (this.buffTimer > 0) return this.atkDelay * 0.80; // 공격 속도 20% 빨라짐 (딜레이 20% 감소)
                return this.atkDelay;
            }

            draw() {
                // 덤불 속에 있는지 체크 후 투명도 조절
                let inBush = false;
                if(selectedMapIndex === 1) {
                    for(let b of mapBushes) {
                        if(this.x + this.width > b.x && this.x < b.x + b.w &&
                           this.y + this.height > b.y && this.y < b.y + b.h) {
                            inBush = true;
                            break;
                        }
                    }
                }

                ctx.save();
                if(inBush) ctx.globalAlpha = 0.4; // 덤불 은신 효과

                ctx.shadowBlur = 15;
                ctx.shadowColor = this.color;
                
                if (this.slowTimer > 0) ctx.fillStyle = "#57606f"; 
                else if (this.buffTimer > 0) ctx.fillStyle = "#fff200"; // 스타 버프 상태는 황금빛
                else ctx.fillStyle = this.color;
                
                ctx.fillRect(this.x, this.y, this.width, this.height);
                ctx.shadowBlur = 0;

                // 캐릭터 얼굴 특징 그리기
                ctx.fillStyle = "white";
                ctx.font = "12px Arial";
                ctx.fillText(this.faceSymbol, this.x + 8, this.y + 25);

                // UI 정보
                ctx.fillStyle = "white";
                ctx.font = "11px Arial";
                ctx.fillText(this.name + (this.is1P ? "(1P)" : "(2P)"), this.x, this.y - 30);
                
                if (this.slowTimer > 0) { ctx.fillStyle = "#00f2ff"; ctx.fillText("SLOW", this.x, this.y - 38); }
                if (this.buffTimer > 0) { ctx.fillStyle = "#ffca28"; ctx.fillText("BUFF!!", this.x, this.y - 38); }

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

                // 일반 공격 이펙트
                if(this.effectTimer > 0) {
                    ctx.fillStyle = "rgba(255,255,255,0.4)";
                    let rX = this.facing === 1 ? this.x + this.width : this.x - this.range;
                    ctx.fillRect(rX, this.y + 15, this.range, 6);
                    this.effectTimer--;
                }

                // 궁극기 이펙트
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
                    } else { // Star 버프 오라 효과
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
                
                // 바닥 충돌 처리
                if (this.y >= canvas.height - this.height - 20) {
                    this.y = canvas.height - this.height - 20;
                    this.vY = 0;
                    this.isJumping = false;
                }

                // [맵에 따른 벽 충돌 처리] (Map 1 선택 시)
                if (selectedMapIndex === 1) {
                    for(let obs of mapObstacles) {
                        // 캐릭터 수평/수직 충돌 연산
                        if (this.x + this.width > obs.x && this.x < obs.x + obs.w &&
                            this.y + this.height > obs.y && this.y < obs.y + obs.h) {
                            
                            // 바닥이나 천장 충돌
                            if (this.y + this.height - this.vY <= obs.y) {
                                this.y = obs.y - this.height;
                                this.vY = 0;
                                this.isJumping = false;
                            } else if (this.y - this.vY >= obs.y + obs.h) {
                                this.y = obs.y + obs.h;
                                this.vY = 0;
                            } else {
                                // 좌우 벽 밀어내기
                                if (this.x + this.width/2 < obs.x + obs.w/2) {
                                    this.x = obs.x - this.width;
                                } else {
                                    this.x = obs.x + obs.w;
                                }
                            }
                        }
                    }
                }

                // ⭐ [버그 수정 완료] 오른쪽/왼쪽 벽 화면 밖 탈출 완전 방지 
                if (this.x < 0) this.x = 0;
                if (this.x > canvas.width - this.width) this.x = canvas.width - this.width;
                
                if(this.atkCooldown > 0) this.atkCooldown--;
                if(this.ultCooldown > 0) this.ultCooldown--;
                if(this.slowTimer > 0) this.slowTimer--;
                if(this.buffTimer > 0) this.buffTimer--;
            }

            jump() {
                // 일반 바닥 혹은 구조물 위에서만 점프 가능하게 체크
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
                this.atkCooldown = this.currentAtkDelay; // 스타의 버프 상태 반영
                
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
                        opp.slowTimer = 90; // 1.5초 감속
                    }
                } else if(this.type === "Mari") {
                    let dx = (this.x + 15) - (opp.x + 15);
                    let dy = (this.y + 22) - (opp.y + 22);
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    
                    // ⭐ [사양 변경] 적을 맞추었을 때만 체력을 회복하도록 검증 추가
                    if(dist < this.ultRange + 15) {
                        opp.hp -= this.ultDamage;
                        this.hp = Math.min(this.maxHp, this.hp + 10); // 적중 시에만 +10 힐
                    }
                } else if(this.type === "Star") {
                    // 스타 궁극기: 2.5초간 공속, 이속 20% 증가 (60fps * 2.5 = 150프레임)
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
                document.getElementById("select-title").innerText = "맵과 전장 확정";
                document.getElementById("select-subtitle").innerText = "아래에서 맵을 확인하고 진입 버튼을 누르세요.";
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
            p1 = new Player(150, 200, p1Sel, true);
            p2 = new Player(620, 200, p2Sel, false);
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
            
            // 맵 환경요소 그리기
            if(selectedMapIndex === 1) {
                // 덤불 그리기 (초록색 반투명 사각형)
                ctx.fillStyle = "rgba(46, 213, 115, 0.4)";
                for(let b of mapBushes) {
                    ctx.fillRect(b.x, b.y, b.w, b.h);
                }
                // 벽/구조물 그리기 (회색 입체 사각형)
                ctx.fillStyle = "#555";
                for(let obs of mapObstacles) {
                    ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
                }
            }

            // 기본 아레나 바닥
            ctx.fillStyle = "#333";
            ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

            if(gameState === "PLAY") {
                // 1P 키 핸들링
                if (keys["KeyA"]) { p1.x -= p1.currentSpeed; p1.facing = -1; }
                if (keys["KeyD"]) { p1.x += p1.currentSpeed; p1.facing = 1; }
                if (keys["Space"]) p1.jump();

                // 2P 키 핸들링
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
                ctx.fillText("대기실에서 캐릭터와 전장을 조율 중입니다...", 240, 200);
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

st.markdown("""
### 📊 최종 패치 내역 요약

#### 🛠 시스템 및 버그 픽스
1. **오른쪽 벽 탈출 버그 수정:** 플레이어가 우측 경계면 외부로 밀려 나가는 물리 예외 현상을 완벽하게 봉쇄했습니다.
2. **맵 선택 시스템 추가:**
   - **평지 아레나:** 장애물 없는 깔끔한 1:1 진검승부 맵.
   - **네온 미로:** 공중 발판, 기둥형 벽 및 숨으면 몸이 반투명해져서 기습이 가능한 **덤불(Bush)**이 배치된 전략형 맵.
3. **도트 비주얼 얼굴 연출:** 캐릭터 선택창에서 한눈에 구분할 수 있는 얼굴형 디자인 테마 아이콘을 적용했습니다.

#### ⚖️ 영웅별 변경 스탯 사양
* **메인 (Main)**
  - 체력 `100`, 기본 공격력 `9`, 사거리 `4칸`으로 컴팩트화되었습니다.
  - 공격 속도가 **0.4초**로 대폭 상향되었으며, 기본 이동 속도가 5% 추가 보정되어 인파이팅 기동성이 매우 빠릅니다.
  - 궁극기 쿨타임 `10초`, 공격력 `15`로 조정 (감속 디버프 유효).
* **마리 (Mari)**
  - 사거리가 `16칸`으로 재조정되었으며, 이동 속도가 기존 대비 3% 하향되었습니다. (공격 속도 `1.2초`)
  - 궁극기 공격력 `20`. **(핵심)** 이제 궁극기 범위 내에 **적 캐릭터가 정확히 맞았을 때만** 마리의 체력이 10 회복됩니다. 허공에 쓰면 피가 차지 않습니다.
* **★신규 캐릭터★ 스타 (Star)**
  - 높은 기초 체력(`130`)과 균형 잡힌 밸런스형 사거리(`7칸`), 데미지 `5`, 공격 속도 `0.5초`.
  - **궁극기 (버프):** 2.5초 동안 **자신의 이동 속도와 공격 속도가 20%만큼 동시 폭증**하는 하이퍼 오버클럭 상태가 됩니다. (쿨타임 `13초`)
""")
