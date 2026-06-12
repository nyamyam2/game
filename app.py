import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="네온 배틀 v1.41", layout="centered")

st.title("⚔️ 네온 배틀 버전 1.41v 패치")
st.caption("🤖 AI 벽 공격 방지(난이도:보통) & 미니로봇 크기 확대 및 타격 가능 패치 완료!")

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
        
        .char-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 6px; margin: 8px 0; }
        .char-card { background: #1a1a26; border: 2px solid #2d2d3d; border-radius: 10px; padding: 6px; width: 88px; cursor: pointer; transition: 0.2s; text-align: center; }
        .char-card.selected-p1 { border-color: #00f2ff; background: #182a3c; }
        .char-card.selected-p2 { border-color: #ff4757; background: #3c1820; }
        
        .cologne-container { display: flex; justify-content: center; gap: 15px; margin: 10px 0; background: #161622; padding: 10px; border-radius: 8px; border: 1px dashed #444; }
        .cologne-btn { background: #2b2b3d; color: #fff; border: 2px solid #444; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 11px; width: 45%; text-align: left; }
        .cologne-btn:hover { border-color: #00f2ff; background: #35354e; }
        .cologne-btn.active { background: #00f2ff; color: #000; font-weight: bold; border-color: #fff; }
        
        .avatar-frame { width: 42px; height: 42px; margin: 0 auto 5px; background: #242436; border-radius: 50%; border: 2px solid #3d3d5c; overflow: hidden; position: relative; }
        .eye-left, .eye-right { background: #111; width: 4px; height: 4px; border-radius: 50%; position: absolute; top: 11px; z-index: 5; }
        .eye-left { left: 6px; } .eye-right { left: 16px; }

        .hero-main { background: #ffd2a1; width: 30px; height: 32px; border-radius: 50%; position: absolute; bottom: 6px; left: 6px; }
        .main-hair-top { background: #1a1a1a; width: 34px; height: 16px; position: absolute; top: -3px; left: -2px; border-radius: 8px 8px 0 0; }
        .main-suit { background: #1e90ff; width: 40px; height: 15px; position: absolute; bottom: 0; left: -5px; border-radius: 4px 4px 0 0; }

        .hero-mari { background: #ffe3ca; width: 26px; height: 28px; border-radius: 50%; position: absolute; bottom: 8px; left: 8px; z-index: 2; }
        .mari-long-hair-back { background: #4a2831; width: 32px; height: 36px; position: absolute; top: 12px; left: 5px; border-radius: 4px 4px 12px 12px; z-index: 1; }
        .mari-hair-top { background: #ff527b; width: 30px; height: 14px; position: absolute; top: -4px; left: -2px; border-radius: 8px 8px 0 0; }

        .hero-star { background: #ffe0bd; width: 26px; height: 28px; border-radius: 50%; position: absolute; bottom: 6px; left: 8px; }
        .star-crown-gold { background: #f1c40f; width: 20px; height: 10px; position: absolute; top: -9px; left: 3px; clip-path: polygon(0 100%, 0 20%, 30% 60%, 50% 0, 70% 60%, 100% 20%, 100% 100%); z-index: 6; }
        .star-hair-blonde { background: #fecc5c; width: 30px; height: 12px; position: absolute; top: -2px; left: -2px; border-radius: 6px 6px 0 0; }
        
        .hero-jam { background: #ffd2a1; width: 26px; height: 28px; border-radius: 50%; position: absolute; bottom: 6px; left: 8px; }
        .jam-green-cap { background: #2ed573; width: 30px; height: 11px; position: absolute; top: -4px; left: -2px; border-radius: 4px 4px 0 0; z-index: 6; }

        .hero-clap { background: #fcd1a1; width: 26px; height: 28px; border-radius: 50%; position: absolute; bottom: 6px; left: 8px; }
        .clap-hair { background: #eccc68; width: 30px; height: 12px; position: absolute; top: -3px; left: -2px; border-radius: 6px 6px 0 0; }

        .hero-yuri { background: #fff1e0; width: 26px; height: 28px; border-radius: 50%; position: absolute; bottom: 6px; left: 8px; z-index: 2; }
        .yuri-ponytail { background: #4b382a; width: 14px; height: 24px; position: absolute; top: 4px; left: 20px; border-radius: 0 12px 12px 0; transform: rotate(10deg); z-index: 1; }
        .yuri-hair-top { background: #4b382a; width: 30px; height: 14px; position: absolute; top: -3px; left: -2px; border-radius: 8px 8px 0 0; }

        .hero-robot { background: #747d8c; width: 28px; height: 28px; border-radius: 4px; position: absolute; bottom: 6px; left: 7px; border: 1px solid #a4b0be; }
        .robot-antenna { background: #ff4757; width: 4px; height: 10px; position: absolute; top: -9px; left: 12px; border-radius: 2px; }
        .robot-eye-neon { background: #00f2ff; width: 18px; height: 4px; position: absolute; top: 8px; left: 5px; box-shadow: 0 0 6px #00f2ff; }

        .map-container { display: flex; justify-content: center; gap: 10px; margin: 4px 0; }
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
            <div id="p1-control-hint">1P: A/D(이동), Space(점프), F(평타), G(궁극기)</div>
            <div id="p2-control-hint">2P: ◀/▶(이동), ▲(점프), ↓(평타), L(궁극기)</div>
        </div>

        <div id="select-screen" class="ui-overlay">
            <h3 id="select-title" style="color:#00f2ff; margin: 0 0 2px 0; font-size: 15px;">1P 영웅 낙점 (v1.41v)</h3>
            <p id="select-subtitle" style="font-size:11px; color:#aaa; margin:0 0 6px 0;">인공지능 벽 공격 방지 알고리즘 및 밸런스 조정 패치판</p>
            
            <div class="char-container">
                <div class="char-card" id="card-Main" onclick="selectChar('Main')">
                    <div class="avatar-frame"><div class="hero-main"><div class="main-hair-top"></div><div class="eye-left"></div><div class="eye-right"></div><div class="main-suit"></div></div></div>
                    <strong style="color:#6dd5fa; font-size:11px;">메인</strong>
                </div>
                <div class="char-card" id="card-Mari" onclick="selectChar('Mari')">
                    <div class="mari-long-hair-back"></div>
                    <div class="avatar-frame" style="background:#3a2936; border-color:#5c3d52;"><div class="hero-mari"><div class="mari-hair-top"></div><div class="eye-left"></div><div class="eye-right"></div></div></div>
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
                    <div class="avatar-frame" style="background:#362f24; border-color:#5c4e3d;"><div class="hero-clap"><div class="clap-hair"></div><div class="eye-left"></div><div class="eye-right"></div></div></div>
                    <strong style="color:#ffa502; font-size:11px;">클랩</strong>
                </div>
                <div class="char-card" id="card-Yuri" onclick="selectChar('Yuri')">
                    <div class="yuri-ponytail"></div>
                    <div class="avatar-frame" style="background:#3a2d24; border-color:#5c4636;"><div class="hero-yuri"><div class="yuri-hair-top"></div><div class="eye-left" style="background:#ff4757;"></div><div class="eye-right" style="background:#ff4757;"></div></div></div>
                    <strong style="color:#ff4757; font-size:11px;">유리💖</strong>
                </div>
                <div class="char-card" id="card-Robot" onclick="selectChar('Robot')">
                    <div class="avatar-frame" style="background:#2f3542; border-color:#747d8c;"><div class="hero-robot"><div class="robot-antenna"></div><div class="robot-eye-neon"></div></div></div>
                    <strong style="color:#a4b0be; font-size:11px;">로봇킹🤖</strong>
                </div>
            </div>

            <div id="cologne-panel" class="hidden">
                <div style="font-size: 11px; color: #fffa65; margin-bottom: 4px; font-weight: bold;" id="cologne-panel-title">패시브 코롱 향수 장착</div>
                <div class="cologne-container">
                    <button id="col-btn-1" class="cologne-btn" onclick="chooseCologne(1)">코롱 1</button>
                    <button id="col-btn-2" class="cologne-btn" onclick="chooseCologne(2)">코롱 2</button>
                </div>
            </div>

            <div class="map-container">
                <button id="mode-pvp-btn" class="map-btn selected" onclick="selectMode('PVP')">인간 vs 인간 (2P)</button>
                <button id="mode-ai-btn" class="map-btn" onclick="selectMode('AI')">인간 vs 인공지능 (AI: 보통)</button>
            </div>

            <div class="map-container">
                <button id="map0-btn" class="map-btn selected" onclick="selectMap(0)">평지 아레나</button>
                <button id="map1-btn" class="map-btn" onclick="selectMap(1)">네온 미로 (덤불회복 1.5초)</button>
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
        let playMode = "PVP"; 
        let p1Sel = null, p2Sel = null;
        let p1Cologne = 1, p2Cologne = 1;
        let selectPhase = "P1_CHAR"; 
        let selectedMapIndex = 0;

        const cologneData = {
            Main: { c1: "코롱1: 최대체력 +5 및 공격력 +1 증가 (리워크)", c2: "코롱2: 궁극기 쿨타임 1.5초 감소" },
            Mari: { c1: "코롱1: 평타 시 30% 확률로 +3딜", c2: "코롱2: 대기 시 초당 보호막 +2 (최대 50)" },
            Star: { c1: "코롱1: 궁 사용시 적에게 즉시 5딜 타격", c2: "코롱2: 일반 공격 데미지 +1 상시증가" },
            Jam:  { c1: "코롱1: 평타 명중시 8% 확률로 궁 즉시충전", c2: "코롱2: 꽝 나오면 다음 대박 데미지 +5 (버프)" },
            Clap: { c1: "코롱1: 타격 명중 시에만 박수 획득량 +1", c2: "코롱2: 궁극기 베이스 데미지 +5 보너스" },
            Yuri: { c1: "코롱1: 타격 명중 시 25% 확률로 1.5초 매혹", c2: "코롱2: 적 매혹 시 유리의 체력 초당 4 회복" },
            Robot:{ c1: "코롱1: 패시브 이속 35% 가속 & 공속 0.2초 단축", c2: "코롱2: 미니 로봇의 스탯 강화 (체력+5, 공격+1)" }
        };

        const mapObstacles = [
            { x: 140, y: 270, w: 45, h: 40 }, { x: 475, y: 270, w: 45, h: 40 }, { x: 260, y: 195, w: 140, h: 20 } 
        ];
        const mapBushes = [
            { x: 40, y: 260, w: 70, h: 50 }, { x: 550, y: 260, w: 70, h: 50 }, { x: 300, y: 145, w: 60, h: 50 }
        ];

        // 🤖 미니 로봇 클래스 (크기 확대 피격 판정 및 체력 동기화 구현)
        class MiniRobot {
            constructor(x, y, is1P, enhanced) {
                this.is1P = is1P;
                this.x = x + (Math.random() * 30 - 15);
                this.y = y - 10;
                this.width = 22;  // 크기 키움 (12 -> 22)
                this.height = 24; // 크기 키움 (14 -> 24)
                this.vY = 0;
                this.hp = enhanced ? 25 : 20;
                this.maxHp = this.hp;
                this.damage = enhanced ? 4 : 3;
                this.speed = 2.4; 
                this.range = 3 * GRID;
                this.atkDelay = 30; 
                this.atkCooldown = 0;
            }
            update(opp) {
                this.vY += GRAVITY;
                this.y += this.vY;
                if(this.y >= canvas.height - this.height - 15) {
                    this.y = canvas.height - this.height - 15; this.vY = 0;
                }
                if(selectedMapIndex === 1) {
                    for(let obs of mapObstacles) {
                        if (this.x + this.width > obs.x && this.x < obs.x + obs.w && this.y + this.height > obs.y && this.y < obs.y + obs.h) {
                            this.y = obs.y - this.height; this.vY = 0;
                        }
                    }
                }

                let dx = opp.x - this.x;
                if(Math.abs(dx) > this.range - 5) {
                    this.x += Math.sign(dx) * this.speed;
                }

                if(this.atkCooldown > 0) this.atkCooldown--;
                else {
                    let dist = Math.sqrt(dx*dx + (opp.y - this.y)*(opp.y - this.y));
                    if(dist <= this.range) {
                        opp.takeDamage(this.damage);
                        this.atkCooldown = this.atkDelay;
                    }
                }
            }
            draw() {
                ctx.save();
                ctx.fillStyle = this.is1P ? "#00f2ff" : "#ff4757";
                ctx.fillRect(this.x, this.y, this.width, this.height);
                
                // 체력바 가시화 추가
                ctx.fillStyle = "red"; ctx.fillRect(this.x, this.y - 6, this.width, 2);
                ctx.fillStyle = "lime"; ctx.fillRect(this.x, this.y - 6, (this.hp / this.maxHp) * this.width, 2);

                ctx.fillStyle = "white";
                ctx.fillRect(this.x + 4, this.y + 5, 4, 3);
                ctx.fillRect(this.x + 14, this.y + 5, 4, 3);
                ctx.restore();
            }
        }

        const keys = {};
        window.addEventListener("keydown", (e) => { 
            keys[e.code] = true; 
            if(["Space", "ArrowUp", "ArrowDown"].includes(e.code)) e.preventDefault();
            if(gameState === "PLAY") {
                if(e.code === "KeyF" && p1.charmTimer <= 0 && p1.stunTimer <= 0) p1.attack(p2);
                if(e.code === "KeyG" && p1.charmTimer <= 0 && p1.stunTimer <= 0) p1.useUltimate(p2);
                if(playMode === "PVP") {
                    if(e.code === "ArrowDown" && p2.charmTimer <= 0 && p2.stunTimer <= 0) p2.attack(p1);
                    if(e.code === "KeyL" && p2.charmTimer <= 0 && p2.stunTimer <= 0) p2.useUltimate(p1);
                }
            }
        });
        window.addEventListener("keyup", (e) => { keys[e.code] = false; });

        class Player {
            constructor(x, y, type, is1P, cologneChoice) {
                this.is1P = is1P; this.type = type; this.cologne = cologneChoice;
                this.x = x; this.y = y; this.oldX = x; this.oldY = y;
                this.width = 25; this.height = 38; this.vY = 0;
                this.facing = is1P ? 1 : -1; this.isJumping = false;
                
                this.slowTimer = 0; this.buffTimer = 0; this.inBush = false; this.bushHealTimer = 0;    
                this.popupText = ""; this.popupTimer = 0; 
                this.jamBuffTimer = 0; this.shieldHp = 0;       
                
                this.charmTimer = 0; this.dotDamageTimer = 0; this.dotDamageCount = 0;
                this.clapStacks = 0; this.stunTimer = 0;
                this.mariNoAtkTimer = 0;
                this.jamNextIsJackpot = false;

                if(type === "Main") {
                    // 메인 코롱1 리워크: 체력 +5증가, 공격력 +1증가
                    let hpMax = (this.cologne === 1) ? 105 : 100;
                    this.name = "메인"; this.hp = hpMax; this.maxHp = hpMax; 
                    this.damage = (this.cologne === 1) ? 8 : 7;                     
                    this.range = 4 * GRID; this.atkDelay = 18; this.baseSpeed = 4.2; 
                    this.ultDamage = 18; this.ultRange = 8 * GRID; 
                    this.ultMaxCooldown = (this.cologne === 2) ? 570 : 660; 
                    this.color = "#1e90ff"; this.faceSymbol = "🕶️";
                } else if(type === "Mari") {
                    this.name = "마리"; this.hp = 90; this.maxHp = 90; this.damage = 9;                     
                    this.range = 15 * GRID; this.atkDelay = 75; this.baseSpeed = 3.6;           
                    this.transparentUltDamage = 20; this.ultRange = 4 * GRID; this.ultMaxCooldown = 720; 
                    this.color = "#ff00ff"; this.faceSymbol = "🎀";
                } else if(type === "Star") { 
                    this.name = "스타"; this.hp = 125; this.maxHp = 125; 
                    this.damage = (this.cologne === 2) ? 7 : 6;                    
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
                } else if(type === "Yuri") { 
                    this.name = "유리"; this.hp = 100; this.maxHp = 100; this.damage = 4;
                    this.range = 7 * GRID; this.atkDelay = 18; this.baseSpeed = 4.0; 
                    this.ultRange = 5 * GRID; this.ultMaxCooldown = 900; 
                    this.color = "#ff4757"; this.faceSymbol = "🎓";
                } else { 
                    // 로봇킹 일반 데미지 1 하향 패치 (8 -> 7)
                    this.name = "로봇킹"; this.hp = 120; this.maxHp = 120; this.damage = 7;
                    this.range = 4 * GRID; 
                    this.atkDelay = (this.cologne === 1) ? 108 : 120; 
                    this.baseSpeed = (this.cologne === 1) ? 3.5 * 1.35 : 3.5;
                    this.ultRange = 0; this.ultMaxCooldown = 900; 
                    this.color = "#747d8c"; this.faceSymbol = "🤖";
                }

                this.atkCooldown = 0; this.ultCooldown = 0;
                this.effectTimer = 0; this.ultEffectTimer = 0; this.lastRenderRange = 0;
            }

            get currentSpeed() {
                if (this.charmTimer > 0) return 2.0; 
                if (this.stunTimer > 0) return 0; 
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
                if (this.stunTimer > 0) ctx.fillStyle = "#ffa502"; 
                else if (this.charmTimer > 0) ctx.fillStyle = "#ff758c"; 
                else if (this.slowTimer > 0) ctx.fillStyle = "#57606f"; 
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

                ctx.fillStyle = this.charmTimer > 0 ? "red" : "#000";
                if(this.facing === 1) ctx.fillRect(this.x + 16, this.y + 10, 2, 2);
                else ctx.fillRect(this.x + 7, this.y + 10, 2, 2);

                ctx.fillStyle = "white"; ctx.font = "9px Arial";
                let nameLabel = this.name + (this.is1P ? "(1P)" : "(2P)") + ` [C${this.cologne}]`;
                if(this.type === "Clap") nameLabel += ` [${this.clapStacks}👏]`;
                ctx.fillText(nameLabel, this.x - 5, this.y - 25);
                
                if (this.stunTimer > 0) { ctx.fillStyle = "#ffa502"; ctx.fillText("💫기절💫", this.x - 4, this.y - 32); }
                else if (this.charmTimer > 0) { ctx.fillStyle = "#ff4757"; ctx.fillText("♥매혹♥", this.x - 4, this.y - 32); }

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
                    } else if(this.type === "Star" || this.type === "Jam" || this.type === "Robot") { 
                        ctx.strokeStyle = "#2ed573"; ctx.strokeRect(this.x - 4, this.y - 4, this.width + 8, this.height + 8);
                    }
                    this.ultEffectTimer--;
                }
                ctx.restore();
            }

            update(opp) {
                this.oldX = this.x; this.oldY = this.y;
                if (this.stunTimer > 0) this.stunTimer--;

                if (this.charmTimer > 0) {
                    this.charmTimer--;
                    if (opp) {
                        if (this.x < opp.x) { this.x += this.currentSpeed; this.facing = 1; }
                        else { this.x -= this.currentSpeed; this.facing = -1; }
                    }
                }

                this.vY += GRAVITY; this.y += this.vY;
                if (this.y >= canvas.height - this.height - 15) {
                    this.y = canvas.height - this.height - 15; this.vY = 0; this.isJumping = false;
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

                // 🛠️ [덤불회복 1.5초 동기화] 90프레임 주기로 치유 연산 가동
                if(this.inBush && this.hp > 0) {
                    this.bushHealTimer++;
                    if(this.bushHealTimer >= 90) { 
                        this.hp = Math.min(this.maxHp, this.hp + 3);
                        this.popupText = "🌿 덤불 치유 +3"; this.popupTimer = 25;
                        this.bushHealTimer = 0;
                    }
                } else { this.bushHealTimer = 0; }

                let cooldownSpeed = this.inBush ? 1.50 : 1.0; 
                if(this.atkCooldown > 0) this.atkCooldown = Math.max(0, this.atkCooldown - cooldownSpeed);
                if(this.ultCooldown > 0) this.ultCooldown = Math.max(0, this.ultCooldown - cooldownSpeed);
                
                if(this.slowTimer > 0) this.slowTimer--;
                if(this.buffTimer > 0) this.buffTimer--;
                if(this.jamBuffTimer > 0) this.jamBuffTimer--;

                if (this.type === "Mari" && this.cologne === 2) {
                    if (this.atkCooldown === 0) {
                        this.mariNoAtkTimer++;
                        if (this.mariNoAtkTimer >= 60) {
                            this.shieldHp = Math.min(50, this.shieldHp + 2);
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
                if (this.charmTimer > 0 || this.stunTimer > 0) return; 
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
                if(this.atkCooldown > 0 || this.charmTimer > 0 || this.stunTimer > 0) return;
                let validRange = this.calculateWallBlockingRange(this.currentRange);
                this.lastRenderRange = validRange; 
                this.effectTimer = 4; this.atkCooldown = this.currentAtkDelay; 
                
                let myL = this.facing === 1 ? this.x + this.width : this.x - validRange;
                let myR = this.facing === 1 ? this.x + this.width + validRange : this.x;

                let hitOpponent = (myR >= opp.x && myL <= opp.x + opp.width && this.y + this.height >= opp.y && this.y <= opp.y + opp.height);

                // 🛠️ [미니로봇 피격 메커니즘] 플레이어가 일반공격을 뻗었을 때 범위 내의 미니로봇 타격 및 파괴 가능
                for(let i = activeMinions.length - 1; i >= 0; i--) {
                    let m = activeMinions[i];
                    // 적 진영의 소환수만 타격 가능
                    if (m.is1P !== this.is1P) {
                        if(myR >= m.x && myL <= m.x + m.width && this.y + this.height >= m.y && this.y <= m.y + m.height) {
                            m.hp -= this.damage;
                            this.popupText = "💥 미니로봇 요격 성공!"; this.popupTimer = 25;
                            if(m.hp <= 0) activeMinions.splice(i, 1);
                        }
                    }
                }

                // 🛠️ [클랩 리워크] 오직 타격 성공(명중) 시에만 스택 연산이 일어나도록 변경
                if(this.type === "Clap" && hitOpponent) {
                    let gain = (this.cologne === 1) ? 2 : 1;
                    if(this.clapStacks < 20) this.clapStacks = Math.min(20, this.clapStacks + gain);
                }

                if(hitOpponent) {
                    let finalDmg = this.damage;
                    if (this.type === "Mari" && this.cologne === 1) {
                        if (Math.random() < 0.30) { finalDmg += 3; this.popupText = "💥 코롱 크리티컬 +3!"; this.popupTimer = 35; }
                    }

                    opp.takeDamage(finalDmg);

                    if (this.type === "Jam" && this.cologne === 1) {
                        if (Math.random() < 0.08) { this.ultCooldown = 0; this.popupText = "⚡ 명중! 궁 즉시 100% 충전"; this.popupTimer = 45; }
                    }

                    if (this.type === "Yuri" && this.cologne === 1) {
                        if(Math.random() < 0.25) { opp.charmTimer = 90; this.popupText = "💘 기습 매혹 (1.5초)"; this.popupTimer = 40; }
                    }

                    if (this.type === "Robot") {
                        opp.stunTimer = 30; opp.x += this.facing * GRID * 1.5; 
                        opp.popupText = "⚙️ 메카 펀치! 기절+넉백"; opp.popupTimer = 30;
                    }
                }
            }

            useUltimate(opp) {
                if(this.ultCooldown > 0 || this.charmTimer > 0 || this.stunTimer > 0) return;
                this.ultCooldown = this.ultMaxCooldown;

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
                    }
                    this.popupTimer = 70;
                } else if(this.type === "Star") {
                    this.ultEffectTimer = 15; this.buffTimer = 120;
                } else if(this.type === "Robot") {
                    this.ultEffectTimer = 20;
                    let isEnhanced = (this.cologne === 2); 
                    for(let i=0; i<3; i++) {
                        activeMinions.push(new MiniRobot(this.x, this.y, this.is1P, isEnhanced));
                    }
                    this.popupText = "🤖 미니 로봇 3개체 기동!!"; this.popupTimer = 60;
                } else if(this.type === "Jam") {
                    this.ultEffectTimer = 15; let rnd = Math.random();
                    if (this.cologne === 2 && this.jamNextIsJackpot) { rnd = 0.05; this.jamNextIsJackpot = false; }
                    
                    if (rnd < 0.10) { 
                        // 🛠️ [잼 코롱2 버프] 꽝 다음 대박 데미지 +5 증가 반영 (기존 25 -> 30)
                        let jackpotDmg = (this.cologne === 2) ? 30 : 25;
                        opp.takeDamage(jackpotDmg); 
                        this.popupText = `💥 대박! ${jackpotDmg} 데미지!!`; 
                    } 
                    else if (rnd < 0.30) { this.hp = Math.min(this.maxHp, this.hp + 20); this.popupText = "💚 힐링! HP +20 회복"; } 
                    else if (rnd < 0.40) { this.jamBuffTimer = 120; this.popupText = "🏹 신속! 사거리 +3칸"; } 
                    else if (rnd < 0.60) { this.x = opp.x + (opp.facing === 1 ? -30 : 30); this.y = opp.y; opp.takeDamage(10); this.popupText = "🔮 습격! 순간이동"; } 
                    else if (rnd < 0.80) { this.shieldHp = 15; this.popupText = "🛡️ 방어! 배리어 활성"; } 
                    else { this.popupText = "💨 꽝! 다음 기회에"; if (this.cologne === 2) this.jamNextIsJackpot = true; }
                    this.popupTimer = 100; 
                }
            }
        }

        let p1, p2;
        let activeMinions = []; 

        function selectMode(mode) {
            playMode = mode;
            document.getElementById("mode-pvp-btn").classList.toggle("selected", mode === "PVP");
            document.getElementById("mode-ai-btn").classList.toggle("selected", mode === "AI");
        }

        function selectChar(type) {
            if (selectPhase === "P1_CHAR") {
                p1Sel = type;
                document.querySelectorAll(".char-card").forEach(c => c.classList.remove("selected-p1"));
                document.getElementById("card-" + type).classList.add("selected-p1");
                
                document.getElementById("cologne-panel").classList.remove("hidden");
                document.getElementById("cologne-panel-title").innerText = `▶ 1P [${type}]의 패시브 코롱 선택`;
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
                document.getElementById("cologne-panel-title").innerText = `▶ 2P [${type}]의 패시브 코롱 선택`;
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
                
                setTimeout(() => {
                    if(playMode === "AI") {
                        const heroPool = ["Main", "Mari", "Star", "Jam", "Clap", "Yuri", "Robot"];
                        p2Sel = heroPool[Math.floor(Math.random() * heroPool.length)];
                        p2Cologne = Math.random() < 0.5 ? 1 : 2;
                        
                        selectPhase = "READY";
                        document.getElementById("select-title").innerText = "AI 상대 구성 완료! 난이도: 보통";
                        document.getElementById("cologne-panel").classList.add("hidden");
                        document.getElementById("start-game-btn").classList.remove("hidden");
                    } else {
                        selectPhase = "P2_CHAR";
                        document.getElementById("select-title").innerText = "2P 영웅 낙점 (v1.41v)";
                        document.getElementById("cologne-panel").classList.add("hidden");
                    }
                }, 300);

            } else if (selectPhase === "P2_COL") {
                p2Cologne = num;
                document.getElementById("col-btn-1").classList.toggle("active", num === 1);
                document.getElementById("col-btn-2").classList.toggle("active", num === 2);
                
                setTimeout(() => {
                    selectPhase = "READY";
                    document.getElementById("select-title").innerText = "모든 세팅 완료! 격돌하세요.";
                    document.getElementById("start-game-btn").classList.remove("hidden");
                }, 300);
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
            activeMinions = [];
            gameState = "PLAY";
        }

        function resetGame() {
            p1Sel = null; p2Sel = null; p1Cologne = 1; p2Cologne = 1;
            selectPhase = "P1_CHAR";
            activeMinions = [];
            document.querySelectorAll(".char-card").forEach(c => {
                c.classList.remove("selected-p1"); c.classList.remove("selected-p2");
            });
            document.getElementById("select-title").innerText = "1P 영웅 낙점 (v1.41v)";
            document.getElementById("select-screen").classList.remove("hidden");
            document.getElementById("result-screen").classList.add("hidden");
            document.getElementById("start-game-btn").classList.add("hidden");
            document.getElementById("cologne-panel").classList.add("hidden");
            gameState = "SELECT";
        }

        // 🤖 [AI 알고리즘 고도화] 벽 타격 방지 연산 장치 (난이도: 보통)
        let aiDecisionCounter = 0;
        function runAILogic() {
            if(p2.charmTimer > 0 || p2.stunTimer > 0) return;
            
            aiDecisionCounter++;
            let dx = p1.x - p2.x;

            // 추적 기동 속도 고정 (보통 난이도 맞춤형 전진)
            if(Math.abs(dx) > p2.currentRange - 10) {
                if(dx > 0) { p2.x += p2.currentSpeed; p2.facing = 1; }
                else { p2.x -= p2.currentSpeed; p2.facing = -1; }
            } else {
                if(aiDecisionCounter % 40 === 0) p2.facing = Math.sign(dx) || 1;
            }

            if(aiDecisionCounter % 120 === 0 && Math.random() < 0.4) {
                p2.jump();
            }

            // 사거리 내 진입 확인
            if(Math.abs(dx) <= p2.currentRange + 10) {
                if(p2.atkCooldown === 0) {
                    
                    // 🛠️ [핵심 인공지능 개화] 자신과 타겟 사이에 구조물(벽)이 존재하는지 확인하는 시선 검사 레이캐스팅
                    let wallBlocked = false;
                    if(selectedMapIndex === 1) {
                        let leftBound = Math.min(p1.x, p2.x);
                        let rightBound = Math.max(p1.x, p2.x);
                        for(let obs of mapObstacles) {
                            // 플레이어 라인 높이 근처에 가로막는 오브젝트 레이어가 존재할 때
                            if(obs.x + obs.w > leftBound && obs.x < rightBound && p2.y + 15 > obs.y && p2.y < obs.y + obs.h) {
                                wallBlocked = true;
                                break;
                            }
                        }
                    }

                    // 벽이 없을 때에만 칼같이 공격을 뻗도록 유도
                    if(!wallBlocked) {
                        p2.attack(p1);
                    } else {
                        // 벽에 막히면 점프하여 뛰어넘거나 전술적 우회를 시도함
                        if(Math.random() < 0.5) p2.jump();
                    }
                }
            }

            if(p2.ultCooldown === 0 && Math.random() < 0.2) {
                p2.useUltimate(p1);
            }
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
                if (p1.charmTimer <= 0 && p1.stunTimer <= 0) {
                    if (keys["KeyA"]) { p1.x -= p1.currentSpeed; p1.facing = -1; }
                    if (keys["KeyD"]) { p1.x += p1.currentSpeed; p1.facing = 1; }
                    if (keys["Space"]) p1.jump();
                }

                if(playMode === "PVP") {
                    if (p2.charmTimer <= 0 && p2.stunTimer <= 0) {
                        if (keys["ArrowLeft"]) { p2.x -= p2.currentSpeed; p2.facing = -1; }
                        if (keys["ArrowRight"]) { p2.x += p2.currentSpeed; p2.facing = 1; }
                        if (keys["ArrowUp"]) p2.jump();
                    }
                } else {
                    runAILogic(); 
                }

                p1.update(p2); p2.update(p1);

                for(let i = activeMinions.length - 1; i >= 0; i--) {
                    let m = activeMinions[i];
                    let targetEnemy = m.is1P ? p2 : p1;
                    m.update(targetEnemy);
                    m.draw();
                }

                p1.draw(); p2.draw();

                if(p1.hp <= 0 || p2.hp <= 0) {
                    gameState = "END";
                    document.getElementById("result-screen").classList.remove("hidden");
                    document.getElementById("winner-text").innerText = p1.hp <= 0 ? "2P (승리!)" : "1P (승리!)";
                }
            } else if (gameState === "SELECT") {
                ctx.fillStyle = "#15151c"; ctx.font = "12px Arial";
                ctx.fillText("AI 싱글 배틀 필드 준비 중...", 245, 160);
            } else { p1.draw(); p2.draw(); }
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
</body>
</html>
"""

components.html(game_html, height=485)
