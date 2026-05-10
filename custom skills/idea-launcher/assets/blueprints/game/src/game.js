const canvas = document.querySelector("#game");
const context = canvas.getContext("2d");
const restart = document.querySelector("#restart");

const state = {
  playerX: 480,
  score: 0,
  signalY: 40,
  running: true
};

function reset() {
  state.playerX = 480;
  state.score = 0;
  state.signalY = 40;
  state.running = true;
}

function draw() {
  context.fillStyle = "#111315";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = "#f0d36b";
  context.fillRect(state.playerX - 48, 460, 96, 18);
  context.fillStyle = "#65c3c8";
  context.beginPath();
  context.arc(480, state.signalY, 18, 0, Math.PI * 2);
  context.fill();
  context.fillStyle = "#fff";
  context.font = "20px system-ui";
  context.fillText(`Score ${state.score}`, 24, 36);
  context.fillText("Move with arrow keys. Catch the signal.", 24, 66);
}

function update() {
  state.signalY += 3;
  if (state.signalY > 460 && Math.abs(state.playerX - 480) < 64) {
    state.score += 1;
    state.signalY = 40;
  }
  if (state.signalY > canvas.height + 30) {
    state.signalY = 40;
  }
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

window.addEventListener("keydown", (event) => {
  if (event.key === "ArrowLeft") state.playerX = Math.max(60, state.playerX - 32);
  if (event.key === "ArrowRight") state.playerX = Math.min(canvas.width - 60, state.playerX + 32);
});

restart.addEventListener("click", reset);
loop();
