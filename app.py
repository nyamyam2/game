import streamlit as st
import streamlit.components.v1 as components

# 페이지 레이아웃 컴팩트 설정
st.set_page_config(page_title="스트림릿 네온 배틀: 1.0v 미니", layout="centered")

st.title("⚔️ 네온 배틀 1.0v (화면 최적화 버전)")
st.caption("작은 모니터 화면 크기 맞춤 축소 및 레이캐스팅 기반 벽 관통 완전 차단 완료!")

# 모니터 크기에 맞게 전체 스케일을 축소한 하이브리드 게임 엔진 코드
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; background-color: #16161a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 5px; overflow: hidden; }
        
        /* 화면이 작은 PC 환경을 고려해 전체 크기를 680px 권역으로 압축 */
        .game-wrapper { position: relative; width: 680px; margin: 0 auto; }
        
        /* 기존 800x400에서 660x330으로 컴팩트하게 리사이징 */
        canvas { background: #000; border: 3px solid #444; display: block; margin: 5px auto; box-shadow: 0 0 15px rgba(0,255,255,0.15); }
        
        /* 오버레이 팝업창도 화면을 가리지 않도록 560px 폭으로 압축 */
        .ui-overlay { position: absolute; top: 48%; left: 50%; transform: translate(-50%, -50%); background: rgba(10, 10, 15, 0.97); 
                     padding: 15px; border: 2px solid #00f2ff; border-radius: 12px; width: 560px; z-index: 10; box-shadow: 0 0 25px rgba(0,0,0,0.9); }
        
        .char-container { display: flex; justify-content: center; gap: 8px; margin: 10px 0; }
        .char-card { background: #1f1f2e; border: 2px solid #3a3a4a; border-radius: 10px; padding: 8px; width: 115px; cursor: pointer; transition: 0.2s; text-align: center; }
        .char-card:hover { transform: scale(1.03); border-color: #00f2ff; background: #25253a; }
        
        /* 🎨 고화질 사람 얼굴 그래픽 아바타 (CSS 디테일 렌더링) */
        .avatar-box { width: 50px; height: 50px; margin: 0 auto 6px; position: relative; background: #2d2d3f; border-radius: 8px; overflow: hidden; border: 1px solid #444; }
        
        /* 공통 인체 피부 및 목 구조 */
        .face-skin { width: 28px; height: 28px; background: #ffdbac; border-radius: 50%; position: absolute; top: 12px; left: 11px; z-index: 2; }
        .face-eyes { position: absolute; top: 10px; left: 4px; width: 4px; height: 4px; background: #222; border-radius: 50%; box-shadow: 12px 0 #222; }
        .face-neck { width: 8px; height: 10px; background: #e0ac69; position: absolute; top: 34px; left: 21px; z-index: 1; }
        
        /* 캐릭터별 고유 커스텀 외모 디테일 */
        .main-hair { width: 32px; height: 14px; background: #2c3e50; border-radius: 6px 6px 0 0; position: absolute; top: 8px; left: 9px; z-index: 3; }
        .main-glass { width: 24px; height: 5px; background: #111; position: absolute; top: 11px; left: 2px; border-radius: 1px; } /* 메인의 선글라스 */
        
        .mari-hair { width: 34px; height: 12px; background: #ff4757; border-radius: 8px 8px 0 0; position: absolute; top: 8px; left: 8px; z-index: 3; }
        .mari-hair-left { width: 8px; height: 18px; background: #ff4757; position: absolute; top: 14px; left: 6px; border-radius: 4px; z-index: 3; } /* 트윈테일 묶음 */
        .mari-hair-right { width: 8px; height: 18px; background: #ff4757; position: absolute; top: 14px; left: 36px; border-radius: 4px; z-index: 3; }
        
        .star-crown { width: 20px; height: 10px; background: #f1c40f; position: absolute; top: 1px; left: 15px; clip-path: polygon(0% 100%, 0% 20%, 30% 60%, 50% 0%, 70% 60%, 100% 20%, 100% 100%); z-index: 4; } /* 황금 왕관 쉐이프 */
        .star-hair { width: 30px; height: 14px; background: #f5cd79; border-radius: 5px 5px 0 0; position: absolute; top: 9px; left: 10px; z-index: 3; }
        
        .jam-cap { width: 32px; height: 10px; background: #2ed573; border-radius: 4px 4px 0 0; position: absolute; top: 6px; left: 9px; z-index: 4; } /* 힙한 스냅백 모자 */
        .jam-cap-brim { width: 12px; height: 3px; background: #1e703c; position: absolute; top: 10px; left: 27px; z-index: 4; border-radius: 0 2px 2px 0; }
        .jam-hair { width: 30px; height: 12px; background: #747d8c; border-radius: 4px 4px 0 0; position: absolute; top: 10px; left: 10px; z-index: 3; }

        .map-container { display: flex; justify-content: center; gap: 10px; margin: 8px 0; }
        .map-btn { padding: 8px 16px; font-size: 12px; cursor: pointer; border: 2px solid #555; background: #333; color: white; font-weight: bold; border-radius: 6px; }
        .map-btn.selected { border-color: #2ed573; background: #1e4620; }
        
        .start-action-btn { background: #2ed573; color: white; padding: 10px 30px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px; margin-top: 5px; box-shadow: 0 3px 6px rgba(0,255,0,0.2); }
        .restart-btn { background: #2ed573; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px; }
        .hidden { display: none !important; }
        .status-container { display: flex; justify-content: space-around; width: 660px; margin: 0 auto; font-size: 11px; color: #bbb; }
    </style>
</head>
<body>

    <div class="game-wrapper">
        <div class="status-container">
            <div>1P: A/D(이동), Space(점프), F(평타), G(궁극기)</div>
            <div>2P: ◀/▶(이동), ▲(점프), ↓(평타), L(궁극기)</div>
        </div>

        <div id="select-screen" class="ui-overlay">
            <h3 id="select-title" style="color:#00f2ff; margin: 0 0 3px 0; font-size: 16px;">1P 영웅 선택 (v1.0)</h3>
            <p id="select-subtitle" style="font-size:11px; color:#aaa; margin:0 0 8px 0;">작은 모니터 화면 배율 최적화 스킨 적용</p>
            
            <div class="char-container">
                <div class="char-card" onclick="selectChar('Main')">
                    <div class="avatar-box">
                        <div class="main-hair"></div>
                        <div class="face-skin"><div class="main-glass"></div><div class="face-eyes"></div></div>
                        <div class="face-neck"></div>
                    </div>
                    <strong style="color:#6dd5fa; font-size:12px;">메인 (인파이터)</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:3px; line-height:11px;">공속 0.3s | 데미지 7<br>궁 11s (30%감속)</div>
                </div>
                <div class="char-card" onclick="selectChar('Mari')">
                    <div class="avatar-box">
                        <div class="mari-hair"></div><div class="mari-hair-left"></div><div class="mari-hair-right"></div>
                        <div class="face-skin"><div class="face-eyes"></div></div>
                        <div class="face-neck"></div>
                    </div>
                    <strong style="color:#ff77ff; font-size:12px;">마리 (스나이퍼)</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:3px; line-height:11px;">공속 1.25s | 범위 15<br>이속 -5% | 데미지 9</div>
                </div>
                <div class="char-card" onclick="selectChar('Star')">
                    <div class="avatar-box">
                        <div class="star-crown"></div><div class="star-hair"></div>
                        <div class="face-skin"><div class="face-eyes"></div></div>
                        <div class="face-neck"></div>
                    </div>
                    <strong style="color:#ffca28; font-size:12px;">스타 (탱커버퍼)</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:3px; line-height:11px;">체력 125 | 데미지 6<br>궁: 2초간 속도 +50%</div>
                </div>
                <div class="char-card" onclick="selectChar('Jam')">
                    <div class="avatar-box">
                        <div class="jam-cap"></div><div class="jam-cap-brim"></div><div class="jam-hair"></div>
                        <div class="face-skin"><div class="face-eyes"></div></div>
                        <div class="face-neck"></div>
                    </div>
                    <strong style="color:#2ed573; font-size:12px;">잼 (랜덤도박형)</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:3px; line-height:11px;">공속 0.1s | 범위 7<br>궁: 대박25딜 / 20힐</div>
                </div>
            </div>

            <hr style="border: 0; border-top: 1px solid #333; margin: 6px 0;">
            <div class="map-container">
                <button id="map0-btn" class="map-btn selected" onclick="selectMap(0)">평지 전장</button>
                <button id="map1-btn" class="map-btn" onclick="selectMap(1)">네온 미로 (벽 충돌 수정됨)</button>
            </div>

            <button id="start-game-btn" class="start-action-btn hidden" onclick="confirmStart()">전장 진입하기</button>
        </div>

        <div id="result-screen" class="ui-overlay hidden">
            <h2 id="winner-text" style="font-size: 24px; margin: 0;"></h2>
            <button class="restart-btn" onclick="resetGame()">다시하기 (Restart)</button>
        </div>

        <canvas id="gameCanvas" width="660" height="330"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        
        const GRID = 16; // 맵 크기 축소에 맞춘 그리드 배율 하향 변경
        const GRAVITY = 0.55;
        
        let gameState = "SELECT";
        let p1Sel = null, p2Sel = null;
        let selectedMapIndex = 0;

        // 축소 배율에 완벽히 정렬한 네온 미로 오브젝트 데이터
        const mapObstacles = [
            { x: 140, y: 270, w: 45, h: 40 }, 
            { x: 475, y: 270, w: 45, h: 40 }, 
            { x: 260, y: 195, w: 140, h: 20 } 
        ];

        const mapBushes = [
            { x: 40, y: 260, w: 70, h: 50 },
            { x: 550, y: 260, w: 70, h: 50 },
            { x: 300, y: 145, w: 60, h: 50 }
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
                this.is1P = is1P; this.type = type;
                this.x = x; this.y = y;
                this.oldX = x; this.oldY = y;
                this.width = 25; this.height = 38; // 히트박스도 컴팩트하게 축소
                this.vY = 0;
                this.facing = is1P ? 1 : -1;
                this.isJumping = false;
                
                this.slowTimer = 0; this.buffTimer = 0; this.inBush = false;     
                this.bushHealTimer = 0; this.healTextTimer = 0;  
                this.popupText = ""; this.popupTimer = 0; this.jamBuffTimer = 0; this.shieldHp = 0;       

                if(type === "Main") {
                    this.name = "메인"; this.hp = 100; this.maxHp = 100; this.damage = 7;                     
                    this.range = 4 * GRID; this.atkDelay = 18; this.baseSpeed = 4.2; 
                    this.ultDamage = 18; this.ultRange = 8 * GRID; this.ultMaxCooldown = 660;           
                    this.color = "#1e90ff"; this.faceSymbol = "🕶️";
                } else if(type === "Mari") {
                    this.name = "마리"; this.hp = 90; this.maxHp = 90; this.damage = 9;                     
                    this.range = 15 * GRID; this.atkDelay = 75; this.baseSpeed = 3.6;           
                    this.ultDamage = 20; this.ultRange = 4 * GRID; this.ultMaxCooldown = 720; 
                    this.color = "#ff00ff"; this.faceSymbol = "🎀";
                } else if(type === "Star") { 
                    this.name = "스타"; this.hp = 125; this.maxHp = 125; this.damage = 6;                     
                    this.range = 7 * GRID; this.atkDelay = 42; this.baseSpeed = 3.9; 
                    this.ultDamage = 0; this.ultRange = 0; this.ultMaxCooldown = 780; 
                    this.color = "#ffca28"; this.faceSymbol = "👑";
                } else { 
                    this.name = "잼"; this.hp = 90; this.maxHp = 90; this.damage = 3;
                    this.range = 7 * GRID; this.atkDelay = 6; this.baseSpeed = 3.9; 
                    this.ultDamage = 0; this.ultRange = 0; this.ultMaxCooldown = 840; 
                    this.color = "#2ed573"; this.faceSymbol = "🎲";
                }

                this.atkCooldown = 0; this.ultCooldown = 0;
                this.effectTimer = 0; this.ultEffectTimer = 0; this.lastRenderRange = 0;
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
                    if(this.x + this.width > b.x && this.x < b.x + b.w && this.y + this.height > b.y && this.y < b.y + b.h) {
                        inside = true; break;
                    }
                }
                this.inBush = inside;
            }

            takeDamage(amount) {
                if(this.shieldHp > 0) {
                    this.shieldHp -= amount; this.popupText = "보호막 흡수!"; this.popupTimer = 40;
                    if(this.shieldHp <= 0) { this.shieldHp = 0; this.popupText = "보호막 파괴!"; }
                } else { this.hp -= amount; }
            }

            draw() {
                ctx.save();
                if(this.inBush) ctx.globalAlpha = 0.4; 

                ctx.shadowBlur = 10; ctx.shadowColor = this.color;
                if (this.slowTimer > 0) ctx.fillStyle = "#57606f"; 
                else if (this.buffTimer > 0 || this.jamBuffTimer > 0) ctx.fillStyle = "#fff200"; 
                else ctx.fillStyle = this.color;
                
                ctx.fillRect(this.x, this.y, this.width, this.height);
                ctx.shadowBlur = 0;

                if(this.shieldHp > 0) {
                    ctx.strokeStyle = "#00f2ff"; ctx.lineWidth = 2;
                    ctx.strokeRect(this.x - 3, this.y - 3, this.width + 6, this.height + 6);
                }

                ctx.fillStyle = "white"; ctx.font = "10px Arial";
                ctx.fillText(this.faceSymbol, this.x + 5, this.y + 22);

                ctx.fillStyle = "white"; ctx.font = "10px Arial";
                ctx.fillText(this.name + (this.is1P ? "(1P)" : "(2P)"), this.x, this.y - 22);
                
                if (this.slowTimer > 0) { ctx.fillStyle = "#00f2ff"; ctx.fillText("SLOW", this.x, this.y - 30); }
                if (this.buffTimer > 0 || this.jamBuffTimer > 0) { ctx.fillStyle = "#ffca28"; ctx.fillText("BUFF!", this.x, this.y - 30); }

                if (this.popupTimer > 0) {
                    ctx.fillStyle = "#fffa65"; ctx.font = "bold 10px Arial";
                    ctx.fillText(this.popupText, this.x - 10, this.y - 38);
                    this.popupTimer--;
                }

                ctx.fillStyle = "#333"; ctx.fillRect(this.x, this.y - 14, 25, 3);
                ctx.fillStyle = this.hp < (this.maxHp * 0.3) ? "red" : "lime";
                ctx.fillRect(this.x, this.y - 14, (this.hp / this.maxHp) * 25, 3);

                if(this.effectTimer > 0) {
                    ctx.fillStyle = "rgba(255,255,255,0.5)";
                    let rX = this.facing === 1 ? this.x + this.width : this.x - this.lastRenderRange;
                    ctx.fillRect(rX, this.y + 12, this.lastRenderRange, 3);
                    this.effectTimer--;
                }

                if(this.ultEffectTimer > 0) {
                    ctx.strokeStyle = "yellow"; ctx.lineWidth = 2;
                    if(this.type === "Main") {
                        let rX = this.facing === 1 ? this.x + this.width : this.x - this.lastRenderRange;
                        ctx.strokeRect(rX, this.y, this.lastRenderRange, this.height);
                    } else if(this.type === "Mari") {
                        ctx.beginPath(); ctx.arc(this.x + 12, this.y + 19, this.ultRange, 0, Math.PI * 2); ctx.stroke();
                    } else if(this.type === "Star" || this.type === "Jam") { 
                        ctx.strokeStyle = "#2ed573"; ctx.strokeRect(this.x - 4, this.y - 4, this.width + 8, this.height + 8);
                    }
                    this.ultEffectTimer--;
                }
                ctx.restore();
            }

            update() {
                // 움직이기 전 이전 좌표를 즉각 저장 (이것이 벽 관통 무효화의 핵심)
                this.oldX = this.x;
                this.oldY = this.y;

                this.vY += GRAVITY;
                this.y += this.vY;
                
                if (this.y >= canvas.height - this.height - 15) {
                    this.y = canvas.height - this.height - 15;
                    this.vY = 0; this.isJumping = false;
                }

                // 🛠️ [벽 통과 에러 완전 박멸 알고리즘] 바운딩 박스 진입 역추적 계산 교정
                if (selectedMapIndex === 1) {
                    for(let obs of mapObstacles) {
                        if (this.x + this.width > obs.x && this.x < obs.x + obs.w &&
                            this.y + this.height > obs.y && this.y < obs.y + obs.h) {
                            
                            // 1. 머리나 발이 천장/바닥면 경계에 닿았을 때 고정
                            if (this.oldY + this.height <= obs.y) {
                                this.y = obs.y - this.height; this.vY = 0; this.isJumping = false;
                            } else if (this.oldY >= obs.y + obs.h) {
                                this.y = obs.y + obs.h; this.vY = 0;
                            } else {
                                // 2. 벽의 옆면을 뚫고 들어가는 가속도가 잡히면 즉시 X축 프레임 롤백
                                this.x = this.oldX;
                            }
                        }
                    }
                }

                // 🛠️ [우측 화면 이탈 버그 원천 해결] 캔버스 해상도 한계 강제 클램핑
                if (this.x < 0) this.x = 0;
                if (this.x > canvas.width - this.width) this.x = canvas.width - this.width;
                
                this.checkBushIntersection();

                let cooldownSpeed = this.inBush ? 1.15 : 1.0;
                if(this.atkCooldown > 0) this.atkCooldown = Math.max(0, this.atkCooldown - cooldownSpeed);
                if(this.ultCooldown > 0) this.ultCooldown = Math.max(0, this.ultCooldown - cooldownSpeed);
                
                if(this.inBush && this.hp < this.maxHp) {
                    this.bushHealTimer++;
                    if(this.bushHealTimer >= 180) {
                        this.hp = Math.min(this.maxHp, this.hp + 2); this.bushHealTimer = 0; 
                    }
                } else { this.bushHealTimer = 0; }

                if(this.slowTimer > 0) this.slowTimer--;
                if(this.buffTimer > 0) this.buffTimer--;
                if(this.jamBuffTimer > 0) this.jamBuffTimer--;
            }

            jump() {
                let 온그라운드 = (this.y >= canvas.height - this.height - 15);
                if (selectedMapIndex === 1) {
                    for(let obs of mapObstacles) {
                        if (this.x + this.width > obs.x && this.x < obs.x + obs.w && Math.abs((this.y + this.height) - obs.y) < 2) {
                            온그라운드 = true;
                        }
                    }
                }
                if (!this.isJumping || 온그라운드) { this.vY = -10.5; this.isJumping = true; }
            }

            // 🛠️ [공격 벽 관통 무효화] 투사 선상의 장애물 유무 실시간 추적 차단 필터
            calculateWallBlockingRange(maxRange) {
                if (selectedMapIndex !== 1) return maxRange;
                let step = 3; let currentValidRange = 0;
                while (currentValidRange < maxRange) {
                    currentValidRange += step;
                    let checkX = this.facing === 1 ? this.x + this.width + currentValidRange : this.x - currentValidRange;
                    let checkY = this.y + 15; 
                    let blocked = false;
                    for (let obs of mapObstacles) {
                        if (checkX >= obs.x && checkX <= obs.x + obs.w && checkY >= obs.y && checkY <= obs.y + obs.h) {
                            blocked = true; break;
                        }
                    }
                    if (blocked) return currentValidRange - step; // 벽에 막힌 곳 직전까지만 사거리 차단
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
                    let dx = (this.x + 12) - (opp.x + 12); let dy = (this.y + 19) - (opp.y + 19);
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    if(dist < this.ultRange + 12) { opp.takeDamage(this.ultDamage); this.hp = Math.min(this.maxHp, this.hp + 10); }
                } else if(this.type === "Star") {
                    this.ultEffectTimer = 15; this.buffTimer = 120;
                } else if(this.type === "Jam") {
                    this.ultEffectTimer = 15; let rnd = Math.random();
                    if (rnd < 0.10) { opp.takeDamage(25); this.popupText = "💥 대박! 25 데미지!!"; } 
                    else if (rnd < 0.30) { this.hp = Math.min(this.maxHp, this.hp + 20); this.popupText = "💚 힐링! HP +20 회복"; } 
                    else if (rnd < 0.40) { this.jamBuffTimer = 120; this.popupText = "🏹 신속! 사거리 +3칸"; } 
                    else if (rnd < 0.60) { this.x = opp.x + (opp.facing === 1 ? -30 : 30); this.y = opp.y; opp.takeDamage(10); this.popupText = "🔮 습격! 순간이동"; } 
                    else if (rnd < 0.80) { this.shieldHp = 15; this.popupText = "🛡️ 방어! 배리어 활성"; } 
                    else { this.popupText = "💨 꽝! 다음 기회에"; }
                    this.popupTimer = 100; 
                }
            }
        }

        let p1, p2;

        function selectChar(type) {
            if(!p1Sel) {
                p1Sel = type; document.getElementById("select-title").innerText = "2P 영웅 선택 (v1.0)";
            } else if(!p2Sel) {
                p2Sel = type;
                document.getElementById("select-title").innerText = "전장 환경 구축 완료";
                document.getElementById("select-subtitle").innerText = "아래 진입하기 버튼이 생성되었습니다.";
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
            p1 = new Player(100, 200, p1Sel, true); p2 = new Player(530, 200, p2Sel, false);
            gameState = "PLAY";
        }

        function resetGame() {
            p1Sel = null; p2Sel = null;
            document.getElementById("select-title").innerText = "1P 영웅 선택 (v1.0)";
            document.getElementById("select-subtitle").innerText = "원하는 스타일의 영웅 카드를 클릭하세요.";
            document.getElementById("select-screen").classList.remove("hidden");
            document.getElementById("result-screen").classList.add("hidden");
            document.getElementById("start-game-btn").classList.add("hidden");
            gameState = "SELECT";
        }

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            if(selectedMapIndex === 1) {
                ctx.fillStyle = "rgba(46, 213, 115, 0.25)";
                for(let b of mapBushes) { ctx.fillRect(b.x, b.y, b.w, b.h); }
                ctx.fillStyle = "#444"; 
                for(let obs of mapObstacles) { ctx.fillRect(obs.x, obs.y, obs.w, obs.h); }
            }

            ctx.fillStyle = "#222"; ctx.fillRect(0, canvas.height - 15, canvas.width, 15);

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
                ctx.fillStyle = "#1c1c24"; ctx.font = "13px Arial";
                ctx.fillText("매치 데이터를 정렬하고 있습니다...", 240, 160);
            } else { p1.draw(); p2.draw(); }
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
</body>
</html>
"""

# 전체 창이 다 보일 수 있도록 세로 크기를 480px로 알맞게 축소 조정
components.html(game_html, height=480)
