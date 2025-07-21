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
import streamlit.components.v1 as components

with open("bunny_platformer.html", 'r', encoding='utf-8') as f:
    html_code = f.read()

st.markdown("## 🐰 Bunny Platformer Game")
components.html(html_code, height=600, scrolling=False)

import streamlit as st
import streamlit.components.v1 as components

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  html, body {
    margin: 0;
    overflow: hidden;
    height: 100%;
    background: linear-gradient(to top, #ff9a9e, #fad0c4, #fad0c4);
  }

  #game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  }

  #game {
    position: absolute;
    width: 100%;
    height: 10000px; /* Enough height for scrolling upward */
    top: -9000px; /* Start close to the bottom */
  }

  .player {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    font-size: 40px;
  }

  .car {
    position: absolute;
    font-size: 32px;
    color: red;
  }

  #score {
    position: fixed;
    top: 10px;
    left: 10px;
    font-size: 20px;
    background: white;
    padding: 5px 15px;
    border-radius: 8px;
    z-index: 999;
  }

  #hearts {
    position: fixed;
    top: 10px;
    right: 10px;
    font-size: 24px;
    z-index: 999;
  }

  #fullscreen-btn {
    position: fixed;
    bottom: 10px;
    right: 10px;
    padding: 10px 20px;
    background: white;
    border-radius: 10px;
    border: none;
    font-size: 16px;
    cursor: pointer;
    z-index: 999;
  }
</style>
</head>
<body>
<div id="game-container">
  <div id="score">Score: 0</div>
  <div id="hearts">❤️❤️</div>
  <button id="fullscreen-btn">Fullscreen</button>
  <div id="game">
    <div id="player" class="player">🍓</div>
  </div>
</div>

<script>
  const player = document.getElementById("player");
  const game = document.getElementById("game");
  const scoreDisplay = document.getElementById("score");
  const heartsDisplay = document.getElementById("hearts");
  const gameContainer = document.getElementById("game-container");
  let posX = window.innerWidth / 2 - 20;
  let posY = 9900; // Start near the bottom of #game
  let score = 0;
  let lives = 2;
  let speed = 3;

  function updatePosition() {
    player.style.left = posX + "px";
    player.style.top = posY + "px";

    // Move camera with player if they go up
    if (posY < window.scrollY + 300) {
      window.scrollTo({ top: posY - 300, behavior: "smooth" });
    }
  }

  function endGame() {
    alert("Game Over! Final Score: " + score);
    location.reload();
  }

  document.getElementById("fullscreen-btn").onclick = () => {
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen();
    }
  };

  document.addEventListener("keydown", function(event) {
    if (event.key === "ArrowLeft") posX -= 40;
    if (event.key === "ArrowRight") posX += 40;
    if (event.key === "ArrowUp") {
      posY -= 40;
      score += 1;
      scoreDisplay.textContent = "Score: " + score;
    }
    if (event.key === "ArrowDown") {
      posY += 40;
    }

    // Prevent going off screen
    if (posX < 0) posX = 0;
    if (posX > window.innerWidth - 40) posX = window.innerWidth - 40;
    if (posY > 9950) posY = 9950; // Don't fall below floor

    updatePosition();
  });

  function createCar() {
    const car = document.createElement("div");
    car.classList.add("car");
    car.textContent = "💔";

    const direction = Math.floor(Math.random() * 4); // 0: left, 1: right, 2: top, 3: bottom
    let fromLeft = direction === 0;
    let fromRight = direction === 1;
    let fromTop = direction === 2;
    let fromBottom = direction === 3;

    const carY = posY - Math.random() * 500 + 250;

    if (fromLeft || fromRight) {
      car.style.top = carY + "px";
      car.style.left = fromLeft ? "-50px" : window.innerWidth + "px";
    } else {
      car.style.left = Math.random() * (window.innerWidth - 50) + "px";
      car.style.top = fromTop ? (carY - 400) + "px" : (carY + 400) + "px";
    }

    game.appendChild(car);

    let move = setInterval(() => {
      let cx = car.offsetLeft;
      let cy = car.offsetTop;

      if (fromLeft) car.style.left = (cx + speed) + "px";
      else if (fromRight) car.style.left = (cx - speed) + "px";
      else if (fromTop) car.style.top = (cy + speed) + "px";
      else if (fromBottom) car.style.top = (cy - speed) + "px";

      const px = player.offsetLeft;
      const py = player.offsetTop;

      if (
        Math.abs(px - car.offsetLeft) < 30 &&
        Math.abs(py - car.offsetTop) < 30
      ) {
        lives -= 1;
        heartsDisplay.innerText = "❤️".repeat(lives);
        car.remove();
        clearInterval(move);
        if (lives <= 0) endGame();
      }

      // Remove car if it's off screen
      if (
        cx < -100 || cx > window.innerWidth + 100 ||
        cy < posY - 1000 || cy > posY + 1000
      ) {
        car.remove();
        clearInterval(move);
      }
    }, 10);
  }

  setInterval(createCar, 1000);
  updatePosition();
