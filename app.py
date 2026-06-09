import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정
st.set_page_config(page_title="스트림릿 격투 게임", layout="centered")

st.title("⚔️ 스트림릿 2P 배틀 게임")
st.caption("1P(메인): A/D (이동), SPACE (점프), F (공격) | 2P(메인): ◀/▶ (이동), ▲ (점프), L (공격)")

# 게임 구현을 위한 HTML5 / JavaScript 코드
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; background-color: #222; color: white; font-family: sans-serif; margin: 0; padding: 0; }
        canvas { background: #111; border: 4px solid #444; display: block; margin: 10px auto; box-shadow: 0 0 20px rgba(0,0,0,0.8); }
        .controls { font-size: 14px; color: #aaa; margin-top: 5px; }
    </style>
</head>
<body>

    <canvas id="gameCanvas" width="800" height="400"></canvas>
    <div id="winner-display" style="font-size: 24px; font-weight: bold; color: #ff4757; height: 30px;"></div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const winnerDisplay = document.getElementById("winner-display");

        // 물리 법칙 및 사거리 기준 (1칸 = 20px로 정의, 사거리 4칸 = 80px)
        const GRAVITY = 0.6;
        const GRID_SIZE = 20; 
        const ATTACK_RANGE = 4 * GRID_SIZE; // 80px

        // 게임 상태
        let gameOver = false;

        // 플레이어 클래스
        class Player {
            constructor(x, y, color, name, is1P) {
                this.name = name;
                this.x = x;
                this.y = y;
                this.width = 40;
                this.height = 60;
                this.color = color;
                this.hp = 100;
                this.damage = 20;
                this.speed = 5;
                const vX = 0;
                this.vY = 0;
                this.isJumping = false;
                this.isAttacking = false;
                this.attackCooldown = 0;
                this.facing = is1P ? 1 : -1; // 1: 우측, -1: 좌측
                this.is1P = is1P;
            }

            draw() {
                // 캐릭터 본체 (디자인)
                ctx.fillStyle = this.color;
                ctx.fillRect(this.x, this.y, this.width, this.height);

                // 눈 장식 (보는 방향 표시)
                ctx.fillStyle = "#fff";
                let eyeX = this.facing === 1 ? this.x + this.width - 12 : this.x + 4;
                ctx.fillRect(eyeX, this.y + 12, 8, 8);
                
                // 머리 장식 (왕관/뿔 형태)
                ctx.fillStyle = "#ffd32a";
                ctx.fillRect(this.x + 10, this.y - 8, 20, 8);

                // 체력바 그리기
                ctx.fillStyle = "#555";
                ctx.fillRect(this.x - 5, this.y - 20, 50, 6);
                ctx.fillStyle = this.hp > 30 ? "#2ed573" : "#ff4757";
                ctx.fillRect(this.x - 5, this.y - 20, (this.hp / 100) * 50, 6);

                // 이름 표시
                ctx.fillStyle = "#fff";
                ctx.font = "12px sans-serif";
                ctx.fillText(this.name + (this.is1P ? " (1P)" : " (2P)"), this.x - 5, this.y - 25);

                // 공격 이펙트 애니메이션
                if (this.isAttacking) {
                    ctx.fillStyle = "rgba(255, 234, 167, 0.6)";
                    if (this.facing === 1) {
                        ctx.fillRect(this.x + this.width, this.y + 15, ATTACK_RANGE, 30);
                    } else {
                        ctx.fillRect(this.x - ATTACK_RANGE, this.y + 15, ATTACK_RANGE, 30);
                    }
                }
            }

            update() {
                // 중력 적용
                this.vY += GRAVITY;
                this.y += this.vY;

                // 바닥 충돌 처리
                if (this.y >= canvas.height - this.height - 20) {
                    this.y = canvas.height - this.height - 20;
                    this.vY = 0;
                    this.isJumping = false;
                }

                // 화면 외곽 이탈 방지
                if (this.x < 0) this.x = 0;
                if (this.x > canvas.width - this.width) this.x = canvas.width - this.width;

                // 쿨다운 감소
                if (this.attackCooldown > 0) this.attackCooldown--;
                if (this.attackCooldown === 10) this.isAttacking = false; // 공격 이펙트 종료
            }

            jump() {
                if (!this.isJumping) {
                    this.vY = -13;
                    this.isJumping = true;
                }
            }

            attack(opponent) {
                if (this.attackCooldown === 0 && !gameOver) {
                    this.isAttacking = true;
                    this.attackCooldown = 20; // 다음 공격까지의 딜레이

                    // 사거리 및 피격 판정 계산
                    let myAttackLeft = this.facing === 1 ? this.x + this.width : this.x - ATTACK_RANGE;
                    let myAttackRight = this.facing === 1 ? this.x + this.width + ATTACK_RANGE : this.x;

                    // 상대방 히트박스와 겹치는지 확인 (Y축도 어느정도 맞아야 함)
                    if (
                        myAttackRight >= opponent.x &&
                        myAttackLeft <= opponent.x + opponent.width &&
                        this.y + this.height >= opponent.y &&
                        this.y <= opponent.y + opponent.height
                    ) {
                        opponent.hp -= this.damage;
                        if (opponent.hp < 0) opponent.hp = 0;
                    }
                }
            }
        }

        // 캐릭터 생성 (이름: 메인, 체력: 100, 공격력: 20)
        const p1 = new Player(150, 200, "#1e90ff", "메인", true);
        const p2 = new Player(600, 200, "#ff4757", "메인", false);

        // 키보드 입력 핸들링
        const keys = {};
        window.addEventListener("keydown", (e) => {
            keys[e.code] = true;
            
            // 스크롤 방지
            if(["Space", "ArrowUp", "ArrowDown"].includes(e.code)) {
                e.preventDefault();
            }

            // 공격 키 단발 입력 처리
            if (e.code === "KeyF") p1.attack(p2);
            if (e.code === "KeyL") p2.attack(p1);
        });
        window.addEventListener("keyup", (e) => { keys[e.code] = false; });

        // 게임 루프
        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 배경 바닥 그리기
            ctx.fillStyle = "#444";
            ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

            if (!gameOver) {
                // 1P 조작 (A, D, Space)
                if (keys["KeyA"]) { p1.x -= p1.speed; p1.facing = -1; }
                if (keys["KeyD"]) { p1.x += p1.speed; p1.facing = 1; }
                if (keys["Space"]) { p1.jump(); }

                // 2P 조작 (화살표 좌, 우, 위)
                if (keys["ArrowLeft"]) { p2.x -= p2.speed; p2.facing = -1; }
                if (keys["ArrowRight"]) { p2.x += p2.speed; p2.facing = 1; }
                if (keys["ArrowUp"]) { p2.init; p2.jump(); }

                // 업데이트
                p1.update();
                p2.update();

                // 승리 조건 체크
                if (p1.hp <= 0) {
                    gameOver = true;
                    winnerDisplay.innerText = "🏆 2P Win!! 🏆";
                } else if (p2.hp <= 0) {
                    gameOver = true;
                    winnerDisplay.innerText = "🏆 1P Win!! 🏆";
                }
            }

            // 그리기
            p1.draw();
            p2.draw();

            requestAnimationFrame(gameLoop);
        }

        // 게임 시작
        gameLoop();
    </script>
</body>
</html>
"""

# 스트림릿 컴포넌트로 HTML 삽입 (크기는 게임창에 맞게 조절)
components.html(game_html, height=480)

st.info("💡 참고: 공격 키는 1P는 **'F'**, 2P는 **'L'** 입니다! 사거리 내에서 공격해보세요.")
