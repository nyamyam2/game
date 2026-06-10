import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="스트림릿 네온 배틀: 1.0v 수정판", layout="centered")

st.title("⚔️ 스트림릿 2P 배틀: 1.0v 최종 수정본")
st.caption("우측 맵 이탈·벽 끼임 완벽 해결 및 UI 짤림 개선 완료!")

# 게임 로직 (HTML/JS/CSS)
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; background-color: #1a1a1a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 10px; overflow-x: hidden; }
        
        /* 전체적인 컨테이너 레이아웃 배치 최적화 (버튼 짤림 방지) */
        .game-wrapper { position: relative; width: 800px; margin: 0 auto; padding-bottom: 20px; }
        
        canvas { background: #000; border: 3px solid #333; display: block; margin: 10px auto; box-shadow: 0 0 20px rgba(0,255,255,0.2); }
        
        /* UI 오버레이 높이와 간격 조절로 하단 버튼 시인성 확보 */
        .ui-overlay { position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%); background: rgba(12, 12, 18, 0.96); 
                     padding: 20px; border: 2px solid #00f2ff; border-radius: 16px; width: 640px; z-index: 10; box-shadow: 0 0 35px rgba(0,0,0,0.95); }
        
        .char-container { display: flex; justify-content: center; gap: 12px; margin: 15px 0; }
        .char-card { background: #22222e; border: 2px solid #3a3a4a; border-radius: 12px; padding: 10px; width: 135px; cursor: pointer; transition: 0.3s; text-align: center; }
        .char-card:hover { transform: scale(1.05); border-color: #00f2ff; background: #2a2a3a; }
        
        /* 🎨 이모티콘 탈피: CSS 조합형 사람 캐릭터 그래픽 아바타 */
        .human-avatar { width: 50px; height: 55px; margin: 0 auto 10px; position: relative; background: transparent; }
        .human-head { width: 32px; height: 32px; border-radius: 50%; background: #ffdbac; margin: 0 auto; position: relative; z-index: 2; box-shadow: 0 2px 5px rgba(0,0,0,0.3); }
        .human-body { width: 44px; height: 20px; border-radius: 6px 6px 0 0; margin: -4px auto 0; position: relative; z-index: 1; }
        
        /* 캐릭터별 세부 사람 얼굴/의상 스타일 특징 정의 */
        .main-head { background: #e0ac69; border-top: 8px solid #222; } /* 검은 머리 크루 */
        .main-head::before { content: ''; position: absolute; top: 12px; left: 4px; width: 24px; height: 6px; background: #111; border-radius: 2px; } /* 선글라스 */
        .main-body { background: #1e90ff; } /* 블루 정장 */

        .mari-head { background: #f1c27d; border-top: 6px solid #ff77ff; } /* 핑크 헤어 */
        .mari-head::before { content: '🎀'; position: absolute; top: -10px; left: 6px; font-size: 14px; } /* 리본 코디 */
        .mari-body { background: #ff00ff; } /* 핑크 드레스 */

        .star-head { background: #ffdbac; border-top: 6px solid #f1c40f; } /* 금발 머리 */
        .star-head::before { content: '👑'; position: absolute; top: -12px; left: 6px; font-size: 14px; } /* 황금 왕관 */
        .star-body { background: #f39c12; } /* 황실 가운 */

        .jam-head { background: #e0ac69; border-top: 8px solid #27ae60; } /* 록색 캡모자 스타일 */
        .jam-head::before { content: ''; position: absolute; top: 14px; left: 6px; width: 6px; height: 4px; background: #333; border-radius: 50%; box-shadow: 14px 0 #333; } /* 동그란 눈 */
        .jam-body { background: #2ed573; } /* 그린 셔츠 */

        .map-container { display: flex; justify-content: center; gap: 15px; margin: 10px 0; }
        .map-btn { padding: 10px 20px; cursor: pointer; border: 2px solid #555; background: #333; color: white; font-weight: bold; border-radius: 8px; transition: 0.2s; }
        .map-btn.selected { border-color: #2ed573; background: #1e4620; }
        
        /* 절대 잘리지 않도록 크기와 마진을 최적화한 하단 진입 버튼 */
        .start-action-btn { background: #2ed573; color: white; padding: 14px 40px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 10px; display: inline-block; box-shadow: 0 4px 10px rgba(0,255,0,0.3); }
        .start-action-btn:hover { background: #26af5f; }
        
        .restart-btn { background: #2ed573; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px; }
        .hidden { display: none !important; }
        .status-container { display: flex; justify-content: space-around; width: 800px; margin: 0 auto; font-size: 13px; color: #aaa; }
    </style>
</head>
<body>

    <div class="game-wrapper">
        <div class="status-container">
            <div>1P: A/D(이동), Space(점프), F(공격), G(궁극기)</div>
            <div>2P: ◀/▶(이동), ▲(점프), ↓(공격), L(궁극기)</div>
        </div>

        <div id="select-screen" class="ui-overlay">
            <h2 id="select-title" style="color:#00f2ff; margin: 0 0 5px 0;">1P 캐릭터 선택 (v1.0)</h2>
            <p id="select-subtitle" style="font-size:12px; color:#aaa; margin:0 0 10px 0;">이모티콘을 벗어난 리얼 휴먼 도트 스쿼드</p>
            
            <div class="char-container">
                <div class="char-card" onclick="selectChar('Main')">
                    <div class="human-avatar">
                        <div class="human-head main-head"></div>
                        <div class="human-body main-body"></div>
                    </div>
                    <strong style="color:#6dd5fa; font-size:14px;">메인</strong>
                    <div style="font-size:9px; color:#bbb; margin-top:4px; line-height:12px;">공속 0.3s | 공격 7<br>궁 11s (30%감속)</div>
                </div>
                <div class="char-card" onclick="selectChar('Mari')">
                    <div class="human-avatar">
                        <div class="human-head mari-head"></div>
                        <div class="human-body mari-body"></div>
                    </div>
                    <strong style="color:#ff77ff; font-size:14px;">마리</strong>
                    <div style="font-size:9px; color:#bbb; margin-top:4px; line-height:12px;">공속 1.25s | 범위 15<br>이속 -5% | 공격 9</div>
                </div>
                <div class="char-card" onclick="selectChar('Star')">
                    <div class="human-avatar">
                        <div class="human-head star-head"></div>
                        <div class="human-body star-body"></div>
                    </div>
                    <strong style="color:#ffca28; font-size:14px;">스타</strong>
                    <div style="font-size:9px; color:#bbb; margin-top:4px; line-height:12px;">체력 125 | 공격 6<br>궁: 2초간 속도 +50%</div>
                </div>
                <div class="char-card" onclick="selectChar('Jam')">
                    <div class="human-avatar">
                        <div class="human-head jam-head"></div>
                        <div class="human-body jam-body"></div>
                    </div>
                    <strong style="color:#2ed573; font-size:14px;">잼</strong>
                    <div style="font-size:9px; color:#bbb; margin-top:4px; line-height:12px;">공속 0.1s | 범위 7<br>궁: 대박25딜 / 20힐</div>
                </div>
            </div>

            <hr style="border: 0; border-top: 1px solid #333; margin: 10px 0;">
            <h3 style="margin: 0 0 5px 0; font-size:15px;">전장 선택</h3>
            <div class="map-container">
                <button id="map0-btn" class="map-btn selected" onclick="selectMap(0)">평지 아레나</button>
                <button id="map1-btn" class="map-btn" onclick="selectMap(1)">네온 미로 (버그 픽스 완료)</button>
            </div>

            <button id="start-game-btn" class="start-action-btn hidden" onclick="confirmStart()">전장으로 진입하기</button>
        </div>

        <div id="result-screen" class="ui-overlay hidden">
            <h2 id="winner-text" style="font-size: 30px; margin: 0;"></h2>
            <button class="restart-btn" onclick="resetGame()">다시하기 (Restart)</button>
        </div>

        <canvas id="gameCanvas" width="800" height="400"></canvas>
    </div>

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
                this.oldX = x; 
                this.oldY = y;
                this.width = 30;
                this.height = 45;
                this.vY = 0;
                this.facing = is1P ? 1 : -1;
                this.isJumping = false;
                
                this.slowTimer = 0;
                this.buffTimer = 0;
                this.inBush = false;     
                this.bushHealTimer = 0;  
                this.healTextTimer = 0;  
                this.popupText = "";     
                this.popupTimer = 0;
                this.jamBuffTimer = 0;   
                this.shieldHp = 0;       

                if(type === "Main") {
                    this.name = "메인"; this.hp = 100; this.maxHp = 100; this.damage = 7;                     
                    this.range = 4 * GRID; this.atkDelay = 18; this.baseSpeed = 5 * 1.13; 
                    this.ultDamage = 18; this.ultRange = 8 * GRID; this.ultMaxCooldown = 660;           
                    this.color = "#1e90ff"; this.faceSymbol = "🕶️";
                } else if(type === "Mari") {
                    this.name = "마리"; this.hp = 90; this.maxHp = 90; this.damage = 9;                     
                    this.range = 15 * GRID; this.atkDelay = 75; this.baseSpeed = 5 * 0.92;           
                    this.ultDamage = 20; this.ultRange = 4 * GRID; this.ultMaxCooldown = 720; 
                    this.color = "#ff00ff"; this.faceSymbol = "🎀";
                } else if(type === "Star") { 
                    this.name = "스타"; this.hp = 125; this.maxHp = 125; this.damage = 6;                     
                    this.range = 7 * GRID; this.atkDelay = 42; this.baseSpeed = 5; 
                    this.ultDamage = 0; this.ultRange = 0; this.ultMaxCooldown = 780; 
                    this.color = "#ffca28"; this.faceSymbol = "👑";
                } else { 
                    this.name = "잼"; this.hp = 90; this.maxHp = 90; this.damage = 3;
                    this.range = 7 * GRID; this.atkDelay = 6; this.baseSpeed = 5; 
                    this.ultDamage = 0; this.ultRange = 0; this.ultMaxCooldown = 840; 
                    this.color = "#2ed573"; this.faceSymbol = "🎲";
                }

                this.atkCooldown = 0; this.ultCooldown = 0;
                this.effectTimer = 0; this.ultEffectTimer = 0;
                this.lastRenderRange = 0;
            }

            get currentSpeed() {
                let speed = this.baseSpeed;
                if (this.slowTimer > 0) speed *= 0.70;    
                if (this.buffTimer > 0) speed *= 1.50;    
                return speed;
            }

            get currentRange() {
                let r = this.range;
                if (this.type === "Jam" && this.jamBuffTimer > 0) r += 3 * GRID; 
                return r;
            }

            get currentAtkDelay() {
                if (this.type === "Star" && this.buffTimer > 0) return this.atkDelay * 0.50; 
                return this.atkDelay;
            }

            checkBushIntersection() {
                if (selectedMapIndex !== 1) { this.inBush = false; return; }
                let inside = false;
                for(let b of mapBushes) {
                    if(this.x + this.width > b.x && this.x < b.x + b.w &&
                       this.y + this.height > b.y && this.y < b.y + b.h) {
                        inside = true; break;
                    }
                }
                this.inBush = inside;
            }

            takeDamage(amount) {
                if(this.shieldHp > 0) {
                    this.shieldHp -= amount;
                    this.popupText = "보호막 흡수!";
                    this.popupTimer = 40;
                    if(this.shieldHp <= 0) { this.shieldHp = 0; this.popupText = "보호막 파괴!"; }
                } else { this.hp -= amount; }
            }

            draw() {
                ctx.save();
                if(this.inBush) ctx.globalAlpha = 0.4; 

                ctx.shadowBlur = 15;
                ctx.shadowColor = this.color;
                if (this.slowTimer > 0) ctx.fillStyle = "#57606f"; 
                else if (this.buffTimer > 0 || this.jamBuffTimer > 0) ctx.fillStyle = "#fff200"; 
                else ctx.fillStyle = this.color;
                
                ctx.fillRect(this.x, this.y, this.width, this.height);
                ctx.shadowBlur = 0;

                if(this.shieldHp > 0) {
                    ctx.strokeStyle = "#00f2ff"; ctx.lineWidth = 3;
                    ctx.strokeRect(this.x - 4, this.y - 4, this.width + 8, this.height + 8);
                }

                ctx.fillStyle = "white"; ctx.font = "12px Arial";
                ctx.fillText(this.faceSymbol, this.x + 8, this.y + 25);

                ctx.fillStyle = "white"; ctx.font = "11px Arial";
                ctx.fillText(this.name + (this.is1P ? "(1P)" : "(2P)"), this.x, this.y - 30);
                
                if (this.slowTimer > 0) { ctx.fillStyle = "#00f2ff"; ctx.fillText("SLOW", this.x, this.y - 38); }
                if (this.buffTimer > 0 || this.jamBuffTimer > 0) { ctx.fillStyle = "#ffca28"; ctx.fillText("BUFF!!", this.x, this.y - 38); }

                if (this.popupTimer > 0) {
                    ctx.fillStyle = "#fffa65"; ctx.font = "bold 11px Arial";
                    ctx.fillText(this.popupText, this.x - 10, this.y - 48);
                    this.popupTimer--;
                }

                if (this.healTextTimer > 0) {
                    ctx.fillStyle = "#2ed573"; ctx.font = "bold 12px Arial";
                    ctx.fillText("+2", this.x + this.width + 5, this.y + 10);
                    this.healTextTimer--;
                }

                ctx.fillStyle = "#333";
                ctx.fillRect(this.x, this.y - 20, 30, 4);
                ctx.fillStyle = this.hp < (this.maxHp * 0.3) ? "red" : "lime";
                ctx.fillRect(this.x, this.y - 20, (this.hp / this.maxHp) * 30, 4);

                ctx.fillStyle = "rgba(255,255,255,0.3)";
                ctx.fillRect(this.x, this.y - 14, 30, 2);
                ctx.fillStyle = "yellow";
                let ultBar = (1 - this.ultCooldown / this.ultMaxCooldown) * 30;
                ctx.fillRect(this.x, this.y - 14, Math.max(0, ultBar), 2);

                if(this.effectTimer > 0) {
                    ctx.fillStyle = "rgba(255,255,255,0.5)";
                    let rX = this.facing === 1 ? this.x + this.width : this.x - this.lastRenderRange;
                    ctx.fillRect(rX, this.y + 15, this.lastRenderRange, 4);
                    this.effectTimer--;
                }

                if(this.ultEffectTimer > 0) {
                    ctx.strokeStyle = "yellow"; ctx.lineWidth = 2;
                    if(this.type === "Main") {
                        let rX = this.facing === 1 ? this.x + this.width : this.x - this.lastRenderRange;
                        ctx.strokeRect(rX, this.y, this.lastRenderRange, this.height);
                    } else if(this.type === "Mari") {
                        ctx.beginPath(); ctx.arc(this.x + 15, this.y + 22, this.ultRange, 0, Math.PI * 2); ctx.stroke();
                    } else if(this.type === "Star" || this.type === "Jam") { 
                        ctx.strokeStyle = "#2ed573"; ctx.strokeRect(this.x - 6, this.y - 6, this.width + 12, this.height + 12);
                    }
                    this.ultEffectTimer--;
                }
                ctx.restore();
            }

            update() {
                this.oldX = this.x;
                this.oldY = this.y;

                this.vY += GRAVITY;
                this.y += this.vY;
                
                if (this.y >= canvas.height - this.height - 20) {
                    this.y = canvas.height - this.height - 20;
                    this.vY = 0;
                    this.isJumping = false;
                }

                // 🛠️ [벽 통과 및 끼임 버그 정밀 수정] X/Y축 독립 변위 검사 기반 밀어내기
                if (selectedMapIndex === 1) {
                    for(let obs of mapObstacles) {
                        if (this.x + this.width > obs.x && this.x < obs.x + obs.w &&
                            this.y + this.height > obs.y && this.y < obs.y + obs.h) {
                            
                            // Y축 방향 진입 차단 처리
                            if (this.oldY + this.height <= obs.y) {
                                this.y = obs.y - this.height; this.vY = 0; this.isJumping = false;
                            } else if (this.oldY >= obs.y + obs.h) {
                                this.y = obs.y + obs.h; this.vY = 0;
                            } else {
                                // X축 방향 진입 무효화 (이전 유효 프레임 위치로 완전 고정)
                                this.x = this.oldX;
                            }
                        }
                    }
                }

                // 🛠️ [오른쪽 탈출 완전 차단] 하드코딩 경계 설정으로 화면 이탈 방지
                if (this.x < 0) this.x = 0;
                if (this.x > canvas.width - this.width) this.x = canvas.width - this.width;
                
                this.checkBushIntersection();

                let cooldownSpeed = this.inBush ? 1.15 : 1.0;
                if(this.atkCooldown > 0) this.atkCooldown = Math.max(0, this.atkCooldown - cooldownSpeed);
                if(this.ultCooldown > 0) this.ultCooldown = Math.max(0, this.ultCooldown - cooldownSpeed);
                
                if(this.inBush && this.hp < this.maxHp) {
                    this.bushHealTimer++;
                    if(this.bushHealTimer >= 180) {
                        this.hp = Math.min(this.maxHp, this.hp + 2);
                        this.bushHealTimer = 0; this.healTextTimer = 30; 
                    }
                } else { this.bushHealTimer = 0; }

                if(this.slowTimer > 0) this.slowTimer--;
                if(this.buffTimer > 0) this.buffTimer--;
                if(this.jamBuffTimer > 0) this.jamBuffTimer--;
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
                if (!this.isJumping || 온그라운드) { this.vY = -12; this.isJumping = true; }
            }

            calculateWallBlockingRange(maxRange) {
                if (selectedMapIndex !== 1) return maxRange;
                let step = 4; let currentValidRange = 0;
                while (currentValidRange < maxRange) {
                    currentValidRange += step;
                    let checkX = this.facing === 1 ? this.x + this.width + currentValidRange : this.x - currentValidRange;
                    let checkY = this.y + 18; 
                    let blocked = false;
                    for (let obs of mapObstacles) {
                        if (checkX >= obs.x && checkX <= obs.x + obs.w && checkY >= obs.y && checkY <= obs.y + obs.h) {
                            blocked = true; break;
                        }
                    }
                    if (blocked) return currentValidRange - step;
                }
                return maxRange;
            }

            attack(opp) {
                if(this.atkCooldown > 0) return;
                let validRange = this.calculateWallBlockingRange(this.currentRange);
                this.lastRenderRange = validRange; 
                this.effectTimer = 4; this.atkCooldown = this.currentAtkDelay; 
                
                let myL = this.facing === 1 ? this.x + this.width : this.x - validRange;
                let myR = this.facing === 1 ? this.x + this.width + validRange : this.x;

                if(myR >= opp.x && myL <= opp.x + opp.width && this.y + this.height >= opp.y && this.y <= opp.y + opp.height) {
                    opp.takeDamage(this.damage);
                }
            }

            useUltimate(opp) {
                if(this.ultCooldown > 0) return;
                this.ultCooldown = this.ultMaxCooldown;

                if(this.type === "Main") {
                    let validUltRange = this.calculateWallBlockingRange(this.ultRange);
                    this.lastRenderRange = validUltRange; this.ultEffectTimer = 15;
                    let myL = this.facing === 1 ? this.x + this.width : this.x - validUltRange;
                    let myR = this.facing === 1 ? this.x + this.width + validUltRange : this.x;
                    if(myR >= opp.x && myL <= opp.x + opp.width && this.y + this.height >= opp.y && this.y <= opp.y + opp.height) {
                        opp.takeDamage(this.ultDamage); opp.slowTimer = 90; 
                    }
                } else if(this.type === "Mari") {
                    this.ultEffectTimer = 15;
                    let dx = (this.x + 15) - (opp.x + 15); let dy = (this.y + 22) - (opp.y + 22);
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    if(dist < this.ultRange + 15) { opp.takeDamage(this.ultDamage); this.hp = Math.min(this.maxHp, this.hp + 10); }
                } else if(this.type === "Star") {
                    this.ultEffectTimer = 15; this.buffTimer = 120;
                } else if(this.type === "Jam") {
                    this.ultEffectTimer = 15; let rnd = Math.random();
                    if (rnd < 0.10) { opp.takeDamage(25); this.popupText = "💥 대박! 25 데미지!!"; } 
                    else if (rnd < 0.30) { this.hp = Math.min(this.maxHp, this.hp + 20); this.popupText = "💚 힐링! HP +20 회복"; } 
                    else if (rnd < 0.40) { this.jamBuffTimer = 120; this.popupText = "🏹 신속! 사거리 +3칸"; } 
                    else if (rnd < 0.60) { this.x = opp.x + (opp.facing === 1 ? -40 : 40); this.y = opp.y; opp.takeDamage(10); this.popupText = "🔮 습격! 순간이동 기습"; } 
                    else if (rnd < 0.80) { this.shieldHp = 15; this.popupText = "🛡️ 방어! 배리어 활성"; } 
                    else { this.popupText = "💨 꽝! 다음 기회에"; }
                    this.popupTimer = 100; 
                }
            }
        }

        let p1, p2;

        function selectChar(type) {
            if(!p1Sel) {
                p1Sel = type; document.getElementById("select-title").innerText = "2P 캐릭터 선택 (v1.0)";
            } else if(!p2Sel) {
                p2Sel = type;
                document.getElementById("select-title").innerText = "공식 전장 셋업 완료";
                document.getElementById("select-subtitle").innerText = "아래 버튼을 누르면 인게임 매치가 즉시 개시됩니다.";
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
            p1 = new Player(120, 200, p1Sel, true); p2 = new Player(650, 200, p2Sel, false);
            gameState = "PLAY";
        }

        function resetGame() {
            p1Sel = null; p2Sel = null;
            document.getElementById("select-title").innerText = "1P 캐릭터 선택 (v1.0)";
            document.getElementById("select-subtitle").innerText = "원하는 스타일의 영웅 카드를 클릭하세요.";
            document.getElementById("select-screen").classList.remove("hidden");
            document.getElementById("result-screen").classList.add("hidden");
            document.getElementById("start-game-btn").classList.add("hidden");
            gameState = "SELECT";
        }

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            if(selectedMapIndex === 1) {
                ctx.fillStyle = "rgba(46, 213, 115, 0.35)";
                for(let b of mapBushes) { ctx.fillRect(b.x, b.y, b.w, b.h); }
                ctx.fillStyle = "#4a4a4a"; 
                for(let obs of mapObstacles) { ctx.fillRect(obs.x, obs.y, obs.w, obs.h); }
            }

            ctx.fillStyle = "#333"; ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

            if(gameState === "PLAY") {
                p1.oldX = p1.x; p1.oldY = p1.y; p2.oldX = p2.x; p2.oldY = p2.y;

                if (keys["KeyA"]) { p1.x -= p1.currentSpeed; p1.facing = -1; }
                if (keys["KeyD"]) { p1.x += p1.currentSpeed; p1.facing = 1; }
                if (keys["Space"]) p1.jump();

                if (keys["ArrowLeft"]) { p2.x -= p2.currentSpeed; p2.facing = -1; }
                if (keys["ArrowRight"]) { p2.x += p2.currentSpeed; p2.facing = 1; }
                if (keys["ArrowUp"]) p2.jump();

                p1.update(); p2.update(); p1.draw(); p2.draw();

                if(p1.hp <= 0 || p2.hp <= 0) {
                    gameState = "END";
                    document.getElementById("result-screen").classList.remove("hidden");
                    document.getElementById("winner-text").innerText = p1.hp <= 0 ? "2P 승리!" : "1P 승리!";
                }
            } else if (gameState === "SELECT") {
                ctx.fillStyle = "#222"; ctx.font = "16px Arial";
                ctx.fillText("대기실에서 엔티티 데이터 동기화 중...", 260, 200);
            } else { p1.draw(); p2.draw(); }
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
</body>
</html>
"""

components.html(game_html, height=570)
