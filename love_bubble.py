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
st.markdown("Slice the falling hearts—but don't slice the beating ones or... 💥💀")

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
st.markdown("---")
st.markdown("### 💘 Dreamy Rhythm 💘")
st.markdown("A soft lo-fi rhythm game where you tap floating tiles to the beat 🎼✨")

# YouTube URL input for the rhythm game
youtube_url = st.text_input("🎵 Paste YouTube URL (audio only):", placeholder="https://www.youtube.com/watch?v=...")

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{ 
    margin: 0; 
    background: linear-gradient(135deg, #ffeef8 0%, #ffe0f0 25%, #ffd4e8 50%, #ffb3d9 100%);
    font-family: 'Arial', sans-serif;
    overflow: hidden;
  }}
  
  #gameContainer {{
    position: relative;
    width: 400px;
    height: 500px;
    margin: 0 auto;
    background: linear-gradient(180deg, rgba(255,255,255,0.1) 0%, rgba(255,179,217,0.2) 100%);
    border: 3px solid #ffb3d9;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(214, 51, 132, 0.2);
  }}
  
  .lane {{
    position: absolute;
    width: 25%;
    height: 100%;
    border-right: 2px solid rgba(255,179,217,0.3);
    background: linear-gradient(180deg, transparent 0%, rgba(255,255,255,0.05) 100%);
  }}
  
  .lane:last-child {{ border-right: none; }}
  
  .tile {{
    position: absolute;
    width: 90%;
    height: 60px;
    left: 5%;
    background: linear-gradient(145deg, #ff6b9d, #d63384);
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(214, 51, 132, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
    transition: all 0.2s ease;
    cursor: pointer;
  }}
  
  .tile.long-hold {{
    height: 120px;
    background: linear-gradient(145deg, #ff9a9e, #fecfef);
    border: 3px solid #d63384;
  }}
  
  .tile:hover {{
    transform: scale(1.05);
    box-shadow: 0 8px 25px rgba(214, 51, 132, 0.6);
  }}
  
  .tile.hit {{
    transform: scale(1.2);
    background: linear-gradient(145deg, #ffd700, #ffb347);
    animation: sparkle 0.3s ease-out;
  }}
  
  @keyframes sparkle {{
    0% {{ transform: scale(1.2) rotate(0deg); }}
    50% {{ transform: scale(1.4) rotate(180deg); }}
    100% {{ transform: scale(1.2) rotate(360deg); }}
  }}
  
  .floating-heart {{
    position: absolute;
    font-size: 20px;
    opacity: 0.6;
    animation: float 4s ease-in-out infinite;
    pointer-events: none;
  }}
  
  @keyframes float {{
    0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-20px) rotate(180deg); }}
  }}
  
  #ui {{
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    display: flex;
    justify-content: space-between;
    color: #8e44ad;
    font-weight: bold;
    z-index: 100;
  }}
  
  #message {{
    position: absolute;
    bottom: 20px;
    left: 20px;
    right: 20px;
    text-align: center;
    color: #d63384;
    font-weight: bold;
    font-size: 14px;
    min-height: 40px;
    background: rgba(255,255,255,0.8);
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 5px 15px rgba(214, 51, 132, 0.2);
  }}
  
  #retryBtn {{
    background: linear-gradient(45deg, #ff6b9d, #d63384);
    border: none;
    color: white;
    font-size: 16px;
    font-weight: bold;
    padding: 10px 20px;
    border-radius: 25px;
    margin-top: 10px;
    cursor: pointer;
    display: none;
  }}
  
  .cracked-heart {{
    position: absolute;
    font-size: 30px;
    color: #ff4757;
    animation: crack 1s ease-out;
  }}
  
  @keyframes crack {{
    0% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
    50% {{ transform: scale(1.2) rotate(-10deg); }}
    100% {{ transform: scale(0.8) rotate(10deg); opacity: 0; }}
  }}
