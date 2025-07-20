import streamlit as st
import random
import json
import os

# Configure the page
st.set_page_config(
    page_title="💌 Love Bubble 💌",
    page_icon="💕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #ffeef8 0%, #ffe0f0 25%, #ffd4e8 50%, #ffb3d9 100%);
    }
    
    .love-note-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 30px;
        border-radius: 25px;
        border: 3px solid #ffb3d9;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(214, 51, 132, 0.2);
    }
    
    .love-note-text {
        font-size: 1.4em;
        color: #8e44ad;
        font-weight: 600;
        line-height: 1.6;
        margin: 0;
    }
    
    .header-text {
        text-align: center;
        color: #d63384;
        font-size: 3em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(214, 51, 132, 0.3);
    }
    
    .subtitle-text {
        text-align: center;
        color: #8e44ad;
        font-size: 1.2em;
        margin-bottom: 30px;
        opacity: 0.8;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff6b9d, #d63384);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 1.2em;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 5px 15px rgba(214, 51, 132, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #d63384, #ff6b9d);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(214, 51, 132, 0.6);
    }
    
    .stTextArea > div > div > textarea {
        border: 2px solid #ffb3d9;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.9);
        font-size: 1.1em;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #d63384;
        box-shadow: 0 0 10px rgba(214, 51, 132, 0.3);
    }
    
    .notes-count {
        text-align: center;
        color: #8e44ad;
        font-size: 1em;
        margin-top: 20px;
        opacity: 0.8;
    }
    
    .success-message {
        background: linear-gradient(45deg, #ff9a9e, #fecfef);
        color: #8e44ad;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
        border: 2px solid #ffb3d9;
    }
</style>
""", unsafe_allow_html=True)

# Love notes data
DEFAULT_LOVE_NOTES = [
    "you make even the boring moments feel like actual magic hmp 💗",
    "my heart goes all badum badum every time i see you dummy 💓",
    "YOU'RE literally the best part of every single day ever ✨",
    "i'm so so SOOO lucky to have you like FR how did i even get you 🍀",
    "your smile makes everything else disappear like WHO gave you permission 😊",
    "i fall harder every day and it's NOT FAIR stop being so cute 💕",
    "you're the reason i believe in those dumb fairy tale love stories now 📚",
    "my fav place is literally just wherever YOU are hm 🏡",
    "you turn my gray sky heart into a whole rainbow and now i'm soft 🌈",
    "i choose you always ALWAYS even when you're mean to me 💍",
    "you're my home my person my little EVERYTHINGGG 🏠",
    "with you it's just… forever vibes and my chest gets all warm 🌟",
    "you make me wanna be soft and good and better like why ✨",
    "i love the way your eyes see stuff like suddenly everything's pretty 👀",
    "you're the sunshine when i wanna cry into my pillow ☀️",
    "my heart is LOCKED and you're the only one who gets the key 🔐",
    "suddenly all love songs are about you and i HATE IT (but not really) 🎶",
    "your sleepy voice in the morning makes me go all fuzzy inside 🌅",
    "you're my fav notification and i'd ignore the whole world for u 📱",
    "the way you make me laugh till i'm wheezing STOPPPP 😂",
    "you smell like home and comfort and i'm gonna sob 🌸",
    "when you scrunch your nose while thinking??? I'M GONE 🤔",
    "you're my fav adventure i'd get lost with you every time 🗺️",
    "your weird 3am thoughts make me giggle like a fool 🌙",
    "my heart does little flippy things when you look at me like that 🎪",
    "the way you get excited over tiny things makes me wanna squish u ✨",
    "you're the safest softest place in the entire universe HMP 🕊️",
    "you hum when you're happy and i fall in love all over again 🎵",
    "you make me believe in magic and now i'm stuck forever 🪄",
    "your dumb dad jokes shouldn't make me laugh BUT THEY DO 😄",
    "you're my fav kind of chaos and i wouldn't change a thing 😈",
    "you somehow always know what i need and i hate itttt (no i don't) 💝",
    "time goes fast and slow with you and i'm just?? lost in you?? ⏰",
    "your messy morning hair makes me want to bury my face in ur neck 💁‍♀️",
    "you're literally the biggest blessing and i didn't even see u coming 🙏",
    "you make tuesdays feel like date nights i didn't plan but love 📅",
    "you're the plot twist that made everything better i swear 📖",
    "you see the world in a way that makes me fall harder every time 🔮",
    "you make my heart feel all full and dumb and i LOVE IT 💓",
    "i saw you dancing alone and now i'm giggling into my sleeves 💃",
    "you're my fav distraction and i don't even wanna focus on anything else 📚",
    "your goodnight texts make me feel like the safest lil thing ever 🌙",
    "you make me wanna write cheesy poetry and blush at my own words 📝",
    "you steal my hoodies and somehow make them look cuter on u 👕",
    "you're my comfy place always always and forever hmp 🏖️",
    "your 2am random facts are so dumb and so YOU i can't stop smiling 🧠",
    "you make every boring day feel like a birthday party or smth 🎉",
    "you make me feel brave and soft and clingy at the same time 🦁",
    "you're the hello that makes me melt and the goodbye that breaks me 👋",
    "your heart is so soft it makes my chest ache and my brain go fuzzy 💖",
    "life with you feels like a dream i never wanna wake up from 💭",
    "you remember the tiniest things about me and i'm just like… HOW 🧩",
    "you're the missing puzzle piece and now i'm whole or whatever 🧩",
    "your smile is illegal and your joy makes me dizzy 🌻",
    "you make me feel like i can do anything and that's terrifying 🌍",
    "your hugs are actual therapy and i need one every five minutes 🤗",
    "you're my fav person to just lay around and do NOTHING with 🛋️",
    "you understand me better than i do and that's wild hmp 💫",
    "you're the biggest adventure and i'm diving in headfirst 🎢",
    "your sleepy cuddles are too powerful i literally malfunction 😴",
    "you make my heart speed up and calm down all at once i hate it here 💗",
    "you believe in my dreams more than i do and now i'm crying 🌟",
    "you're my fav love story and i never want it to end 💕",
    "you talking at midnight is like a lullaby for my anxious little brain 🌙",
    "you make me feel like the luckiest dumb baby in the world 🍀",
    "you make me feel cute and loved and safe and i'm not okay 👸",
    "you're my forever and my always and YES i'm gonna be annoyingly clingy about it 💍"
]

# Initialize session state
if 'love_notes' not in st.session_state:
    st.session_state.love_notes = DEFAULT_LOVE_NOTES.copy()
if 'current_note' not in st.session_state:
    st.session_state.current_note = "Click the button below to see a love note! 💕"
if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# Header
st.markdown('<h1 class="header-text">💌 Love Bubble 💌</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">A jar full of sweet memories and love notes ✨</p>', unsafe_allow_html=True)

# Current love note display
st.markdown(f'''
<div class="love-note-container">
    <p class="love-note-text">{st.session_state.current_note}</p>
</div>
''', unsafe_allow_html=True)

# Surprise button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("💖 Surprise Me! 💖", key="surprise_btn", use_container_width=True):
        if st.session_state.love_notes:
            st.session_state.current_note = random.choice(st.session_state.love_notes)
            st.rerun()
        else:
            st.session_state.current_note = "Add some love notes first! 💕"
            st.rerun()

st.markdown("---")

# Add new note section
st.markdown("### 💝 Add Your Own Love Note")

# Text area for new note
new_note = st.text_area(
    "",
    placeholder="Write a sweet message... 💗",
    max_chars=200,
    height=100,
    key="note_input"
)

# Add note button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("✨ Add Note ✨", key="add_btn", use_container_width=True):
        if new_note.strip():
            st.session_state.love_notes.append(new_note.strip())
            st.session_state.show_success = True
            # Clear the text area by rerunning
            st.rerun()
        else:
            st.error("Please write a love note first! 💗")

# Show success message
if st.session_state.show_success:
    st.markdown('''
    <div class="success-message">
        💕 Love note added successfully! 💕
    </div>
    ''', unsafe_allow_html=True)
    st.session_state.show_success = False

# Notes count
st.markdown(f'''
<div class="notes-count">
    💖 {len(st.session_state.love_notes)} love notes in your bubble 💖
</div>
''', unsafe_allow_html=True)

# Floating hearts effect (using emojis in sidebar)
with st.sidebar:
    st.markdown("### 💕")
    for i in range(10):
        st.markdown("💗" if i % 2 == 0 else "💕")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #8e44ad; opacity: 0.6; margin-top: 30px;">'
    'Made with 💕 for someone special</p>', 
    unsafe_allow_html=True
)
import streamlit.components.v1 as components

st.markdown("---")
st.markdown("### ✂️ Heart Slicer Mini Game ✂️")
st.markdown("Slice the falling hearts—but don't slice the beating ones or... DEAD HA")

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  canvas {
    border: 4px solid #ffb3d9;
    background: linear-gradient(to bottom, #ffeef8, #ffd4e8);
    border-radius: 15px;
    touch-action: none;
  }
  #message {
    text-align: center;
    font-size: 16px;
    color: #d63384;
    font-weight: bold;
    margin-top: 10px;
    min-height: 30px;
  }
  #retryBtn {
    display: none;
    background: linear-gradient(45deg, #ff6b9d, #d63384);
    border: none;
    color: white;
    font-size: 16px;
    font-weight: bold;
    padding: 10px 20px;
    border-radius: 25px;
    margin: 10px auto;
    display: block;
    cursor: pointer;
  }
</style>
</head>
<body>
<div style="text-align:center;">
  <canvas id="sliceCanvas" width="350" height="500"></canvas>
  <div id="message"></div>
  <button id="retryBtn">🔁 Retry</button>
</div>

<script>
const canvas = document.getElementById("sliceCanvas");
const ctx = canvas.getContext("2d");

let hearts = [];
let gameOver = false;
let score = 0;
let frameCount = 0;
const SPAWN_INTERVAL = 60;
const HEART_OPTIONS = ["💗", "💚", "💙", "💛", "🖤", "💜", "🤍", "🧡"];

const messageBox = document.getElementById("message");
const retryBtn = document.getElementById("retryBtn");

function spawnHeart() {
  const x = Math.random() * (canvas.width - 40);
  const emoji = HEART_OPTIONS[Math.floor(Math.random() * HEART_OPTIONS.length)];
  const isBomb = Math.random() < 0.2; // 20% chance it's a bomb, even if it looks cute
  hearts.push({
    x: x,
    y: -40,
    baseSize: 32,
    size: 32,
    scaleDirection: 1,
    emoji: emoji,
    isBomb: isBomb,
    sliced: false
  });
}

function drawHearts() {
  hearts.forEach(h => {
    if (h.isBomb) {
      // Pulsing animation
      if (h.scaleDirection === 1) {
        h.size += 0.2;
        if (h.size > h.baseSize + 3) h.scaleDirection = -1;
      } else {
        h.size -= 0.2;
        if (h.size < h.baseSize - 2) h.scaleDirection = 1;
      }
    } else {
      h.size = h.baseSize;
    }
    ctx.font = `${h.size}px serif`;
    ctx.fillText(h.emoji, h.x, h.y);
  });
}

function updateHearts() {
  for (let i = hearts.length - 1; i >= 0; i--) {
    hearts[i].y += 2.5;
    if (hearts[i].y > canvas.height) {
      hearts.splice(i, 1);
    }
  }
}

function drawSliceMark(x, y) {
  ctx.strokeStyle = "#d63384";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(x - 10, y - 10);
  ctx.lineTo(x + 10, y + 10);
  ctx.moveTo(x + 10, y - 10);
  ctx.lineTo(x - 10, y + 10);
  ctx.stroke();
}

function showMessage(msg, color="#d63384") {
  messageBox.style.color = color;
  messageBox.innerText = msg;
}

function endGame() {
  gameOver = true;
  retryBtn.style.display = "block";
}

function checkSlice(x, y) {
  for (let i = 0; i < hearts.length; i++) {
    const h = hearts[i];
    if (!h.sliced &&
        x >= h.x && x <= h.x + h.size &&
        y >= h.y - h.size && y <= h.y) {
      h.sliced = true;
      drawSliceMark(x, y);
      if (h.isBomb) {
        showMessage("WAAAWWW SO U HATE ME HUH BREAKING MY HEART IC IC HMP GAME OVER 💥💔", "#ff0033");
        endGame();
      } else {
        showMessage("AWH LOOK AT MY BABY DUMMY SO ADORBALE AN AMAZING 💕🥹");
        score += 1;
      }
      hearts.splice(i, 1);
      break;
    }
  }
}

canvas.addEventListener("mousemove", (e) => {
  if (!gameOver) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    checkSlice(x, y);
  }
});

canvas.addEventListener("touchmove", (e) => {
  if (!gameOver) {
    const rect = canvas.getBoundingClientRect();
    const touch = e.touches[0];
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    checkSlice(x, y);
  }
}, { passive: false });

retryBtn.onclick = () => {
  gameOver = false;
  score = 0;
  frameCount = 0;
  hearts = [];
  messageBox.innerText = "";
  retryBtn.style.display = "none";
  gameLoop();
};

function drawScore() {
  ctx.fillStyle = "#8e44ad";
  ctx.font = "18px sans-serif";
  ctx.fillText("Score: " + score, 10, 25);
}

function gameLoop() {
  if (gameOver) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (frameCount % SPAWN_INTERVAL === 0) spawnHeart();
  updateHearts();
  drawHearts();
  drawScore();
  frameCount++;
  requestAnimationFrame(gameLoop);
}

gameLoop();
</script>
</body>
</html>
""", height=640)
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Piano Tiles: Premium Edition</title>
  <style>
    body {
      margin: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      font-family: 'Arial', sans-serif;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;
      touch-action: manipulation;
      user-select: none;
      -webkit-user-select: none;
    }
    #gameContainer {
      position: relative;
      width: 340px;
      height: 620px;
      background: linear-gradient(180deg, rgba(255,255,255,0.97) 0%, rgba(240,240,255,0.92) 100%);
      border: 3px solid #4a5568;
      border-radius: 15px;
      overflow: hidden;
      box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    .lane {
      position: absolute;
      width: 25%;
      height: 100%;
      background: transparent;
      cursor: pointer;
      z-index: 1;
      border-right: 1px solid #cbd5e0;
      transition: background 0.15s;
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }
    .lane:active,
    .lane.pressed {
      background: rgba(34, 77, 184, 0.16);
    }
    .lane:last-child { border-right: none; }
    .tile {
      position: absolute;
      width: 92%;
      left: 4%;
      height: 110px;
      background: linear-gradient(150deg, #1a202c 85%, #2d3748 100%);
      border: 1.5px solid #4a5568;
      border-radius: 7px;
      box-shadow: 0 4px 11px rgba(0,0,0,0.25);
      cursor: pointer;
      transition: box-shadow 0.11s;
      z-index: 3;
      display: flex;
      align-items: end;
      justify-content: center;
      font-size: 19px;
      color: #fff;
      font-weight: 700;
      user-select: none;
    }
    .tile.hit {
      background: linear-gradient(145deg, #4fd1c5 60%, #38a169 100%);
      border-color: #48bb78;
      box-shadow: 0 0 22px #48bb78bb;
      animation: scalehit 0.3s;
    }
    @keyframes scalehit {
      0% { transform: scale(1.0);}
      50% { transform: scale(0.93);}
      100% { transform: scale(1.0);}
    }
    .tile.missed {
      background: linear-gradient(150deg, #e53e3e, #c53030);
      border-color: #c53030;
      animation: shake 0.25s;
    }
    @keyframes shake {
      0%,100%{transform:translateX(0);}
      30%{transform:translateX(-5px);}
      60%{transform:translateX(5px);}
    }
    .hit-zone {
      position: absolute;
      bottom: 95px;
      width: 100%;
      height: 110px;
      background: linear-gradient(to top, rgba(46, 98, 234, 0.09), transparent);
      border-top: 2px solid #667eea;
      border-bottom: 2px solid #38a169;
      pointer-events: none;
      z-index: 10;
    }
    #ui {
      position: absolute;
      top: 9px;
      left: 10px;
      right: 10px;
      display: flex;
      justify-content: space-between;
      color: #4a5568;
      background: rgba(255,255,255,0.93);
      border-radius: 8px;
      font-size: 15px;
      line-height: 1;
      font-weight: bold;
      z-index: 20;
      padding: 7px 12px 4px 12px;
    }
    .score-text {
      position: absolute;
      font-size: 20px;
      font-weight: 900;
      color: #48bb78;
      pointer-events: none;
      z-index: 100;
      left: 51%;
      top: 35%;
      animation: scoreFloat 0.9s ease-out forwards;
      transform: translate(-50%, -50%);
      text-shadow: 0 2px 12px #41e79c99;
    }
    @keyframes scoreFloat {
      0% { opacity: 1; transform: translate(-50%, -50%) scale(1.1);}
      100% { opacity: 0; transform: translate(-50%, -158%) scale(1.23);}
    }
    #message {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      min-width: 220px;
      min-height: 110px;
      text-align: center;
      color: #394664;
      font-weight: bold;
      font-size: 18px;
      background: rgba(245,250,255,0.98);
      border-radius: 17px;
      box-shadow: 0 8px 24px #6276be44;
      z-index: 200;
      padding: 22px 14px;
      display: none;
    }
    #startBtn, #pauseBtn, #retryBtn, #muteBtn {
      background: linear-gradient(45deg, #667eea, #764ba2);
      border: none;
      color: white;
      font-size: 16px;
      font-weight: bold;
      padding: 9px 18px;
      border-radius: 19px;
      margin: 8px 4px 2px 4px;
      cursor: pointer;
      transition: box-shadow 0.2s, transform 0.18s;
    }
    #startBtn:hover, #pauseBtn:hover, #retryBtn:hover, #muteBtn:hover {
      box-shadow: 0 5px 13px #667eea99;
      transform: translateY(-2px);
    }
    #muteBtn.on { background: linear-gradient(45deg, #48bb78, #38a169);}
    .lane-indicator {
      position: absolute;
      width: 50px;
      bottom: 8px;
      left: 0;
      right: 0;
      margin: auto;
      color: #764ba2d0;
      font-weight: bold;
      opacity: 0.48;
      pointer-events: none;
      text-align: center;
      user-select: none;
    }
    .lane[data-lane="0"] .lane-indicator { content: "A"; }
    .lane[data-lane="1"] .lane-indicator { content: "S"; }
    .lane[data-lane="2"] .lane-indicator { content: "D"; }
    .lane[data-lane="3"] .lane-indicator { content: "F"; }
    @media (max-width: 400px) {
      #gameContainer { width: 100vw; height: 100vh; min-width: 90vw; min-height: 95vh;}
    }
  </style>
