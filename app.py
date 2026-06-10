import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="스트림릿 네온 배틀: 1.1v", layout="centered")

st.title("⚔️ 네온 배틀 버전 1.1v 공식 업데이트")
st.caption("신캐 '클랩' 참전! 선택 창 비주얼 전면 개편 및 궁극기 게이지 가시성 확보 완료.")

# 게임 소스코드 (HTML/JS/CSS)
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; background-color: #121214; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 5px; overflow: hidden; user-select: none; }
        .game-wrapper { position: relative; width: 680px; margin: 0 auto; }
        canvas { background: #050508; border: 3px solid #33333f; display: block; margin: 5px auto; box-shadow: 0 0 15px rgba(0,255,255,0.15); }
        
        .ui-overlay { position: absolute; top: 48%; left: 50%; transform: translate(-50%, -50%); background: rgba(8, 8, 12, 0.98); 
                     padding: 12px; border: 2px solid #00f2ff; border-radius: 12px; width: 590px; z-index: 10; box-shadow: 0 0 30px rgba(0,0,0,0.95); }
        
        .char-container { display: flex; justify-content: center; gap: 6px; margin: 8px 0; }
        .char-card { background: #1a1a26; border: 2px solid #2d2d3d; border-radius: 10px; padding: 6px; width: 105px; cursor: pointer; transition: 0.2s; text-align: center; }
        .char-card:hover { transform: scale(1.03); border-color: #00f2ff; background: #222235; }
        
        /* 🎨 1.1v 고화질 인물 일러스트 박스 (SVG 레이어 공정) */
        .avatar-frame { width: 55px; height: 55px; margin: 0 auto 5px; background: #242436; border-radius: 50%; border: 2px solid #3d3d5c; overflow: hidden; position: relative; }
        
        /* [메인] 샤프한 비즈니스 컷 + 블랙 보잉 선글라스 코디 */
        .hero-main { background: #ffd2a1; width: 30px; height: 32px; border-radius: 50%; position: absolute; bottom: 8px; left: 12px; }
        .main-hair-top { background: #1a1a1a; width: 34px; height: 16px; position: absolute; top: -3px; left: -2px; border-radius: 8px 8px 0 0; }
        .main-sunglass { background: #111; width: 26px; height: 7px; position: absolute; top: 11px; left: 2px; border-radius: 2px; box-shadow: 0 1px 3px rgba(0,0,0,0.5); }
        .main-suit { background: #1e90ff; width: 40px; height: 15px; position: absolute; bottom: 0; left: -5px; border-radius: 4px 4px 0 0; }

        /* [마리] 고 퀄리티 여성 일러스트: 페미닌 사이드 뱅 + 로즈 핑크 트윈 블렌딩 + 고급 실크 리본 */
        .hero-mari { background: #ffe3ca; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 10px; left: 13px; }
        .mari-hair-main { background: #ff527b; width: 34px; height: 18px; position: absolute; top: -4px; left: -3px; border-radius: 10px 10px 0 0; }
        .mari-bangs { background: #ff527b; width: 12px; height: 14px; position: absolute; top: 6px; left: -1px; border-radius: 0 0 6px 0; transform: rotate(15deg); }
        .mari-ribbon-l { background: #ff77ff; width: 10px; height: 10px; border-radius: 50%; position: absolute; top: 4px; left: -7px; border: 1px solid #fff; }
        .mari-ribbon-r { background: #ff77ff; width: 10px; height: 10px; border-radius: 50%; position: absolute; top: 4px; left: 25px; border: 1px solid #fff; }
        .mari-blush { background: rgba(255,107,129,0.5); width: 5px; height: 3px; border-radius: 50%; position: absolute; top: 15px; left: 3px; box-shadow: 15px 0 rgba(255,107,129,0.5); }
        .mari-dress { background: #ff00ff; width: 36px; height: 14px; position: absolute; bottom: -12px; left: -4px; border-radius: 50% 50% 0 0; }

        /* [스타] 왕관 황실 전사 */
        .hero-star { background: #ffe0bd; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 13px; }
        .star-crown-gold { background: #f1c40f; width: 22px; height: 12px; position: absolute; top: -10px; left: 3px; clip-path: polygon(0 100%, 0 20%, 30% 60%, 50% 0, 70% 60%, 100% 20%, 100% 100%); }
        .star-hair-blonde { background: #fecc5c; width: 32px; height: 14px; position: absolute; top: -2px; left: -2px; border-radius: 6px 6px 0 0; }
        
        /* [잼] 모자 쓴 후디 소년 */
        .hero-jam { background: #ffd2a1; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 13px; }
        .jam-green-cap { background: #2ed573; width: 32px; height: 12px; position: absolute; top: -4px; left: -2px; border-radius: 4px 4px 0 0; transform: rotate(-5deg); }
        .jam-cap-visor { background: #1b944c; width: 14px; height: 4px; position: absolute; top: 4px; left: 20px; border-radius: 2px; }

        /* [클랩] 1.1v 신캐: 힙합 헤드셋을 장착하고 박수칠 준비가 완료된 박수 아티스트 */
        .hero-clap { background: #fcd1a1; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 13px; }
        .clap-hair { background: #eccc68; width: 32px; height: 14px; position: absolute; top: -3px; left: -2px; border-radius: 6px 6px 0 0; }
        .clap-headphone-l { background: #ff4757; width: 6px; height: 14px; position: absolute; top: 6px; left: -4px; border-radius: 3px; }
        .clap-headphone-r { background: #ff4757; width: 6px; height: 14px; position: absolute; top: 6px; left: 26px; border-radius: 3px; }
        .clap-cloth { background: #ffa502; width: 36px; height: 12px; position: absolute; bottom: -10px; left: -4px; border-radius: 3px; }

        .map-container { display: flex; justify-content: center; gap: 10px; margin: 5px 0; }
        .map-btn { padding: 6px 14px; font-size: 11px; cursor: pointer; border: 2px solid #555; background: #333; color: white; font-weight: bold; border-radius: 6px; }
        .map-btn.selected { border-color: #2ed573; background: #1e4620; }
        
        .start-action-btn { background: #2ed573; color: white; padding: 10px 30px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px; margin-top: 4px; }
        .restart-btn { background: #2ed573; color: white; padding: 6px 14px; border: none; border-radius: 4px; cursor: pointer; margin-top: 8px; }
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
            <h3 id="select-title" style="color:#00f2ff; margin: 0 0 2px 0; font-size: 15px;">1P 영웅 낙점 (v1.1v)</h3>
            <p id="select-subtitle" style="font-size:11px; color:#aaa; margin:0 0 6px 0;">캐릭터 외형 퀄리티 고도화 패치 완료</p>
            
            <div class="char-container">
                <div class="char-card" onclick="selectChar('Main')">
                    <div class="avatar-frame">
                        <div class="hero-main">
                            <div class="main-hair-top"></div>
                            <div class="main-sunglass"></div>
                            <div class="main-suit"></div>
                        </div>
                    </div>
                    <strong style="color:#6dd5fa; font-size:11px;">메인</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:2px; line-height:11px;">공속 0.3s | 공격 7<br>궁 11s (30%감속)</div>
                </div>
                <div class="char-card" onclick="selectChar('Mari')">
                    <div class="avatar-frame" style="background:#3a2936; border-color:#5c3d52;">
                        <div class="hero-mari">
                            <div class="mari-hair-main"></div>
                            <div class="mari-bangs"></div>
                            <div class="mari-ribbon-l"></div>
                            <div class="mari-ribbon-r"></div>
                            <div class="mari-blush"></div>
                            <div class="mari-dress"></div>
                        </div>
                    </div>
                    <strong style="color:#ff77ff; font-size:11px;">마리</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:2px; line-height:11px;">공속 1.25s | 사거리 15<br>이속 -5% | 공격 9</div>
                </div>
                <div class="char-card" onclick="selectChar('Star')">
                    <div class="avatar-frame">
                        <div class="hero-star">
                            <div class="star-hair-blonde"></div>
                            <div class="star-crown-gold"></div>
                        </div>
                    </div>
                    <strong style="color:#ffca28; font-size:11px;">스타</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:2px; line-height:11px;">체력 125 | 공격 6<br>궁: 2초간 속도 +50%</div>
                </div>
                <div class="char-card" onclick="selectChar('Jam')">
                    <div class="avatar-frame">
                        <div class="hero-jam">
                            <div class="jam-green-cap"><div class="jam-cap-visor"></div></div>
                        </div>
                    </div>
                    <strong style="color:#2ed573; font-size:11px;">잼</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:2px; line-height:11px;">공속 0.1s | 사거리 7<br>궁: 대박25딜/20힐</div>
                </div>
                <div class="char-card" onclick="selectChar('Clap')">
                    <div class="avatar-frame" style="background:#362f24; border-color:#5c4e3d;">
                        <div class="hero-clap">
                            <div class="clap-hair"></div>
                            <div class="clap-headphone-l"></div>
                            <div class="clap-headphone-r"></div>
                            <div class="clap-cloth"></div>
                        </div>
                    </div>
                    <strong style="color:#ffa502; font-size:11px;">클랩🆕</strong>
                    <div style="font-size:9px; color:#f1f1f1; margin-top:2px; line-height:11px;">체력 110 | 공속 0.5s<br>스택형 폭발 궁극기</div>
                </div>
            </div>

            <div class="map-container">
                <button id="map0-btn" class="map-btn selected" onclick="selectMap(0)">평지 아레나</button>
                <button id="map1-btn" class="map-btn" onclick="selectMap(1)">네온 미로 (버그 픽스 완료)</button>
            </div>

            <button id="start-game-btn" class="start-action-btn hidden" onclick="confirmStart()">전장 진입하기</button>
        </div>

        <div id="result-screen" class="ui-overlay hidden">
            <h2 id="winner-text" style="font-size: 22px; margin: 0;"></h2>
            <button class="restart-btn" onclick="resetGame()">다시하기 (Restart)</button>
        </div>

        <canvas id="gameCanvas" width="660" height="330"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        
        const GRID = 16; 
        const GRAVITY = 0.55;
        
        let gameState = "SELECT";
        let p1Sel = null, p2Sel = null;
        let selectedMapIndex = 0;

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
                this.width = 25; this.height = 38; 
                this.vY = 0;
                this.facing = is1P ? 1 : -1;
                this.isJumping = false;
                
                this.slowTimer = 0; this.buffTimer = 0; this.inBush = false;     
                this.bushHealTimer = 0; this.popupText = ""; this.popupTimer = 0; 
                this.jamBuffTimer = 0; this.shieldHp = 0;       
                
                // 🛠️ 신규 스탯 및 오리지널 리밸런싱 데이터 정의
                this.clapStacks = 0; // 클랩 전용 박수 스택 변수

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
                } else if(type === "Jam") { 
                    this.name = "잼"; this.hp = 90; this.maxHp = 90; this.damage = 3;
                    this.range = 7 * GRID; this.atkDelay = 6; this.baseSpeed = 3.9; 
                    this.ultDamage = 0; this.ultRange = 0; this.ultMaxCooldown = 840; 
                    this.color = "#2ed573"; this.faceSymbol = "🎲";
                } else { // 🛠️ 신규 영웅 클랩 스탯 세팅 완료
                    this.name = "클랩"; this.hp = 110; this.maxHp = 110; this.damage = 1;
                    this.range = 10 * GRID; this.atkDelay = 30; // 0.5초 = 30프레임
                    this.baseSpeed = 4.0; this.ultDamage = 0; // 스택 비례 연산 유동 적용
                    this.ultRange = 6 * GRID; this.ultMaxCooldown = 780; // 13초 = 780프레임
                    this.color = "#ffa502"; this.faceSymbol = "🎧";
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

                // 상단 스태이터스 텍스트 정보 표기 (박수 스택 포함)
                ctx.fillStyle = "white"; ctx.font = "9px Arial";
                let nameLabel = this.name + (this.is1P ? "(1P)" : "(2P)");
                if(this.type === "Clap") nameLabel += ` [${this.clapStacks}👏]`;
                ctx.fillText(nameLabel, this.x - 5, this.y - 25);
                
                if (this.slowTimer > 0) { ctx.fillStyle = "#00f2ff"; ctx.fillText("SLOW", this.x, this.y - 32); }

                if (this.popupTimer > 0) {
                    ctx.fillStyle = "#fffa65"; ctx.font = "bold 9px Arial";
                    ctx.fillText(this.popupText, this.x - 12, this.y - 38);
                    this.popupTimer--;
                }

                // 체력바 유닛 레이아웃
                ctx.fillStyle = "#333"; ctx.fillRect(this.x, this.y - 16, 25, 3);
                ctx.fillStyle = this.hp < (this.maxHp * 0.3) ? "red" : "lime";
                ctx.fillRect(this.x, this.y - 16, (this.hp / this.maxHp) * 25, 3);

                // 🛠️ [요청] 궁극기 쿨타임/충전 게이지 노란색 바를 상시 뚜렷하게 노출
                ctx.fillStyle = "rgba(40,40,40,0.8)"; ctx.fillRect(this.x, this.y - 11, 25, 2.5);
                ctx.fillStyle = "yellow";
                let ultPercent = 1 - (this.ultCooldown / this.ultMaxCooldown);
                ctx.fillRect(this.x, this.y - 11, Math.max(0, ultPercent) * 25, 2.5);

                if(this.effectTimer > 0) {
                    ctx.fillStyle = this.type === "Clap" ? "rgba(255, 165, 2, 0.6)" : "rgba(255,255,255,0.5)";
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
                    } else if(this.type === "Clap") {
                        // 클랩의 위쪽과 앞방향 전방 범위를 나타내는 감각적인 반호 펄스 드로잉
                        ctx.fillStyle = "rgba(255, 165, 2, 0.25)";
                        ctx.beginPath();
                        if(this.facing === 1) {
                            ctx.arc(this.x + this.width, this.y, this.ultRange, -Math.PI/2, Math.PI/4);
                        } else {
                            ctx.arc(this.x, this.y, this.ultRange, Math.PI * 0.75, Math.PI * 1.5);
                        }
                        ctx.lineTo(this.x + 12, this.y);
                        ctx.fill();
                    } else if(this.type === "Star" || this.type === "Jam") { 
                        ctx.strokeStyle = "#2ed573"; ctx.strokeRect(this.x - 4, this.y - 4, this.width + 8, this.height + 8);
                    }
                    this.ultEffectTimer--;
                }
                ctx.restore();
            }

            update() {
                this.oldX = this.x; this.oldY = this.y;
                this.vY += GRAVITY; this.y += this.vY;
                
                if (this.y >= canvas.height - this.height - 15) {
                    this.y = canvas.height - this.height - 15;
                    this.vY = 0; this.isJumping = false;
                }

                // 벽 관통 차단/끼임 무효화 물리 엔진 가동
                if (selectedMapIndex === 1) {
                    for(let obs of mapObstacles) {
                        if (this.x + this.width > obs.x && this.x < obs.x + obs.w &&
                            this.y + this.height > obs.y && this.y < obs.y + obs.h) {
                            if (this.oldY + this.height <= obs.y) {
                                this.y = obs.y - this.height; this.vY = 0; this.isJumping = false;
                            } else if (this.oldY >= obs.y + obs.h) {
                                this.y = obs.y + obs.h; this.vY = 0;
                            } else {
                                this.x = this.oldX;
                            }
                        }
                    }
                }

                if (this.x < 0) this.x = 0;
                if (this.x > canvas.width - this.width) this.x = canvas.width - this.width;
                
                this.checkBushIntersection();

                let cooldownSpeed = this.inBush ? 1.15 : 1.0;
                if(this.atkCooldown > 0) this.atkCooldown = Math.max(0, this.atkCooldown - cooldownSpeed);
                if(this.ultCooldown > 0) this.ultCooldown = Math.max(0, this.ultCooldown - cooldownSpeed);
                
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

                // 🛠️ 클랩 일반공격 시 박수 스택 축적 판정 메커니즘 (최대 20스택 상한)
                if(this.type === "Clap") {
                    if(this.clapStacks < 20) this.clapStacks++;
                }

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
                } else if(this.type === "Clap") {
                    // 🛠️ [클랩 궁극기] 박수 스택 * 2 만큼의 데미지를 위와 전방 6칸 구역 적에게 투사
                    this.ultEffectTimer = 15;
                    
                    let targetInUltRange = false;
                    let dx = opp.x - this.x;
                    let dy = opp.y - this.y;
                    let distance = Math.sqrt(dx*dx + dy*dy);

                    if(distance <= this.ultRange) {
                        // 전방 방향성 및 위쪽(dy <= 10) 고도 환경 다중 분석 체킹
                        let correctDirection = (this.facing === 1 && dx >= -10) || (this.facing === -1 && dx <= 10);
                        let isAboveOrFront = (dy <= 15) && correctDirection;
                        if(isAboveOrFront) targetInUltRange = true;
                    }

                    if(targetInUltRange) {
                        let finalClapDamage = this.clapStacks * 2;
                        opp.takeDamage(finalClapDamage);
                        // 적 명중 시 박수 스택 2 증가 보너스 부여 (상한 20개 내)
                        if(this.clapStacks < 20) this.clapStacks = Math.min(20, this.clapStacks + 2);
                        this.popupText = `👏 클랩 스매시! ${finalClapDamage}딜`;
                    } else {
                        this.popupText = "공중 헛손질 👏";
                    }
                    this.popupTimer = 60;

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
                p1Sel = type; document.getElementById("select-title").innerText = "2P 영웅 낙점 (v1.1v)";
            } else if(!p2Sel) {
                p2Sel = type;
                document.getElementById("select-title").innerText = "전투 시스템 매칭 완료";
                document.getElementById("select-subtitle").innerText = "아래 진입하기 버튼을 클릭하여 전투를 시작하세요.";
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
            document.getElementById("select-title").innerText = "1P 영웅 낙점 (v1.1v)";
            document.getElementById("select-subtitle").innerText = "캐릭터 외형 퀄리티 고도화 패치 완료";
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
                ctx.fillStyle = "#3a3a45"; 
                for(let obs of mapObstacles) { ctx.fillRect(obs.x, obs.y, obs.w, obs.h); }
            }

            ctx.fillStyle = "#22222a"; ctx.fillRect(0, canvas.height - 15, canvas.width, 15);

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
                ctx.fillStyle = "#15151c"; ctx.font = "12px Arial";
                ctx.fillText("픽창에서 전략 지표를 구성하는 중...", 245, 160);
            } else { p1.draw(); p2.draw(); }
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
</body>
</html>
"""

components.html(game_html, height=485)