</style>
</head>
<body>
<div id="gameContainer">
  <div class="lane" style="left: 0%;"></div>
  <div class="lane" style="left: 25%;"></div>
  <div class="lane" style="left: 50%;"></div>
  <div class="lane" style="left: 75%;"></div>
  
  <div id="ui">
    <div>✨ <span id="score">0</span></div>
    <div>💗 <span id="hearts">3</span></div>
    <div>🎵 <span id="streak">0</span></div>
  </div>
  
  <div id="message">Ready to feel the rhythm? 💕</div>
  <button id="retryBtn">🔁 Wanna retry?</button>
</div>

<script>
const gameContainer = document.getElementById('gameContainer');
const scoreEl = document.getElementById('score');
const heartsEl = document.getElementById('hearts');
const streakEl = document.getElementById('streak');
const messageEl = document.getElementById('message');
const retryBtn = document.getElementById('retryBtn');

let score = 0;
let hearts = 3;
let streak = 0;
let gameActive = true;
let tiles = [];
let floatingHearts = [];

// Sample beat map for "Our Start" (you can expand this)
const beatMap = [
  {{time: 1000, lane: 0, type: 'tap'}},
  {{time: 1500, lane: 2, type: 'tap'}},
  {{time: 2000, lane: 1, type: 'hold', duration: 1000}},
  {{time: 3200, lane: 3, type: 'tap'}},
  {{time: 3700, lane: 0, type: 'tap'}},
  {{time: 4200, lane: 2, type: 'tap'}},
  {{time: 5000, lane: 1, type: 'hold', duration: 800}},
  {{time: 6000, lane: 3, type: 'tap'}},
  {{time: 6500, lane: 0, type: 'tap'}},
  {{time: 7000, lane: 2, type: 'tap'}},
  {{time: 7500, lane: 1, type: 'tap'}},
  {{time: 8000, lane: 3, type: 'hold', duration: 1200}},
];

let gameStartTime = Date.now();
let currentBeatIndex = 0;

const compliments = [
  "Look at you, all smooth and synced. My lil maestro dummy 🎼💗",
  "Ooh someone's got rhythm! You're making my heart flutter 💕",
  "Perfect timing baby! You're in sync with my heartbeat ✨",
  "Awh you're so good at this! My talented little love 🥹💗",
  "Keep going! You're making beautiful music 🎵💕"
];

function createFloatingHeart() {{
  const heart = document.createElement('div');
  heart.className = 'floating-heart';
  heart.innerHTML = ['💗', '💕', '💖', '💝'][Math.floor(Math.random() * 4)];
  heart.style.left = Math.random() * 350 + 'px';
  heart.style.top = Math.random() * 450 + 'px';
  heart.style.animationDelay = Math.random() * 2 + 's';
  gameContainer.appendChild(heart);
  
  setTimeout(() => heart.remove(), 4000);
}}

function createTile(beat) {{
  const tile = document.createElement('div');
  tile.className = beat.type === 'hold' ? 'tile long-hold' : 'tile';
  tile.style.left = (beat.lane * 25) + '%';
  tile.style.top = '-70px';
  tile.innerHTML = beat.type === 'hold' ? '💖' : '💗';
  
  tile.dataset.lane = beat.lane;
  tile.dataset.type = beat.type;
  tile.dataset.duration = beat.duration || 0;
  tile.dataset.startTime = Date.now();
  
  gameContainer.appendChild(tile);
  tiles.push(tile);
  
  // Animate tile falling
  let position = -70;
  const fallInterval = setInterval(() => {{
    if (!gameActive) {{
      clearInterval(fallInterval);
      return;
    }}
    
    position += 3;
    tile.style.top = position + 'px';
    
    // Check if tile reached bottom without being hit
    if (position > 500) {{
      clearInterval(fallInterval);
      if (!tile.dataset.hit) {{
        missedTile();
      }}
      tile.remove();
      tiles = tiles.filter(t => t !== tile);
    }}
  }}, 16);
  
  // Add click handler
  tile.addEventListener('click', () => hitTile(tile));
}}

