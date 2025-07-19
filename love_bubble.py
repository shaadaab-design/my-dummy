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
   "you make even the boring moments feel like actual magic hmp"
"my heart goes all badum badum every time i see you dummy"
"YOU’RE literally the best part of every single day ever"
"i’m so so SOOO lucky to have you like FR how did i even get you"
"your smile makes everything else disappear like WHO gave you permission"
"i fall harder every day and it’s NOT FAIR stop being so cute"
"you’re the reason i believe in those dumb fairy tale love stories now"
"my fav place is literally just wherever YOU are hm"
"you turn my gray sky heart into a whole rainbow and now i’m soft"
"i choose you always ALWAYS even when you’re mean to me"
"you’re my home my person my little EVERYTHINGGG"
"with you it’s just… forever vibes and my chest gets all warm"
"you make me wanna be soft and good and better like why"
"i love the way your eyes see stuff like suddenly everything’s pretty"
"you’re the sunshine when i wanna cry into my pillow"
"my heart is LOCKED and you’re the only one who gets the key"
"suddenly all love songs are about you and i HATE IT (but not really)"
"your sleepy voice in the morning makes me go all fuzzy inside"
"you’re my fav notification and i’d ignore the whole world for u"
"the way you make me laugh till i’m wheezing STOPPPP"
"you smell like home and comfort and i’m gonna sob"
"when you scrunch your nose while thinking??? I’M GONE"
"you’re my fav adventure i’d get lost with you every time"
"your weird 3am thoughts make me giggle like a fool"
"my heart does little flippy things when you look at me like that"
"the way you get excited over tiny things makes me wanna squish u"
"you’re the safest softest place in the entire universe HMP"
"you hum when you’re happy and i fall in love all over again"
"you make me believe in magic and now i’m stuck forever"
"your dumb dad jokes shouldn’t make me laugh BUT THEY DO"
"you’re my fav kind of chaos and i wouldn’t change a thing"
"you somehow always know what i need and i hate itttt (no i don’t)"
"time goes fast and slow with you and i’m just?? lost in you??"
"your messy morning hair makes me want to bury my face in ur neck"
"you’re literally the biggest blessing and i didn’t even see u coming"
"you make tuesdays feel like date nights i didn’t plan but love"
"you’re the plot twist that made everything better i swear"
"you see the world in a way that makes me fall harder every time"
"you make my heart feel all full and dumb and i LOVE IT"
"i saw you dancing alone and now i’m giggling into my sleeves"
"you’re my fav distraction and i don’t even wanna focus on anything else"
"your goodnight texts make me feel like the safest lil thing ever"
"you make me wanna write cheesy poetry and blush at my own words"
"you steal my hoodies and somehow make them look cuter on u"
"you’re my comfy place always always and forever hmp"
"your 2am random facts are so dumb and so YOU i can’t stop smiling"
"you make every boring day feel like a birthday party or smth"
"you make me feel brave and soft and clingy at the same time"
"you’re the hello that makes me melt and the goodbye that breaks me"
"your heart is so soft it makes my chest ache and my brain go fuzzy"
"life with you feels like a dream i never wanna wake up from"
"you remember the tiniest things about me and i’m just like… HOW"
"you’re the missing puzzle piece and now i’m whole or whatever"
"your smile is illegal and your joy makes me dizzy"
"you make me feel like i can do anything and that’s terrifying"
"your hugs are actual therapy and i need one every five minutes"
"you’re my fav person to just lay around and do NOTHING with"
"you understand me better than i do and that’s wild hmp"
"you’re the biggest adventure and i’m diving in headfirst"
"your sleepy cuddles are too powerful i literally malfunction"
"you make my heart speed up and calm down all at once i hate it here"
"you believe in my dreams more than i do and now i’m crying"
"you’re my fav love story and i never want it to end"
"you talking at midnight is like a lullaby for my anxious little brain"
"you make me feel like the luckiest dumb baby in the world"
"you make me feel cute and loved and safe and i’m not okay"
"you’re my forever and my always and YES i’m gonna be annoyingly clingy about it"
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