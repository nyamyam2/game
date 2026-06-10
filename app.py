import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="네온 배틀 v1.30", layout="centered")

st.title("⚔️ 네온 배틀 버전 1.30v 공식 패치")
st.caption("✨ 신규 '코롱(패시브)' 특성 시스템 전격 도입! 나만의 맞춤형 전략 세팅")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; background-color: #121214; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 5px; overflow: hidden; user-select: none; }
        .game-wrapper { position: relative; width: 680px; margin: 0 auto; }
        canvas { background: #050508; border: 3px solid #33333f; display: block; margin: 5px auto; box-shadow: 0 0 15px rgba(0,255,255,0.15); }
        
        .ui-overlay { position: absolute; top: 48%; left: 50%; transform: translate(-50%, -50%); background: rgba(8, 8, 12, 0.98); 
                     padding: 12px; border: 2px solid #00f2ff; border-radius: 12px; width: 610px; z-index: 10; box-shadow: 0 0 30px rgba(0,0,0,0.95); }
        
        .char-container { display: flex; justify-content: center; gap: 6px; margin: 8px 0; }
        .char-card { background: #1a1a26; border: 2px solid #2d2d3d; border-radius: 10px; padding: 6px; width: 92px; cursor: pointer; transition: 0.2s; text-align: center; }
        .char-card.selected-p1 { border-color: #00f2ff; background: #182a3c; }
        .char-card.selected-p2 { border-color: #ff4757; background: #3c1820; }
        
        /* 코롱 선택기 스타일 */
        .cologne-container { display: flex; justify-content: center; gap: 15px; margin: 12px 0; background: #161622; padding: 10px; border-radius: 8px; border: 1px dashed #444; }
        .cologne-btn { background: #2b2b3d; color: #fff; border: 2px solid #444; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 11px; width: 45%; text-align: left; }
        .cologne-btn:hover { border-color: #00f2ff; background: #35354e; }
        .cologne-btn.active { background: #00f2ff; color: #000; font-weight: bold; border-color: #fff; }
        
        /* 🎨 아바타 그래픽 엔진 */
        .avatar-frame { width: 45px; height: 45px; margin: 0 auto 5px; background: #242436; border-radius: 50%; border: 2px solid #3d3d5c; overflow: hidden; position: relative; }
        .eye-left, .eye-right { background: #111; width: 4px; height: 4px; border-radius: 50%; position: absolute; top: 12px; z-index: 5; }
        .eye-left { left: 6px; } .eye-right { left: 16px; }
        .eye-left::after, .eye-right::after { content: ''; background: #fff; width: 1.5px; height: 1.5px; border-radius: 50%; position: absolute; top: 0.5px; left: 0.5px; }

        .hero-main { background: #ffd2a1; width: 30px; height: 32px; border-radius: 50%; position: absolute; bottom: 8px; left: 8px; }
        .main-hair-top { background: #1a1a1a; width: 34px; height: 16px; position: absolute; top: -3px; left: -2px; border-radius: 8px 8px 0 0; }
        .main-suit { background: #1e90ff; width: 40px; height: 15px; position: absolute; bottom: 0; left: -5px; border-radius: 4px 4px 0 0; }

        .hero-mari { background: #ffe3ca; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 10px; left: 9px; z-index: 2; }
        .mari-long-hair-back { background: #4a2831; width: 34px; height: 38px; position: absolute; top: 12px; left: 6px; border-radius: 4px 4px 12px 12px; z-index: 1; }
        .mari-hair-top { background: #ff527b; width: 32px; height: 16px; position: absolute; top: -4px; left: -2px; border-radius: 8px 8px 0 0; }
        .mari-dress { background: #ff00ff; width: 36px; height: 14px; position: absolute; bottom: -12px; left: -4px; border-radius: 50% 50% 0 0; }

        .hero-star { background: #ffe0bd; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 9px; }
        .star-crown-gold { background: #f1c40f; width: 22px; height: 12px; position: absolute; top: -10px; left: 3px; clip-path: polygon(0 100%, 0 20%, 30% 60%, 50% 0, 70% 60%, 100% 20%, 100% 100%); z-index: 6; }
        .star-hair-blonde { background: #fecc5c; width: 32px; height: 14px; position: absolute; top: -2px; left: -2px; border-radius: 6px 6px 0 0; }
        
        .hero-jam { background: #ffd2a1; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 9px; }
        .jam-green-cap { background: #2ed573; width: 32px; height: 12px; position: absolute; top: -4px; left: -2px; border-radius: 4px 4px 0 0; z-index: 6; }

        .hero-clap { background: #fcd1a1; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 9px; }
        .clap-hair { background: #eccc68; width: 32px; height: 14px; position: absolute; top: -3px; left: -2px; border-radius: 6px 6px 0 0; }
        .clap-headphone-l { background: #ff4757; width: 6px; height: 14px; position: absolute; top: 6px; left: -4px; border-radius: 3px; z-index: 6; }
        .clap-headphone-r { background: #ff4757; width: 6px; height: 14px; position: absolute; top: 6px; left: 26px; border-radius: 3px; z-index: 6; }

        .hero-yuri { background: #fff1e0; width: 28px; height: 30px; border-radius: 50%; position: absolute; bottom: 8px; left: 9px; z-index: 2; }
        .yuri-ponytail { background: #4b382a; width: 14px; height: 26px; position: absolute; top: 4px; left: 22px; border-radius: 0 12px 12px 0; transform: rotate(10deg); z-index: 1; }
        .yuri-hair-top { background: #4b382a; width: 32px; height: 15px; position: absolute; top: -3px; left: -2px; border-radius: 8px 8px 0 0; }
        .yuri-uniform { background: #3b3b4f; width: 36px; height: 12px; position: absolute; bottom: -10px; left: -4px; border-radius: 3px; }

        .map-container { display: flex; justify-content: center; gap: 10px; margin: 5px 0; }
        .map-btn { padding: 5px 12px; font-size: 11px; cursor: pointer; border: 2px solid #555; background: #333; color: white; border-radius: 6px; }
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
            <h3 id="select-title" style="color:#00f2ff; margin: 0 0 2px 0; font-size: 15px;">1P 영웅 낙점 (v1.30v)</h3>
            <p id="select-subtitle" style="font-size:11px; color:#aaa; margin:0 0 6px 0;">영웅을 클릭한 뒤 하단에서 고유 '코롱(패시브)' 특성을 선택하세요.</p>
            
            <div class="char-container">
                <div class="char-card" id="card-Main" onclick="selectChar('Main')">
                    <div class="avatar-frame"><div class="hero-main"><div class="main-hair-top"></div><div class="eye-left"></div><div class="eye-right"></div><div class="main-suit"></div></div></div>
                    <strong style="color:#6dd5fa; font-size:11px;">메인</strong>
                </div>
                <div class="char-card" id="card-Mari" onclick="selectChar('Mari')">
                    <div class="mari-long-hair-back"></div>
                    <div class="avatar-frame" style="background:#3a2936; border-color:#5c3d52;"><div class="hero-mari"><div class="mari-hair-top"></div><div class="eye-left"></div><div class="eye-right"></div><div class="mari-dress"></div></div></div>
                    <strong style="color:#ff77ff; font-size:11px;">마리👩‍🦰</strong>
                </div>
                <div class="char-card" id="card-Star" onclick="selectChar('Star')">
                    <div class="avatar-frame"><div class="hero-star"><div class="star-hair-blonde"></div><div class="star-crown-gold"></div><div class="eye-left"></div><div class="eye-right"></div></div></div>
                    <strong style="color:#ffca28; font-size:11px;">스타</strong>
                </div>
                <div class="char-card" id="card-Jam" onclick="selectChar('Jam')">
                    <div class="avatar-frame"><div class="hero-jam"><div class="jam-green-cap"></div><div class="eye-left"></div><div class="eye-right"></div></div></div>
                    <strong style="color:#2ed573; font-size:11px;">잼</strong>
                </div>
                <div class="char-card" id="card-Clap" onclick="selectChar('Clap')">
                    <div class="avatar-frame" style="background:#362f24; border-color:#5c4e3d;"><div class="hero-clap"><div class="clap-hair"></div><div class="clap-headphone-l"></div><div class="clap-headphone-r"></div><div class="eye-left"></div><div class="eye-right"></div></div></div>
                    <strong style="color:#ffa502; font-size:11px;">클랩</strong>
                </div>
                <div class="char-card" id="card-Yuri" onclick="selectChar('Yuri')">
                    <div class="yuri-ponytail"></div>
                    <div class="avatar-frame" style="background:#3a2d24; border-color:#5c4636;"><div class="hero-yuri"><div class="yuri-hair-top"></div><div class="eye-left" style="background:#ff4757;"></div><div class="eye-right" style="background:#ff4757;"></div><div class="yuri-uniform"></div></div></div>
                    <strong style="color:#ff4757; font-size:11px;">유리💖</strong>
                </div>
            </div>

            <div id="cologne-panel" class="hidden">
                <div style="font-size: 11px; color: #fffa65; margin-bottom: 4px; font-weight: bold;" id="cologne-panel-title">패시브 스킬(코롱) 선택</div>
                <div class="cologne-container">
                    <button id="col-btn-1" class="cologne-btn" onclick="chooseCologne(1)">코롱 1: 불러오는 중...</button>
                    <button id="col-btn-2" class="cologne-btn" onclick="chooseCologne(2)">코롱 2: 불러오는 중...</button>
                </div>
            </div>

            <div class="map-container">
                <button id="map0-btn" class="map-btn selected" onclick="selectMap(0)">평지 아레나</button>
                <button id="map1-btn" class="map-btn" onclick="selectMap(1)">네온 미로 (덤불 완벽 작동)</button>
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
        let p1Cologne = 1, p2Cologne = 1;
        let selectPhase = "P1_CHAR"; // P1_CHAR -> P1_COL -> P2_CHAR -> P2_COL -> READY
        let selectedMapIndex = 0;

        // 코롱 특성 설명 DB 다운로드
        const cologneData = {
            Main: { c1: "코롱1: 최대체력 +15 증가", c2: "코롱2: 궁극기 쿨타임 1초 감소" },
            Mari: { c1: "코롱1: 평타 시 25% 확률로 +3딜", c2: "코롱2: 대기 시 1초당 보호막 +2" },
            Star: { c1: "코롱1: 궁 사용시 적에게 5딜 원격 타격", c2: "코롱2: 일반 공격 데미지 +1" },
            Jam:  { c1: "코롱1: 평타 시 5% 확률로 궁 즉시충전", c2: "코롱2: 꽝 나오면 다음 궁 무조건 대박" },
            Clap: { c1: "코롱1: 스택 * 2%만큼 이동속도 증가", c2: "코롱2: 궁극기 기본 데미지 +5" },
            Yuri: { c1: "코롱1: 평타 적중시 1초간 이속 +15%", c2: "코롱2: 적 매혹 시 초당 체력 4 회복" }
        };

        const mapObstacles = [
            { x: 140, y: 270, w: 45, h: 40 }, { x: 475, y: 270, w: 45, h: 40 }, { x: 260, y: 195, w: 140, h: 20 } 
        ];
        const mapBushes = [
            { x: 40, y: 260, w: 70, h: 50 }, { x: 550, y: 260, w: 70, h: 50 }, { x: 300, y: 145, w: 60, h: 50 }
        ];

        const keys = {};
        window.addEventListener("keydown", (e) => { 
            keys[e.code] = true; 
            if(["Space", "ArrowUp", "ArrowDown"].includes(e.code)) e.preventDefault();
            if(gameState === "PLAY") {
                if(e.code === "KeyF" && p1.charmTimer <= 0) p1.attack(p2);
                if(e.code === "KeyG" && p1.charmTimer <= 0) p1.useUltimate(p2);
                if(e.code === "ArrowDown" && p2.charmTimer <= 0) p2.attack(p1);
                if(e.code === "KeyL" && p2.charmTimer <= 0) p2.useUltimate(p1);
            }
        });
        window.addEventListener("keyup", (e) => { keys[e.code] = false; });

        class Player {
            constructor(x, y, type, is1P, cologneChoice) {
                this.is1P = is1P; this.type = type; this.cologne = cologneChoice;
                this.x = x; this.y = y; this.oldX = x; this.oldY = y;
                this.width = 25; this.height = 38; this.vY = 0;
                this.facing = is1P ? 1 : -1; this.isJumping = false;
                
                this.slowTimer = 0; this.buffTimer = 0; this.inBush = false;     
                this.popupText = ""; this.popupTimer = 0; 
                this.jamBuffTimer = 0; this.shieldHp = 0;       
                
                this.charmTimer = 0; this.dotDamageTimer = 0; this.dotDamageCount = 0;
                this.clapStacks = 0; 

                // 코롱 전용 내부 정밀 파라미터 제어기
                this.mariNoAtkTimer = 0;
                this.jamNextIsJackpot = false;
                this.yuriHitBuffTimer = 0;

                if(type === "Main") {
                    let maxHpBonus = (this.cologne === 1) ? 15 : 0;
                    this.name = "메인"; this.hp = 100 + maxHpBonus; this.maxHp = 100 + maxHpBonus; this.damage = 7;                     
                    this.range = 4 * GRID; this.atkDelay = 18; this.baseSpeed = 4.2; 
                    this.ultDamage = 18; this.ultRange = 8 * GRID; 
                    this.ultMaxCooldown = (this.cologne === 2) ? 600 : 660; // 코롱2 장착 시 궁쿨 1초 감소 (60프레임 감소)
                    this.color = "#1e90ff"; this.faceSymbol = "🕶️";
                } else if(type === "Mari") {
                    this.name = "마리"; this.hp = 90; this.maxHp = 90; this.damage = 9;                     
                    this.range = 15 * GRID; this.atkDelay = 75; this.baseSpeed = 3.6;           
                    this.transparentUltDamage = 20; this.ultRange = 4 * GRID; this.ultMaxCooldown = 720; 
                    this.color = "#ff00ff"; this.faceSymbol = "🎀";
                } else if(type === "Star") { 
                    this.name = "스타"; this.hp = 125; this.maxHp = 125; 
                    this.damage = (this.cologne === 2) ? 7 : 6; // 코롱2 장착 시 평타 데미지 +1 보너스                     
                    this.range = 7 * GRID; this.atkDelay = 42; this.baseSpeed = 3.9; 
                    this.ultDamage = 0; this.ultRange = 0; this.ultMaxCooldown = 780; 
                    this.color = "#ffca28"; this.faceSymbol = "👑";
                } else if(type === "Jam") { 
                    this.name = "잼"; this.hp = 90; this.maxHp = 90; this.damage = 3;
                    this.range = 7 * GRID; this.atkDelay = 6; this.baseSpeed = 3.9; 
                    this.ultDamage = 0; this.ultRange = 0; this.ultMaxCooldown = 840; 
                    this.color = "#2ed573"; this.faceSymbol = "🎲";
                } else if(type === "Clap") { 
                    this.name = "클랩"; this.hp = 110; this.maxHp = 110; this.damage = 1;
                    this.range = 10 * GRID; this.atkDelay = 30; this.baseSpeed = 4.0; 
                    this.ultRange = 6 * GRID; this.ultMaxCooldown = 780; 
                    this.color = "#ffa502"; this.faceSymbol = "🎧";
                } else { 
                    this.name = "유리"; this.hp = 100; this.maxHp = 100; this.damage = 4;
                    this.range = 7 * GRID; this.atkDelay = 18; this.baseSpeed = 4.0; 
                    this.ultRange = 5 * GRID; this.ultMaxCooldown = 900; 
                    this.color = "#ff4757"; this.faceSymbol = "🎓";
                }

                this.atkCooldown = 0; this.ultCooldown = 0;
                this.effectTimer = 0; this.ultEffectTimer = 0; this.lastRenderRange = 0;
            }

            get currentSpeed() {
                if (this.charmTimer > 0) return 2.0; 
                let speed = this.baseSpeed;
                if (this.slowTimer > 0) speed *= 0.70;    
                if (this.buffTimer > 0) speed *= 1.50;    
                
                // [클랩 코롱1] 박수스택당 2% 속도 보너스 연산 조립
                if (this.type === "Clap" && this.cologne === 1) {
                    speed *= (1 + (this.clapStacks * 0.02));
                }
                // [유리 코롱1] 평타 적중시 이속 15% 가속 엔진 활성화
                if (this.type === "Yuri" && this.cologne === 1 && this.yuriHitBuffTimer > 0) {
                    speed *= 1.15;
                }
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
                if (this.charmTimer > 0) ctx.fillStyle = "#ff758c"; 
                else if (this.slowTimer > 0) ctx.fillStyle = "#57606f"; 
                else if (this.buffTimer > 0 || this.jamBuffTimer > 0 || this.yuriHitBuffTimer > 0) ctx.fillStyle = "#fff200"; 
                else ctx.fillStyle = this.color;
                
                ctx.fillRect(this.x, this.y, this.width, this.height);
                ctx.shadowBlur = 0;

                if(this.shieldHp > 0) {
                    ctx.strokeStyle = "#00f2ff"; ctx.lineWidth = 2;
                    ctx.strokeRect(this.x - 3, this.y - 3, this.width + 6, this.height + 6);
                }

                ctx.fillStyle = "white"; ctx.font = "10px Arial";
                ctx.fillText(this.faceSymbol, this.x + 5, this.y + 22);

                ctx.fillStyle = this.charmTimer > 0 ? "red" : "#000";
                if(this.facing === 1) ctx.fillRect(this.x + 16, this.y + 10, 2, 2);
                else ctx.fillRect(this.x + 7, this.y + 10, 2, 2);

                ctx.fillStyle = "white"; ctx.font = "9px Arial";
                let nameLabel = this.name + (this.is1P ? "(1P)" : "(2P)") + ` [C${this.cologne}]`;
                if(this.type === "Clap") nameLabel += ` [${this.clapStacks}👏]`;
                ctx.fillText(nameLabel, this.x - 5, this.y - 25);
                
                if (this.charmTimer > 0) { ctx.fillStyle = "#ff4757"; ctx.fillText("♥매혹♥", this.x - 4, this.y - 32); }
                else if (this.slowTimer > 0) { ctx.fillStyle = "#00f2ff"; ctx.fillText("SLOW", this.x, this.y - 32); }

                if (this.popupTimer > 0) {
                    ctx.fillStyle = "#fffa65"; ctx.font = "bold 9px Arial";
                    ctx.fillText(this.popupText, this.x - 12, this.y - 38);
                    this.popupTimer--;
                }

                ctx.fillStyle = "#333"; ctx.fillRect(this.x, this.y - 16, 25, 3);
                ctx.fillStyle = this.hp < (this.maxHp * 0.3) ? "red" : "lime";
                ctx.fillRect(this.x, this.y - 16, (this.hp / this.maxHp) * 25, 3);

                ctx.fillStyle = "rgba(40,40,40,0.8)"; ctx.fillRect(this.x, this.y - 11, 25, 2.5);
                ctx.fillStyle = "yellow";
                let ultPercent = 1 - (this.ultCooldown / this.ultMaxCooldown);
                ctx.fillRect(this.x, this.y - 11, Math.max(0, ultPercent) * 25, 2.5);

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
                    } else if(this.type === "Mari" || this.type === "Yuri") {
                        ctx.strokeStyle = this.type === "Yuri" ? "#ff4757" : "yellow";
                        ctx.beginPath(); ctx.arc(this.x + 12, this.y + 19, this.ultRange, 0, Math.PI * 2); ctx.stroke();
                    } else if(this.type === "Clap") {
                        ctx.fillStyle = "rgba(255, 165, 2, 0.25)";
                        ctx.beginPath();
                        if(this.facing === 1) ctx.arc(this.x + this.width, this.y, this.ultRange, -Math.PI/2, Math.PI/4);
                        else ctx.arc(this.x, this.y, this.ultRange, Math.PI * 0.75, Math.PI * 1.5);
                        ctx.lineTo(this.x + 12, this.y); ctx.fill();
                    } else if(this.type === "Star" || this.type === "Jam") { 
                        ctx.strokeStyle = "#2ed573"; ctx.strokeRect(this.x - 4, this.y - 4, this.width + 8, this.height + 8);
                    }
                    this.ultEffectTimer--;
                }
                ctx.restore();
            }

            update(opp) {
                this.oldX = this.x; this.oldY = this.y;
                
                if (this.charmTimer > 0) {
                    this.charmTimer--;
                    if (opp) {
                        if (this.x < opp.x) { this.x += this.currentSpeed; this.facing = 1; }
                        else { this.x -= this.currentSpeed; this.facing = -1; }
                    }
                    // [유리 코롱2] 적이 매혹에 걸려있을 시 매 초당 유리의 체력을 4씩 회복시킴
                    if (opp && opp.type === "Yuri" && opp.cologne === 2) {
                        if (this.charmTimer % 60 === 0) {
                            opp.hp = Math.min(opp.maxHp, opp.hp + 4);
                            opp.popupText = "💖 매혹 흡수 힐링 +4"; opp.popupTimer = 25;
                        }
                    }
                }

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
                            } else { this.x = this.oldX; }
                        }
                    }
                }

                if (this.x < 0) this.x = 0;
                if (this.x > canvas.width - this.width) this.x = canvas.width - this.width;
                
                this.checkBushIntersection();

                let cooldownSpeed = this.inBush ? 1.50 : 1.0; 
                if(this.atkCooldown > 0) this.atkCooldown = Math.max(0, this.atkCooldown - cooldownSpeed);
                if(this.ultCooldown > 0) this.ultCooldown = Math.max(0, this.ultCooldown - cooldownSpeed);
                
                if(this.slowTimer > 0) this.slowTimer--;
                if(this.buffTimer > 0) this.buffTimer--;
                if(this.jamBuffTimer > 0) this.jamBuffTimer--;
                if(this.yuriHitBuffTimer > 0) this.yuriHitBuffTimer--;

                // [마리 코롱2] 공격을 안 하고 1초 대기할 때마다 보호막 생성 로직
                if (this.type === "Mari" && this.cologne === 2) {
                    if (this.atkCooldown === 0) {
                        this.mariNoAtkTimer++;
                        if (this.mariNoAtkTimer >= 60) {
                            this.shieldHp = Math.min(30, this.shieldHp + 2);
                            this.mariNoAtkTimer = 0;
                        }
                    } else { this.mariNoAtkTimer = 0; }
                }

                if (this.dotDamageTimer > 0) {
                    this.dotDamageTimer--;
                    if (this.dotDamageTimer % 60 === 0 && this.dotDamageCount > 0) {
                        this.takeDamage(3); this.dotDamageCount--;
                        this.popupText = "🎵 하트 음표 틱! -3"; this.popupTimer = 30;
                    }
                }
            }

            jump() {
                if (this.charmTimer > 0) return; 
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
                if(this.atkCooldown > 0 || this.charmTimer > 0) return;
                let validRange = this.calculateWallBlockingRange(this.currentRange);
                this.lastRenderRange = validRange; 
                this.effectTimer = 4; this.atkCooldown = this.currentAtkDelay; 
                
                let myL = this.facing === 1 ? this.x + this.width : this.x - validRange;
                let myR = this.facing === 1 ? this.x + this.width + validRange : this.x;

                if(this.type === "Clap") {
                    if(this.clapStacks < 20) this.clapStacks++;
                }

                // [잼 코롱1] 일반 공격 시 5% 확률로 궁극기 게이지 즉시 충전 완료
                if (this.type === "Jam" && this.cologne === 1) {
                    if (Math.random() < 0.05) {
                        this.ultCooldown = 0; this.popupText = "⚡ 코롱 대성공! 궁 즉시 충전"; this.popupTimer = 45;
                    }
                }

                if(myR >= opp.x && myL <= opp.x + opp.width && this.y + this.height >= opp.y && this.y <= opp.y + opp.height) {
                    let finalDmg = this.damage;
                    
                    // [마리 코롱1] 25% 확률로 +3 추가 데미지 부여
                    if (this.type === "Mari" && this.cologne === 1) {
                        if (Math.random() < 0.25) {
                            finalDmg += 3; this.popupText = "💥 코롱 크리티컬 +3!"; this.popupTimer = 35;
                        }
                    }

                    opp.takeDamage(finalDmg);

                    // [유리 코롱1] 평타 적중 시 이동 속도 1초간 가속 발동
                    if (this.type === "Yuri" && this.cologne === 1) {
                        this.yuriHitBuffTimer = 60; this.popupText = "⚡ 발걸음 가뿐! (이속 +15%)"; this.popupTimer = 30;
                    }
                }
            }

            useUltimate(opp) {
                if(this.ultCooldown > 0 || this.charmTimer > 0) return;
                this.ultCooldown = this.ultMaxCooldown;

                // [스타 코롱1] 궁극기 시전 시 즉시 상대에게 원격 5 데미지 충격파 선사
                if (this.type === "Star" && this.cologne === 1) {
                    opp.takeDamage(5); opp.popupText = "⚡ 스타 코롱 저격! -5"; opp.popupTimer = 40;
                }

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
                    if(dist < this.ultRange + 12) { opp.takeDamage(this.transparentUltDamage); this.hp = Math.min(this.maxHp, this.hp + 10); }
                } else if(this.type === "Clap") {
                    this.ultEffectTimer = 15;
                    let targetInUltRange = false;
                    let dx = opp.x - this.x; let dy = opp.y - this.y;
                    let distance = Math.sqrt(dx*dx + dy*dy);
                    if(distance <= this.ultRange) {
                        let correctDirection = (this.facing === 1 && dx >= -10) || (this.facing === -1 && dx <= 10);
                        if((dy <= 15) && correctDirection) targetInUltRange = true;
                    }
                    
                    // [클랩 코롱2] 궁극기 데미지 기본 +5 보너스 정산 결합
                    let baseBonus = (this.cologne === 2) ? 5 : 0;
                    let finalClapDamage = (this.clapStacks * 2) + baseBonus;
                    this.clapStacks = 0;

                    if(targetInUltRange) {
                        opp.takeDamage(finalClapDamage); this.clapStacks = 2;
                        this.popupText = `👏 클랩 스매시! ${finalClapDamage}딜`;
                    } else { this.popupText = "공중 헛손질 👏"; }
                    this.popupTimer = 60;
                } else if(this.type === "Yuri") {
                    this.ultEffectTimer = 25;
                    let dx = (this.x + 12) - (opp.x + 12); let dy = (this.y + 19) - (opp.y + 19);
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    if(dist <= this.ultRange + 15) {
                        opp.charmTimer = 120; opp.dotDamageTimer = 181; opp.dotDamageCount = 3;   
                        this.popupText = "💖 사랑의 노래! (2초 매혹)";
                    } else { this.popupText = "노래 메아리가 닿지 않음 💔"; }
                    this.popupTimer = 70;
                } else if(this.type === "Star") {
                    this.ultEffectTimer = 15; this.buffTimer = 120;
                } else if(this.type === "Jam") {
                    this.ultEffectTimer = 15; 
                    let rnd = Math.random();
                    
                    // [잼 코롱2] 직전 판이 꽝이었다면 이번 판 주사위 무조건 확정 대박 처리 리다이렉트
                    if (this.cologne === 2 && this.jamNextIsJackpot) {
                        rnd = 0.05; // 10% 미만 대박 확정 난수로 강제 보정
                        this.jamNextIsJackpot = false; // 일회성이므로 플래그 회수
                    }

                    if (rnd < 0.10) { 
                        opp.takeDamage(25); this.popupText = "💥 대박! 25 데미지!!"; 
                    } else if (rnd < 0.30) { 
                        this.hp = Math.min(this.maxHp, this.hp + 20); this.popupText = "💚 힐링! HP +20 회복"; 
                    } else if (rnd < 0.40) { 
                        this.jamBuffTimer = 120; this.popupText = "🏹 신속! 사거리 +3칸"; 
                    } else if (rnd < 0.60) { 
                        this.x = opp.x + (opp.facing === 1 ? -30 : 30); this.y = opp.y; opp.takeDamage(10); this.popupText = "🔮 습격! 순간이동"; 
                    } else if (rnd < 0.80) { 
                        this.shieldHp = 15; this.popupText = "🛡️ 방어! 배리어 활성"; 
                    } else { 
                        this.popupText = "💨 꽝! 다음 기회에"; 
                        // [잼 코롱2] 보정 스택 활성화
                        if (this.cologne === 2) this.jamNextIsJackpot = true;
                    }
                    this.popupTimer = 100; 
                }
            }
        }

        let p1, p2;

        function selectChar(type) {
            // 현재 타겟팅 카드 리셋 및 발광 효과 제어
            if (selectPhase === "P1_CHAR") {
                p1Sel = type;
                document.querySelectorAll(".char-card").forEach(c => c.classList.remove("selected-p1"));
                document.getElementById("card-" + type).classList.add("selected-p1");
                
                // 코롱 동적 폼 패널 오픈
                document.getElementById("cologne-panel").classList.remove("hidden");
                document.getElementById("cologne-panel-title").innerText = `▶ 1P [${type}]의 패시브 코롱 향수 장착`;
                document.getElementById("col-btn-1").innerText = cologneData[type].c1;
                document.getElementById("col-btn-2").innerText = cologneData[type].c2;
                document.getElementById("col-btn-1").classList.add("active");
                document.getElementById("col-btn-2").classList.remove("active");
                p1Cologne = 1;
                selectPhase = "P1_COL";
            } else if (selectPhase === "P2_CHAR") {
                p2Sel = type;
                document.querySelectorAll(".char-card").forEach(c => c.classList.remove("selected-p2"));
                document.getElementById("card-" + type).classList.add("selected-p2");
                
                document.getElementById("cologne-panel").classList.remove("hidden");
                document.getElementById("cologne-panel-title").innerText = `▶ 2P [${type}]의 패시브 코롱 향수 장착`;
                document.getElementById("col-btn-1").innerText = cologneData[type].c1;
                document.getElementById("col-btn-2").innerText = cologneData[type].c2;
                document.getElementById("col-btn-1").classList.add("active");
                document.getElementById("col-btn-2").classList.remove("active");
                p2Cologne = 1;
                selectPhase = "P2_COL";
            }
        }

        function chooseCologne(num) {
            if (selectPhase === "P1_COL") {
                p1Cologne = num;
                document.getElementById("col-btn-1").classList.toggle("active", num === 1);
                document.getElementById("col-btn-2").classList.toggle("active", num === 2);
                
                // 1P 세팅 종료 후 즉시 2P 영웅 픽 단계로 연쇄 토글 전환
                setTimeout(() => {
                    selectPhase = "P2_CHAR";
                    document.getElementById("select-title").innerText = "2P 영웅 낙점 (v1.30v)";
                    document.getElementById("cologne-panel").classList.add("hidden");
                }, 400);

            } else if (selectPhase === "P2_COL") {
                p2Cologne = num;
                document.getElementById("col-btn-1").classList.toggle("active", num === 1);
                document.getElementById("col-btn-2").classList.toggle("active", num === 2);
                
                setTimeout(() => {
                    selectPhase = "READY";
                    document.getElementById("select-title").innerText = "모든 특성 세팅 및 동기화 완료";
                    document.getElementById("start-game-btn").classList.remove("hidden");
                }, 400);
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
            p1 = new Player(100, 200, p1Sel, true, p1Cologne); 
            p2 = new Player(530, 200, p2Sel, false, p2Cologne);
            gameState = "PLAY";
        }

        function resetGame() {
            p1Sel = null; p2Sel = null; p1Cologne = 1; p2Cologne = 1;
            selectPhase = "P1_CHAR";
            document.querySelectorAll(".char-card").forEach(c => {
                c.classList.remove("selected-p1"); c.classList.remove("selected-p2");
            });
            document.getElementById("select-title").innerText = "1P 영웅 낙점 (v1.30v)";
            document.getElementById("select-screen").classList.remove("hidden");
            document.getElementById("result-screen").classList.add("hidden");
            document.getElementById("start-game-btn").classList.add("hidden");
            document.getElementById("cologne-panel").classList.add("hidden");
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
                if (p1.charmTimer <= 0) {
                    if (keys["KeyA"]) { p1.x -= p1.currentSpeed; p1.facing = -1; }
                    if (keys["KeyD"]) { p1.x += p1.currentSpeed; p1.facing = 1; }
                    if (keys["Space"]) p1.jump();
                }
                if (p2.charmTimer <= 0) {
                    if (keys["ArrowLeft"]) { p2.x -= p2.currentSpeed; p2.facing = -1; }
                    if (keys["ArrowRight"]) { p2.x += p2.currentSpeed; p2.facing = 1; }
                    if (keys["ArrowUp"]) p2.jump();
                }

                p1.update(p2); p2.update(p1); p1.draw(); p2.draw();

                if(p1.hp <= 0 || p2.hp <= 0) {
                    gameState = "END";
                    document.getElementById("result-screen").classList.remove("hidden");
                    document.getElementById("winner-text").innerText = p1.hp <= 0 ? "2P 승리!" : "1P 승리!";
                }
            } else if (gameState === "SELECT") {
                ctx.fillStyle = "#15151c"; ctx.font = "12px Arial";
                ctx.fillText("코롱 패시브 엔진이 장착 대기 중입니다.", 230, 160);
            } else { p1.draw(); p2.draw(); }
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
</body>
</html>
"""

components.html(game_html, height=485)