function hitTile(tile) {{
  if (tile.dataset.hit) return;
  
  tile.dataset.hit = 'true';
  tile.classList.add('hit');
  
  score += 10;
  streak++;
  scoreEl.textContent = score;
  streakEl.textContent = streak;
  
  // Show compliment on good streaks
  if (streak > 0 && streak % 5 === 0) {{
    const compliment = compliments[Math.floor(Math.random() * compliments.length)];
    messageEl.textContent = compliment;
    setTimeout(() => {{
      if (gameActive) messageEl.textContent = "Keep the rhythm flowing... 💕";
    }}, 2000);
  }}
  
  // Create sparkle effect
  for (let i = 0; i < 3; i++) {{
    setTimeout(() => createFloatingHeart(), i * 100);
  }}
}}

function missedTile() {{
  hearts--;
  heartsEl.textContent = hearts;
  streak = 0;
  streakEl.textContent = streak;
  
  // Create cracked heart
  const crackedHeart = document.createElement('div');
  crackedHeart.className = 'cracked-heart';
  crackedHeart.innerHTML = '💔';
  crackedHeart.style.left = Math.random() * 300 + 'px';
  crackedHeart.style.top = Math.random() * 400 + 200 + 'px';
  gameContainer.appendChild(crackedHeart);
  
  setTimeout(() => crackedHeart.remove(), 1000);
  
  if (hearts <= 0) {{
    endGame();
  }} else {{
    messageEl.textContent = "A little heart crack... but keep going! 💗";
  }}
}}

function endGame() {{
  gameActive = false;
  tiles.forEach(tile => tile.remove());
  tiles = [];
  
  messageEl.innerHTML = `
    You broke the rhythm… and maybe my heart. Hmp. 💔<br>
    <small>But that was our lil song... 💕</small>
  `;
  retryBtn.style.display = 'block';
}}

function startGame() {{
  gameActive = true;
  score = 0;
  hearts = 3;
  streak = 0;
  currentBeatIndex = 0;
  gameStartTime = Date.now();
  
  scoreEl.textContent = score;
  heartsEl.textContent = hearts;
  streakEl.textContent = streak;
  messageEl.textContent = "Feel the rhythm in your heart... 💕";
  retryBtn.style.display = 'none';
  
  // Start spawning tiles based on beat map
  function spawnNextTile() {{
    if (!gameActive || currentBeatIndex >= beatMap.length) return;
    
    const currentTime = Date.now() - gameStartTime;
    const nextBeat = beatMap[currentBeatIndex];
    
    if (currentTime >= nextBeat.time) {{
      createTile(nextBeat);
      currentBeatIndex++;
    }}
    
    if (currentBeatIndex < beatMap.length) {{
      setTimeout(spawnNextTile, 50);
    }} else {{
      // End game after last tile
      setTimeout(() => {{
        if (gameActive) {{
          messageEl.textContent = "Awh, that was our lil song… Wanna retry? 💕";
          retryBtn.style.display = 'block';
          gameActive = false;
        }}
      }}, 5000);
    }}
  }}
  
  spawnNextTile();
}}

// Add floating hearts in background
setInterval(() => {{
  if (gameActive) createFloatingHeart();
}}, 800);

retryBtn.addEventListener('click', startGame);

// Start the game
setTimeout(startGame, 1000);

// Add lane click handlers for mobile
document.querySelectorAll('.lane').forEach((lane, index) => {{
  lane.addEventListener('click', (e) => {{
    const rect = lane.getBoundingClientRect();
    const y = e.clientY - rect.top;
    
    // Find tile in this lane near click position
    const nearbyTile = tiles.find(tile => {{
      const tileRect = tile.getBoundingClientRect();
      const laneRect = lane.getBoundingClientRect();
      return parseInt(tile.dataset.lane) === index && 
             Math.abs(e.clientY - (tileRect.top + tileRect.height/2)) < 50;
    }});
    
    if (nearbyTile && !nearbyTile.dataset.hit) {{
      hitTile(nearbyTile);
    }}
  }});
}});
</script>
</body>
</html>
""", height=580)