</script>
</body>
</html>
"""

import streamlit as st
import random
import time

st.set_page_config(page_title="Emoji Color Match", layout="centered")

st.title("🎯 Emoji Color Reaction Game")

EMOJI_MAP = {
    "red": "❤️",
    "blue": "💙",
    "green": "💚",
    "yellow": "💛",
    "purple": "💜",
    "orange": "🧡"
}

original_colors = list(EMOJI_MAP.keys())

# Game state setup
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "target_color" not in st.session_state:
    st.session_state.target_color = None
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "shuffled_colors" not in st.session_state:
    st.session_state.shuffled_colors = random.sample(original_colors, len(original_colors))
if "clicked_color" not in st.session_state:
    st.session_state.clicked_color = None

with st.container():
    st.markdown("### 🕹️ How to Play:")
    st.markdown("- Click 'Start Game' to begin.")
    st.markdown("- Wait for the countdown (3...2...1...) and then select the correct heart emoji.")
    st.markdown("- The color order changes every round, so stay sharp! 🔁")
    st.divider()

    with st.container(border=True):
        if not st.session_state.game_started:
            if st.button("🚀 Start Game"):
                st.session_state.game_started = True
                st.session_state.target_color = random.choice(original_colors)
                st.session_state.reaction_time = None
                st.session_state.clicked_color = None
                st.session_state.shuffled_colors = random.sample(original_colors, len(original_colors))
                for i in range(3, 0, -1):
                    st.markdown(f"### ⏳ Get ready... {i}")
                    time.sleep(1)
                st.session_state.start_time = time.time()
                st.rerun()
        else:
            # If color has been clicked (from previous rerun)
            if st.session_state.clicked_color:
                end_time = time.time()
                st.session_state.reaction_time = round(end_time - st.session_state.start_time, 3)

                if st.session_state.clicked_color == st.session_state.target_color:
                    st.session_state.score += 1
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Wrong color!")

                st.session_state.clicked_color = None

            if st.session_state.reaction_time is None:
                st.markdown(f"### ✳️ Match This Color: **{st.session_state.target_color.upper()}**")

                cols = st.columns(len(EMOJI_MAP))
                for i, color in enumerate(st.session_state.shuffled_colors):
                    with cols[i]:
                        if st.button(EMOJI_MAP[color], key=color):
                            st.session_state.clicked_color = color
                            st.rerun()
            else:
                st.markdown(f"### 🕒 Reaction Time: `{st.session_state.reaction_time} seconds`")
                st.markdown(f"### ⭐ Score: `{st.session_state.score}`")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🎮 Play Again"):
                        st.session_state.game_started = False
                        st.rerun()
                with col2:
                    if st.button("🔄 Reset Score"):
                        st.session_state.score = 0
                        st.session_state.game_started = False
                        st.rerun()

import streamlit as st
import time
import random

st.set_page_config(page_title="Fortnite Aim Trainer", layout="centered")

# Initialize session state safely
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None
if 'score' not in st.session_state:
    st.session_state['score'] = []
if 'target_index' not in st.session_state:
    st.session_state['target_index'] = random.randint(0, 8)

# Styling
st.markdown("""
    <style>
        .game-box {
            max-width: 400px;
            margin: auto;
            border: 3px solid #ccc;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            background-color: #1e1e1e;
            color: white;
        }
        .center-text {
            text-align: center;
        }
        button {
            height: 50px !important;
            width: 50px !important;
            font-size: 20px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='game-box'>", unsafe_allow_html=True)

st.title("🎯 Fortnite Aim Trainer")

# Start game button
if st.button("🎮 Start New Round"):
    st.session_state['target_index'] = random.randint(0, 8)
    st.session_state['start_time'] = time.time()

# Grid layout
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        if i == st.session_state['target_index']:
            if st.button("🎯", key=f"target_{i}"):
                if st.session_state['start_time'] is not None:
                    reaction = time.time() - st.session_state['start_time']
                    st.session_state['score'].append(reaction)
                    st.success(f"Hit! Reaction time: {reaction:.3f} seconds")
        else:
            st.button(" ", key=f"blank_{i}")

# Show score
if st.session_state['score']:
    st.markdown("---")
    st.write("Your last 5 reaction times:")
    for i, s in enumerate(st.session_state['score'][-5:], 1):
        st.write(f"Shot {i}: {s:.3f} sec")
    avg = sum(st.session_state['score'][-5:]) / len(st.session_state['score'][-5:])
    st.write(f"Average: {avg:.3f} sec")

st.markdown("</div>", unsafe_allow_html=True)