</head>
<body>
  <div id="gameContainer">
    <div class="lane" data-lane="0"><div class="lane-indicator">A</div></div>
    <div class="lane" data-lane="1"><div class="lane-indicator">S</div></div>
    <div class="lane" data-lane="2"><div class="lane-indicator">D</div></div>
    <div class="lane" data-lane="3"><div class="lane-indicator">F</div></div>
    <div class="hit-zone"></div>
    <div id="ui">
      <div>🎼 <span>Score: </span><span id="score">0</span></div>
      <div>💗 <span>Lives: </span><span id="lives">3</span></div>
      <div>🎵 <span>Combo: </span><span id="streak">0</span></div>
      <div>📈 <span>Lvl: </span><span id="level">1</span></div>
      <button id="muteBtn" title="Mute/Unmute Music">🔊</button>
    </div>
    <div id="message">
      <div style="font-size: 20px;">🎹 Piano Tiles: Tap Edition 🎹</div>
      <div style="font-size: 14px; margin: 10px 0;">Tap / Click the black tiles in the hit zone!</div>
      <div style="font-size: 12px; margin-bottom: 14px;">Use: A, S, D, F (keyboard or touch!)</div>
      <button id="startBtn">🎵 Start Game</button>
      <button id="pauseBtn" style="display:none;">⏸️ Pause</button>
      <button id="retryBtn" style="display:none;">🔁 Retry</button>
    </div>
  </div>
  <audio id="soundHit" src="https://cdn.pixabay.com/audio/2022/12/19/audio_12f170b7c3.mp3"></audio>
  <audio id="soundMiss" src="https://cdn.pixabay.com/audio/2022/12/19/audio_c8b4612ca2.mp3"></audio>
  <audio id="bgMusic" src="https://cdn.pixabay.com/audio/2023/05/30/audio_145f3674fa.mp3" loop></audio>
  <script>
    // --- GAME VARIABLES ---
    let score = 0, lives = 3, streak = 0, maxStreak = 0, level = 1;
    let gameActive = false, gamePaused = false, animationId = null;
    let tileSpeed = 2.8, minTileSpeed = 2, maxTileSpeed = 8, spawnRate = 1100, lastSpawnTime = 0;
    let tiles = [];
    const hitZoneStart = 415, hitZoneEnd = 525; // y px
    const keysMap = { 'KeyA':0, 'KeyS':1, 'KeyD':2, 'KeyF':3 };
    // --- DOM ---
    const gameContainer = document.getElementById('gameContainer');
    const scoreEl = document.getElementById('score');
    const livesEl = document.getElementById('lives');
    const streakEl = document.getElementById('streak');
    const levelEl = document.getElementById('level');
    const messageEl = document.getElementById('message');
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const retryBtn = document.getElementById('retryBtn');
    const muteBtn = document.getElementById('muteBtn');
    const bgMusic = document.getElementById('bgMusic');
    const soundHit = document.getElementById('soundHit');
    const soundMiss = document.getElementById('soundMiss');
    // --- AUDIO MUTE ---
    let globalMute = false;
    muteBtn.addEventListener('click', () => {
      globalMute = !globalMute;
      bgMusic.muted = soundHit.muted = soundMiss.muted = globalMute;
      muteBtn.textContent = globalMute ? "🔈" : "🔊";
      muteBtn.className = globalMute ? "on":"";
    });
    // --- UI UPDATE ---
    function updateUI() {
      scoreEl.textContent = score;
      livesEl.textContent = lives;
      streakEl.textContent = streak;
      levelEl.textContent = level;
    }
    function showScoreText(points, emoji="") {
      const txt = document.createElement('div');
      txt.className = 'score-text';
      txt.textContent = `${emoji}+${points}`;
      gameContainer.appendChild(txt);
      setTimeout(()=>txt.remove(),900);
    }
    // --- TILE LOGIC ---
    function createTile(laneIndex) {
      const tile = document.createElement('div');
      tile.className = 'tile';
      tile.style.left = `${laneIndex*25+4}%`;
      tile.style.top = `-115px`;
      tile.dataset.lane = laneIndex;
      gameContainer.appendChild(tile);
      tiles.push({
        element: tile,
        lane: laneIndex,
        y: -115,
        hit: false,
        missed: false,
      });
      // Optional: Lane sound per tile (uncomment lines and add real piano sounds!)
      // tile.dataset.soundUrl = perLanePianoSounds[laneIndex];
    }
    function spawnNewTile() {
      const recentLanes = tiles.slice(-3).map(t=>t.lane);
      let available = [0,1,2,3].filter(l=>!recentLanes.includes(l));
      if(available.length===0) available = [0,1,2,3];
      const idx = available[Math.floor(Math.random()*available.length)];
      createTile(idx);
    }
    // --- GAME UPDATE LOOP ---
    function updateGame() {
      if (!gameActive || gamePaused) return;
      tiles.forEach(tile => {
        if(tile.hit||tile.missed) return;
        tile.y += tileSpeed;
        tile.element.style.top = tile.y+"px";
        // Missed: if passes hit zone bottom w/o being hit
        if(tile.y > hitZoneEnd+35 && !tile.hit && !tile.missed) {
          tile.missed = true;
          tile.element.classList.add('missed');
          lives--; streak = 0;
          updateUI();
          if(!globalMute) soundMiss.cloneNode().play();
          setTimeout(()=>{ if(tile.element) tile.element.remove(); },350);
          if(lives<=0) endGame();
        }
      });
      // Remove offscreen tiles
      tiles = tiles.filter(t => t.y < 710 && !t.missed || !t.hit);
      // Spawning
      const now = Date.now();
      if (now-lastSpawnTime >= spawnRate) {
        spawnNewTile(); lastSpawnTime = now;
      }
      animationId = requestAnimationFrame(updateGame);
    }
    // --- INPUT HANDLERS ---
    function tryHitTile(lane) {
      if(!gameActive||gamePaused) return;
      // Find FIRST available tile in this lane in hit zone
      const tl = tiles.find(tile =>
        !tile.hit && !tile.missed && tile.lane===lane &&
        tile.y >= hitZoneStart && tile.y <= hitZoneEnd
      );
      if (tl) {
        tl.hit = true; streak++; maxStreak = Math.max(maxStreak,streak);
        score += 150 + (streak>1 ? streak*8 : 0);
        updateUI();
        tl.element.classList.add("hit");
        if(!globalMute) soundHit.cloneNode().play();
        showScoreText(150+(streak>1?streak*8:0),"🎵");
        setTimeout(()=>{ if(tl.element) tl.element.remove(); },260);
        // Level up
        if(score>=level*800) { levelUp(); }
        return true;
      } else {
        // Missed: wrong tap
        lives--; streak=0;
        updateUI();
        if(!globalMute) soundMiss.cloneNode().play();
        showScoreText(0,"😐");
        if(lives<=0) endGame();
        return false;
      }
    }
    // Lane tap (mouse/touch)
    document.querySelectorAll('.lane').forEach((laneEl, i) => {
      // Touch/click
      laneEl.addEventListener("mousedown", e=>{
        e.preventDefault(); tryHitTile(i);
        laneEl.classList.add("pressed"); setTimeout(()=>laneEl.classList.remove("pressed"),180);
      });
      laneEl.addEventListener("touchstart", e=>{
        e.preventDefault(); tryHitTile(i);
        laneEl.classList.add("pressed"); setTimeout(()=>laneEl.classList.remove("pressed"),180);
      });
    });
    // Lane tap (key)
    document.addEventListener('keydown', function(e) {
      if (!gameActive||gamePaused) return;
      if (e.repeat) return;
      let idx = keysMap[e.code];
      if(typeof idx==="number") {
        document.querySelector(`.lane[data-lane="${idx}"]`).classList.add("pressed");
        tryHitTile(idx);
      } else if(e.code==="Space") {
        pauseGame();
      }
    });
    document.addEventListener('keyup', function(e){
      let idx = keysMap[e.code];
      if(typeof idx==="number") {
        document.querySelector(`.lane[data-lane="${idx}"]`).classList.remove("pressed");
      }
    });
    // Global: clear pressed on mouseup/touchup
    document.addEventListener('mouseup', ()=> {
      document.querySelectorAll('.lane').forEach(l=>l.classList.remove("pressed"));
    });
    // --- LEVEL UP ---
    function levelUp() {
      level++;
      tileSpeed = Math.min(maxTileSpeed, tileSpeed+0.37);
      spawnRate = Math.max(410, spawnRate-60);
      showMessage(`🎉 Level ${level}! 🎉<br>Tiles move faster!`,1400);
    }
    // --- MESSAGE UI ---
    function showMessage(msg,duration=0) {
      messageEl.innerHTML = msg;
      messageEl.style.display = 'block';
      if(duration) setTimeout(()=>{if(gameActive)messageEl.style.display="none";},duration);
    }
    // --- MAIN GAME STATE ---
    function startGame(){
      score = 0; streak=0; maxStreak=0; lives=3; level=1;
      tileSpeed = minTileSpeed; spawnRate = 1100;
      gameActive = true; gamePaused=false; tiles.forEach(t=>t.element.remove()); tiles=[];
      lastSpawnTime = Date.now(); updateUI();
      messageEl.style.display='none'; startBtn.style.display="none";
      pauseBtn.style.display="inline-block"; retryBtn.style.display="none";
      if(!globalMute) setTimeout(()=>{bgMusic.play()},300);
      spawnNewTile();
      animationId = requestAnimationFrame(updateGame);
    }
    function pauseGame(){
      if(!gameActive) return;
      gamePaused = !gamePaused;
      if(gamePaused) {
        pauseBtn.textContent="▶️ Resume";
        showMessage("Game Paused. Press Space or tap Pause to continue",0);
        if(!globalMute) bgMusic.pause();
      } else {
        pauseBtn.textContent="⏸️ Pause";
        messageEl.style.display="none";
        lastSpawnTime = Date.now();
        if(!globalMute) bgMusic.play();
        animationId = requestAnimationFrame(updateGame);
      }
    }
    function endGame(){
      gameActive=false; gamePaused=false; bgMusic.pause();
      if (animationId) cancelAnimationFrame(animationId);
      pauseBtn.style.display="none"; retryBtn.style.display="inline-block";
      let endings = [
        {score:2200, msg:"👑 MASTER PIANIST! Flawless! 👑"},
        {score:1200, msg:"🌟 AMAZING! Great rhythm! 🌟"},
        {score:700,  msg:"💕 Well played, keep going! 💕"},
        {score:350,  msg:"🎵 Good work! Try for more! 🎵"},
        {score:0,    msg:"💗 Nice try! Practice makes perfect! 💗"}
      ];
      let endMsg = endings.find(e=>score>=e.score).msg;
      showMessage(
        `<div style="font-size:20px;">🎹 Game Over! 🎹</div>
         <div style="margin:10px 0;">Score: ${score}</div>
         <div style="margin:10px 0;">Max Streak: ${maxStreak}</div>
         <div style="margin:10px 0;">Level: ${level}</div>
         <div style="font-size:14px; margin:10px 0;">${endMsg}</div>`,0
      );
    }
    // --- BUTTONS ---
    startBtn.addEventListener('click',startGame);
    pauseBtn.addEventListener('click',pauseGame);
    retryBtn.addEventListener('click',startGame);
    document.getElementById('gameContainer').addEventListener('contextmenu',e=>e.preventDefault());
    // --- INIT SHOW MESSAGE ---
    showMessage(
      `<div style="font-size:20px;">🎹 Piano Tiles: Tap Edition 🎹</div>
      <div style="font-size:14px; margin:10px 0;">Tap / Click the black tiles in the hit zone!</div>
      <div style="font-size:12px; margin-bottom:15px;">A, S, D, F / Tap / Click / Touch</div>`,0
    );
    // --- Responsive ---
    window.addEventListener("blur",()=>{ if(gameActive&&!gamePaused) pauseGame(); });
    // --- Music play on interaction (Mobile) ---
    document.body.addEventListener("touchstart",()=>{ if(gameActive&&!bgMusic.paused&&!globalMute) bgMusic.play(); },{once:true});
  </script>
</body>
</html>
