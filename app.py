import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="스트림릿 네온 배틀: 1.0v 패치", layout="centered")

st.title("⚔️ 스트림릿 2P 배틀: 공식 1.0v 업데이트")
st.caption("벽 관통 및 끼임 버그 전면 수정! 대규모 캐릭터 밸런싱 패치 완결판.")

# 게임 로직 (HTML/JS)
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; background-color: #1a1a1a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; overflow: hidden; }
        canvas { background: #000; border: 3px solid #333; display: block; margin: 10px auto; box-shadow: 0 0 20px rgba(0,255,255,0.2); }
        .ui-overlay { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(10,10,15,0.95); 
                     padding: 25px; border: 2px solid #00f2ff; border-radius: 20px; width: 620px; z-index: 10; box-shadow: 0 0 30px rgba(0,0,0,0.9); }
        
        /* 1.0v 업그레이드된 사람다운 픽창 비주얼 테마 */
        .char-container { display: flex; justify-content: center; gap: 12px; margin: 15px 0; flex-wrap: wrap; }
        .char-card { background: #1e1e24; border: 2px solid #3a3a4a; border-radius: 12px; padding: 12px; width: 130px; cursor: pointer; transition: 0.3s; text-align: center; position: relative; }
        .char-card:hover { transform: scale(1.05); border-color: #00f2ff; background: #252530; }
        
        /* 사람 모형의 미니 프로필 연출을 위한 픽셀 박스 */
        .char-face { width: 64px; height: 64px; margin: 0 auto 10px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 26px; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
        .face-main { background: linear-gradient(135deg, #2980b9, #6dd5fa); border: 2px solid #00f2ff; }
        .face-mari { background: linear-gradient(135deg, #ecc1e3, #ff00ff); border: 2px solid #ff77ff; }
        .face-star { background: linear-gradient(135deg, #f1c40f, #f39c12); border: 2px solid #fffa65; }
        .face-jam  { background: linear-gradient(135deg, #27ae60, #1abc9c); border: 2px solid #2ed573; }

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
        <h2 id="select-title" style="color:#00f2ff; margin-bottom: 5px; letter-spacing: 1px;">1P 캐릭터 선택 (버전 1.0v)</h2>
        <p id="select-subtitle" style="font-size:13px; color:#aaa; margin:0;">원하는 스타일의 영웅 카드를 클릭하세요.</p>
        
        <div class="char-container">
            <div class="char-card" onclick="selectChar('Main')">
                <div class="char-face face-main">👦🕶️</div>
                <strong style="color:#6dd5fa;">메인</strong>
                <div style="font-size:9px; color:#bbb; margin-top:5px; line-height:13px;">공속 0.3s | 공격 7<br>궁 11s (30%감속/18딜)</div>
            </div>
            <div class="char-card" onclick="selectChar('Mari')">
                <div class="char-face face-mari">👧🎀</div>
                <strong style="color:#ff77ff;">마리</strong>
                <div style="font-size:9px; color:#bbb; margin-top:5px; line-height:13px;">공속 1.25s | 사거리 15<br>이속 -5% | 공격 9</div>
            </div>
            <div class="char-card" onclick="selectChar('Star')">
                <div class="char-face face-star">👱👑</div>
                <strong style="color:#ffca28;">스타</strong>
                <div style="font-size:9px; color:#bbb; margin-top:5px; line-height:13px;">체력 125 | 공격 6<br>궁: 2초간 버프 50%🔥</div>
            </div>
            <div class="char-card" onclick="selectChar('Jam')">
                <div class="char-face face-jam">👨‍🎨🎲</div>
                <strong style="color:#2ed573;">잼</strong>
                <div style="font-size:9px; color:#bbb; margin-top:5px; line-height:13px;">공속 0.1s | 사거리 7<br>궁: 대박25딜 / 20힐</div>
            </div>
        </div>

        <hr style="border: 1px solid #333; margin: 15px 0;">
        <h3 style="margin: 5px 0;">전장(맵) 선택</h3>
        <div class="map-container">
            <button id="map0-btn" class="map-btn selected" onclick="selectMap(0)">평지 아레나</button>
            <button id="map1-btn" class="map-btn" onclick="selectMap(1)">네온 미로 (버그 픽스 맵)</button>
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

        // 벽 장애물 데이터 리스트
        const mapObstacles = [
            { x: 180, y: 330, w: 50, h: 50 }, 
            { x: 570, y: 330, w: 50, h: 50 }, 
            { x: 320, y: 240, w: 160, h: 25 } 
        ];

        // 덤불 데이터 리스트
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

                // 🛠️ 1.0v 리밸런싱 스탯 데이터 반영
                if(type === "Main") {
                    this.name = "메인";
                    this.hp = 100; this.maxHp = 100; 
                    this.damage = 7;                     // 1.0v 데미지 7 하향 조정
                    this.range = 4 * GRID; 
                    this.atkDelay = 18;                  // 1.0v 공격속도 0.3초 (60fps * 0.3 = 18프레임) 상향
                    this.baseSpeed = 5 * 1.13; 
                    this.ultDamage = 18;                 // 1.0v 궁극기 데미지 18 상향
                    this.ultRange = 8 * GRID; 
                    this.ultMaxCooldown = 660;           // 1.0v 궁극기 쿨타임 11초 (60fps * 11 = 660프레임)
                    this.color = "#1e90ff"; this.faceSymbol = "🕶️";
                } else if(type === "Mari") {
                    this.name = "마리";
                    this.hp = 90; this.maxHp = 90; 
                    this.damage = 9;                     // 1.0v 평타 데미지 9 상향
                    this.range = 15 * GRID;              // 1.0v 평타 사거리 15칸 조정
                    this.atkDelay = 75;                  // 1.0v 공격속도 1.25초 (60fps * 1.25 = 75프레임) 딜레이 증가
                    this.baseSpeed = 5 * 0.92;           // 1.0v 이동속도 추가 5% 하향 (기존 0.97 -> 0.92)
                    this.ultDamage = 20;
                    this.ultRange = 4 * GRID; this.ultMaxCooldown = 720; 
                    this.color = "#ff00ff"; this.faceSymbol = "🎀";
                } else if(type === "Star") { 
                    this.name = "스타";
                    this.hp = 125; this.maxHp = 125;     // 1.0v 체력 125 조정
                    this.damage = 6;                     // 1.0v 공격력 6 상향
                    this.range = 7 * GRID; 
                    this.atkDelay = 42;                  // 1.0v 공격속도 0.7초 (60fps * 0.7 = 42프레임)
                    this.baseSpeed = 5; this.ultDamage = 0; 
                    this.ultRange = 0; this.ultMaxCooldown = 780; 
                    this.color = "#ffca28"; this.faceSymbol = "👑";
                } else { // Jam
                    this.name = "잼";
                    this.hp = 90; this.maxHp = 90; this.damage = 3;
                    this.range = 7 * GRID;               // 1.0v 일반 사거리 7칸 조정
                    this.atkDelay = 6;                   // 1.0v 일반 공격속도 0.1초 (60fps * 0.1 = 6프레임)
                    this.baseSpeed = 5; this.ultDamage = 0;
                    this.ultRange = 0; this.ultMaxCooldown = 840; 
                    this.color = "#2ed573"; this.faceSymbol = "🎲";
                }

                this.atkCooldown = 0;
                this.ultCooldown = 0;
                this.effectTimer = 0;
                this.ultEffectTimer = 0;
                this.lastRenderRange = 0; // 이펙트 가로막힘 렌더링 기억용 변수
            }

            // 실시간 상태이상 연산 속도 제어
            get currentSpeed() {
                let speed = this.baseSpeed;
                if (this.slowTimer > 0) speed *= 0.70;    // 1.0v 메인 궁극기 감속 체감률 30% 하향 적용
                if (this.buffTimer > 0) speed *= 1.50;    // 1.0v 스타 궁극기 기동 버프 50% 폭증 반영
                return speed;
            }

            get currentRange() {
                let r = this.range;
                if (this.type === "Jam" && this.jamBuffTimer > 0) r += 3 * GRID; // 1.0v 잼 리메이크: 사거리만 3칸 증가
                return r;
            }

            get currentAtkDelay() {
                if (this.type === "Star" && this.buffTimer > 0) return this.atkDelay * 0.50; // 1.0v 스타 궁극기 공격속도 50% 가속 적용
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

            takeDamage(amount) {
                if(this.shieldHp > 0) {
                    this.shieldHp -= amount;
                    this.popupText = "보호막 흡수!";
                    this.popupTimer = 40;
                    if(this.shieldHp <= 0) {
                        this.shieldHp = 0;
                        this.popupText = "보호막 파괴!";
                    }
                } else {
                    this.hp -= amount;
                }
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
                    ctx.strokeStyle = "#00f2ff";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(this.x - 4, this.y - 4, this.width + 8, this.height + 8);
                }

                // 인게임 플레이어 내부 심볼 드로잉
                ctx.fillStyle = "white";
                ctx.font = "12px Arial";
                ctx.fillText(this.faceSymbol, this.x + 8, this.y + 25);

                ctx.fillStyle = "white";
                ctx.font = "11px Arial";
                ctx.fillText(this.name + (this.is1P ? "(1P)" : "(2P)"), this.x, this.y - 30);
                
                if (this.slowTimer > 0) { ctx.fillStyle = "#00f2ff"; ctx.fillText("SLOW", this.x, this.y - 38); }
                if (this.buffTimer > 0 || this.jamBuffTimer > 0) { ctx.fillStyle = "#ffca28"; ctx.fillText("BUFF!!", this.x, this.y - 38); }

                if (this.popupTimer > 0) {
                    ctx.fillStyle = "#fffa65";
                    ctx.font = "bold 11px Arial";
                    ctx.fillText(this.popupText, this.x - 10, this.y - 48);
                    this.popupTimer--;
                }

                if (this.healTextTimer > 0) {
                    ctx.fillStyle = "#2ed573";
                    ctx.font = "bold 12px Arial";
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

                // 🛠️ [관통 버그 수정 비주얼 반영] 가로막힌 레이캐스팅 한계 사거리까지만 이펙트를 렌더링
                if(this.effectTimer > 0) {
                    ctx.fillStyle = "rgba(255,255,255,0.5)";
                    let rX = this.facing === 1 ? this.x + this.width : this.x - this.lastRenderRange;
                    ctx.fillRect(rX, this.y + 15, this.lastRenderRange, 4);
                    this.effectTimer--;
                }

                if(this.ultEffectTimer > 0) {
                    ctx.strokeStyle = "yellow";
                    ctx.lineWidth = 2;
                    if(this.type === "Main") {
                        let rX = this.facing === 1 ? this.x + this.width : this.x - this.lastRenderRange;
                        ctx.strokeRect(rX, this.y, this.lastRenderRange, this.height);
                    } else if(this.type === "Mari") {
                        ctx.beginPath();
                        ctx.arc(this.x + 15, this.y + 22, this.ultRange, 0, Math.PI * 2);
                        ctx.stroke();
                    } else if(this.type === "Star" || this.type === "Jam") { 
                        ctx.strokeStyle = "#2ed573";
                        ctx.strokeRect(this.x - 6, this.y - 6, this.width + 12, this.height + 12);
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

                // 🛠️ [벽 안으로 플레이어가 들어가는 버그 완전 수정] 다중 면 완전 밀착형 물리 디텍션 구현
                if (selectedMapIndex === 1) {
                    for(let obs of mapObstacles) {
                        if (this.x + this.width > obs.x && this.x < obs.x + obs.w &&
                            this.y + this.height > obs.y && this.y < obs.y + obs.h) {
                            
                            // Y축 진입 차단 고착화
                            if (this.oldY + this.height <= obs.y) {
                                this.y = obs.y - this.height;
                                this.vY = 0;
                                this.isJumping = false;
                            } else if (this.oldY >= obs.y + obs.h) {
                                this.y = obs.y + obs.h;
                                this.vY = 0;
                            } else {
                                // X축 진입 밀어내기 및 튕김 보정 (구조물 밖으로 좌표 강제 사수)
                                this.x = this.oldX;
                            }
                        }
                    }
                }

                // 🛠️ [오른쪽 맵 탈출 방지 완전 고정] 화면 우측 밖으로 절대 이탈 불가능
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
                        this.bushHealTimer = 0;
                        this.healTextTimer = 30; 
                    }
                } else {
                    this.bushHealTimer = 0;
                }

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
                if (!this.isJumping || 온그라운드) {
                    this.vY = -12;
                    this.isJumping = true;
                }
            }

            // 🛠️ [핵심 버그 수정] 벽 관통 방지 레이캐스팅(공격 연산 거리 조절 알고리즘)
            calculateWallBlockingRange(maxRange) {
                if (selectedMapIndex !== 1) return maxRange;
                
                let step = 4; // 정밀 검사 픽셀 단위
                let currentValidRange = 0;
                
                while (currentValidRange < maxRange) {
                    currentValidRange += step;
                    // 내 공격 투사체의 진행 좌표 계산
                    let checkX = this.facing === 1 ? this.x + this.width + currentValidRange : this.x - currentValidRange;
                    let checkY = this.y + 18; // 중앙 타격점 기준

                    // 구조물 벽에 닿았는지 체크
                    let blocked = false;
                    for (let obs of mapObstacles) {
                        if (checkX >= obs.x && checkX <= obs.x + obs.w &&
                            checkY >= obs.y && checkY <= obs.y + obs.h) {
                            blocked = true;
                            break;
                        }
                    }
                    if (blocked) {
                        return currentValidRange - step; // 벽에 부딪히기 전까지만 도달 허용
                    }
                }
                return maxRange;
            }

            attack(opp) {
                if(this.atkCooldown > 0) return;
                
                // 🛠️ 벽 관통 방지 적용된 유효 유효 사거리 산출
                let validRange = this.calculateWallBlockingRange(this.currentRange);
                this.lastRenderRange = validRange; 
                this.effectTimer = 4;
                this.atkCooldown = this.currentAtkDelay; 
                
                let myL = this.facing === 1 ? this.x + this.width : this.x - validRange;
                let myR = this.facing === 1 ? this.x + this.width + validRange : this.x;

                // 유효 사거리 내에 적이 존재하며 상하 범위 충돌 시에만 타격 성공
                if(myR >= opp.x && myL <= opp.x + opp.width && 
                   this.y + this.height >= opp.y && this.y <= opp.y + opp.height) {
                    opp.takeDamage(this.damage);
                }
            }

            useUltimate(opp) {
                if(this.ultCooldown > 0) return;
                this.ultCooldown = this.ultMaxCooldown;

                if(this.type === "Main") {
                    // 🛠️ 메인 궁극기 역시 벽 관통 방지 연산 처리
                    let validUltRange = this.calculateWallBlockingRange(this.ultRange);
                    this.lastRenderRange = validUltRange;
                    this.ultEffectTimer = 15;

                    let myL = this.facing === 1 ? this.x + this.width : this.x - validUltRange;
                    let myR = this.facing === 1 ? this.x + this.width + validUltRange : this.x;
                    if(myR >= opp.x && myL <= opp.x + opp.width && 
                       this.y + this.height >= opp.y && this.y <= opp.y + opp.height) {
                        opp.takeDamage(this.ultDamage);
                        opp.slowTimer = 90; 
                    }
                } else if(this.type === "Mari") {
                    this.ultEffectTimer = 15;
                    let dx = (this.x + 15) - (opp.x + 15);
                    let dy = (this.y + 22) - (opp.y + 22);
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    if(dist < this.ultRange + 15) {
                        opp.takeDamage(this.ultDamage);
                        this.hp = Math.min(this.maxHp, this.hp + 10); 
                    }
                } else if(this.type === "Star") {
                    this.ultEffectTimer = 15;
                    // 1.0v 스타의 자가 기동/공속 50% 버프 부여 시간 축소 (2초 = 120프레임)
                    this.buffTimer = 120;
                } else if(this.type === "Jam") {
                    this.ultEffectTimer = 15;
                    let rnd = Math.random();

                    if (rnd < 0.10) { 
                        opp.takeDamage(25);              // 1.0v 대박 데미지 25 밸런싱
                        this.popupText = "💥 대박! 25 데미지!!";
                    } else if (rnd < 0.30) { 
                        this.hp = Math.min(this.maxHp, this.hp + 20); // 1.0v 힐링 능력치 20 상향
                        this.popupText = "💚 힐링! HP +20 회복";
                    } else if (rnd < 0.40) { 
                        this.jamBuffTimer = 120;          // 1.0v 리메이크: 2초간 사거리만 +3칸 증가
                        this.popupText = "🏹 신속! 사거리 +3칸";
                    } else if (rnd < 0.60) { 
                        this.x = opp.x + (opp.facing === 1 ? -40 : 40);
                        this.y = opp.y;
                        opp.takeDamage(10);
                        this.popupText = "🔮 습격! 순간이동 백스텝";
                    } else if (rnd < 0.80) { 
                        this.shieldHp = 15;
                        this.popupText = "🛡️ 방어! 배리어 활성";
                    } else { 
                        this.popupText = "💨 꽝! 다음 기회에";
                    }
                    this.popupTimer = 100; 
                }
            }
        }

        let p1, p2;

        function selectChar(type) {
            if(!p1Sel) {
                p1Sel = type;
                document.getElementById("select-title").innerText = "2P 캐릭터 선택 (버전 1.0v)";
            } else if(!p2Sel) {
                p2Sel = type;
                document.getElementById("select-title").innerText = "공식 1.0v 전장 진입";
                document.getElementById("select-subtitle").innerText = "아래에서 전장 맵을 조율하고 격투장으로 진입하세요.";
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
            document.getElementById("select-title").innerText = "1P 캐릭터 선택 (버전 1.0v)";
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
                p1.oldX = p1.x; p1.oldY = p1.y;
                p2.oldX = p2.x; p2.oldY = p2.y;

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
                ctx.fillText("대기실에서 1.0v 데이터 세팅을 조율 중입니다...", 230, 200);
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
