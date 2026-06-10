import streamlit as st
import streamlit.components.v1 as components

# 페이지 레이아웃 및 스타일 최적화
st.set_page_config(page_title="네온 배틀 v1.15", layout="centered")

st.title("⚔️ 네온 배틀 버전 1.15v 공식 패치")
st.caption("클랩 궁극기 스택 초기화 반영, 마리 긴 생머리 변신 및 전 캐릭터 고화질 안면 눈매 드로잉")

# 인게임 및 픽창 웹 컴포넌트 소스코드
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
        
        /* 🎨 v1.15v 그래픽 엔진: SVG 및 고정밀 CSS 마스크 페이스 칩 */
        .avatar-frame { width: 55px; height: 55px; margin: 0 auto 5px; background: #242436; border-radius: 50%; border: 2px solid #3d3d5c; overflow: hidden; position: relative; }
        
        /* 공통 눈 그래픽 컴포넌트 */
        .eye-left, .eye-right { background: #111; width: 4px; height: 4px; border-radius: 50%; position: absolute; top: 12px; z-index: 5; }
        .eye-left { left: 6px; }
        .eye-right { left: 16px; }
        /* 홍채/동공 반짝임 하이라이트 효과 */
        .eye-left::after, .eye-right::after { content: ''; background: #fff; width: 1.5px; height: 1.5px; border-radius: 50%; position: absolute; top: 0.5px; left: 0.5px; }

        /* [메인] 샤프 정장 + 뚜렷하고 깊이감 있는 눈빛 (선글라스 해제 버전으로 매력 극대화) */
        .hero-main { background: #ffd2a1; width: 30px; height: 32px; border-radius: 50%; position: absolute; bottom: 8px; left: 12px; }
        .main-hair-top { background: #1a1a1a; width: 34px; height: 16px; position: absolute; top: -3px; left: -2px; border-radius: 8px 8px 0 0; }
        .main-suit { background: #1e90ff; width: 40px; height: 15px; position: absolute; bottom: 0; left: -5px; border-radius: 4px 4px 0 0; }

        /* [마리] 🎀 대변신: 트윈테일을 풀고 여성미 넘치는 고품격 '긴 생머리 (Long Straight)' 및 크고 예쁜 눈매 연출 */
        .hero-mari { background: #ffe3ca; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 10px; left: 13px; z-index: 2; }
        /* 양옆으로 차분하게 흘러내리는 긴 생머리 컴포넌트 */
        .mari-long-hair-back { background: #4a2831; width: 34px; height: 38px; position: absolute; top: 12px; left: 10px; border-radius: 4px 4px 12px 12px; z-index: 1; }
        .mari-hair-top { background: #ff527b; width: 32px; height: 16px; position: absolute; top: -4px; left: -2px; border-radius: 8px 8px 0 0; }
        .mari-bangs { background: #ff527b; width: 14px; height: 12px; position: absolute; top: 4px; left: 0px; border-radius: 0 0 5px 0; }
        .mari-ribbon { background: #ff77ff; width: 12px; height: 6px; position: absolute; top: -7px; left: 8px; border-radius: 3px; z-index: 6; box-shadow: 0 1px 2px rgba(0,0,0,0.2); }
        .mari-blush { background: rgba(255,107,129,0.6); width: 4px; height: 2.5px; border-radius: 50%; position: absolute; top: 16px; left: 3px; box-shadow: 14px 0 rgba(255,107,129,0.6); }
        .mari-dress { background: #ff00ff; width: 36px; height: 14px; position: absolute; bottom: -12px; left: -4px; border-radius: 50% 50% 0 0; }
        /* 마리 전용 더 예쁘고 큰 여성용 눈 */
        .mari-eye-l, .mari-eye-r { background: #2f192e; width: 5px; height: 5px; border-radius: 50%; position: absolute; top: 11px; z-index: 5; border-top: 1px solid #111; }
        .mari-eye-l { left: 5px; }
        .mari-eye-r { left: 15px; }
        .mari-eye-l::after, .mari-eye-r::after { content: ''; background: #fff; width: 2px; height: 2px; border-radius: 50%; position: absolute; top: 0.5px; left: 0.5px; }

        /* [스타] 왕관 황실 전사 + 총명한 파란 눈 */
        .hero-star { background: #ffe0bd; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 13px; }
        .star-crown-gold { background: #f1c40f; width: 22px; height: 12px; position: absolute; top: -10px; left: 3px; clip-path: polygon(0 100%, 0 20%, 30% 60%, 50% 0, 70% 60%, 100% 20%, 100% 100%); z-index: 6; }
        .star-hair-blonde { background: #fecc5c; width: 32px; height: 14px; position: absolute; top: -2px; left: -2px; border-radius: 6px 6px 0 0; }
        
        /* [잼] 모자 소년 + 장난기 가득한 눈 */
        .hero-jam { background: #ffd2a1; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 13px; }
        .jam-green-cap { background: #2ed573; width: 32px; height: 12px; position: absolute; top: -4px; left: -2px; border-radius: 4px 4px 0 0; transform: rotate(-4deg); z-index: 6; }
        .jam-cap-visor { background: #1b944c; width: 14px; height: 4px; position: absolute; top: 4px; left: 20px; border-radius: 2px; }

        /* [클랩] 헤드셋 박수 아티스트 + 열정적인 눈빛 */
        .hero-clap { background: #fcd1a1; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 13px; }
        .clap-hair { background: #eccc68; width: 32px; height: 14px; position: absolute; top: -3px; left: -2px; border-radius: 6px 6px 0 0; }
        .clap-headphone-l { background: #ff4757; width: 6px; height: 14px; position: absolute; top: 6px; left: -4px; border-radius: 3px; z-index: 6; }
        .clap-headphone-r { background: #ff4757; width: 6px; height: 14px; position: absolute; top: 6px; left: 26px; border-radius: 3px; z-index: 6; }
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
            <h3 id="select-title" style="color:#00f2ff; margin: 0 0 2px 0; font-size: 15px;">1P 영웅 낙점 (v1.15v)</h3>
            <p id="select-subtitle" style="font-size:11px; color:#aaa; margin:0 0 6px 0;">클랩 궁극기 스택 초기화 반영 및 미형 외형 패치</p>
            
            <div class="char-container">
                <div class="char-card" onclick="selectChar('Main')">
                    <div class="avatar-frame">
                        <div class="hero-main">
                            <div class="main-hair-top"></div>
                            <div class="eye-left"></div><div class="eye-right"></div>
                            <div class="main-suit"></div>
                        </div>
                    </div>
                    <strong style="color:#6dd5fa; font-size:11px;">메인</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:2px; line-height:11px;">공속 0.3s | 공격 7<br>궁 11s (30%감속)</div>
                </div>
                <div class="char-card" onclick="selectChar('Mari')">
                    <div class="mari-long-hair-back"></div>
                    <div class="avatar-frame" style="background:#3a2936; border-color:#5c3d52;">
                        <div class="hero-mari">
                            <div class="mari-hair-top"></div>
                            <div class="mari-bangs"></div>
                            <div class="mari-ribbon"></div>
                            <div class="mari-eye-l"></div><div class="mari-eye-r"></div>
                            <div class="mari-blush"></div>
                            <div class="mari-dress"></div>
                        </div>
                    </div>
                    <strong style="color:#ff77ff; font-size:11px;">마리👩‍🦰</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:2px; line-height:11px;">공속 1.25s | 사거리 15<br>이속 -5% | 공격 9</div>
                </div>
                <div class="char-card" onclick="selectChar('Star')">
                    <div class="avatar-frame">
                        <div class="hero-star">
                            <div class="star-hair-blonde"></div>
                            <div class="star-crown-gold"></div>
                            <div class="eye-left" style="background:#1e90ff;"></div><div class="eye-right" style="background:#1e90ff;"></div>
                        </div>
                    </div>
                    <strong style="color:#ffca28; font-size:11px;">스타</strong>
                    <div style="font-size:9px; color:#ccc; margin-top:2px; line-height:11px;">체력 125 | 공격 6<br>궁: 2초간 속도 +50%</div>
                </div>
                <div class="char-card" onclick="selectChar('Jam')">
                    <div class="avatar-frame">
                        <div class="hero-jam">
                            <div class="jam-green-cap"><div class="jam-cap-visor"></div></div>
                            <div class="eye-left"></div><div class="eye-right"></div>
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
                            <div class="eye-left"></div><div class="eye-right"></div>
                            <div class="clap-cloth"></div>
                        </div>
                    </div>
                    <strong style="color:#ffa502; font-size:11px;">클랩🆕</strong>
                    <div style="font-size:9px; color:#f1f1f1; margin-top:2px; line-height:11px;">체력 110 | 공속 0.5s<br>궁극기 시전 시 스택0</div>
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
                
                this.clapStacks = 0; 

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
                } else { 
                    this.name = "클랩"; this.hp = 110; this.maxHp = 110; this.damage = 1;
                    this.range = 10 * GRID; this.atkDelay = 30; 
                    this.baseSpeed = 4.0; this.ultDamage = 0; 
                    this.ultRange = 6 * GRID; this.ultMaxCooldown = 780; 
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

                // 인게임 눈 그리기 (눈동자 픽셀 드로잉 추가로 디테일 상승)
                ctx.fillStyle = "#000";
                if(this.facing === 1) {
                    ctx.fillRect(this.x + 16, this.y + 10, 2, 2);
                } else {
                    ctx.fillRect(this.x + 7, this.y + 10, 2, 2);
                }

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

                ctx.fillStyle = "#333"; ctx.fillRect(this.x, this.y - 16, 25, 3);
                ctx.fillStyle = this.hp < (this.maxHp * 0.3) ? "red" : "lime";
                ctx.fillRect(this.x, this.y - 16, (this.hp / this.maxHp) * 25, 3);

                // 상시 노출 노란색 궁극기 게이지 바
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
                    // 🛠️ [클랩 패치 변경점] 궁극기 시전 즉시 기존 스택 정보 기반 타격 연산 후 0개로 리셋!
                    this.ultEffectTimer = 15;
                    
                    let targetInUltRange = false;
                    let dx = opp.x - this.x;
                    let dy = opp.y - this.y;
                    let distance = Math.sqrt(dx*dx + dy*dy);

                    if(distance <= this.ultRange) {
                        let correctDirection = (this.facing === 1 && dx >= -10) || (this.facing === -1 && dx <= 10);
                        let isAboveOrFront = (dy <= 15) && correctDirection;
                        if(isAboveOrFront) targetInUltRange = true;
                    }

                    let finalClapDamage = this.clapStacks * 2;
                    
                    // 🛠️ 궁극기 사용했으므로 스택 초기화 (0개로 초기화)
                    this.clapStacks = 0;

                    if(targetInUltRange) {
                        opp.takeDamage(finalClapDamage);
                        // 궁극기 맞출 시 보너스로 박수 2스택이 추가로 쌓임
                        this.clapStacks = 2;
                        this.popupText = `👏 클랩 스매시! ${finalClapDamage}딜 (스택 초기화)`;
                    } else {
                        this.popupText = "공중 헛손질 👏 (스택 초기화)";
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
                p1Sel = type; document.getElementById("select-title").innerText = "2P 영웅 낙점 (v1.15v)";
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
            document.getElementById("select-title").innerText = "1P 영웅 낙점 (v1.15v)";
            document.getElementById("select-subtitle").innerText = "클랩 궁극기 스택 초기화 반영 및 미형 외형 패치";
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
                ctx.fillText("전장 데이터를 로드하고 있습니다...", 245, 160);
            } else { p1.draw(); p2.draw(); }
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
</body>
</html>
"""

components.html(game_html, height=485)
