import streamlit as st

st.set_page_config(layout="wide", page_title="Strawberry Cross", initial_sidebar_state="collapsed")

html_game = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Strawberry Cross</title>
  <style>
    body {
      margin: 0;
      overflow: hidden;
      background: linear-gradient(to right, #ff9a9e, #fad0c4);
    }
    canvas {
      display: block;
      margin: auto;
      background-color: #fff;
      border: 4px solid #ff69b4;
      border-radius: 10px;
    }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="600" height="700"></canvas>
  <script>
    // full game JavaScript here
    // (this is the long part I gave you with strawberry, hearts, collisions, etc.)
  </script>
</body>
</html>
'''

st.components.v1.html(html_game, height=720, width=640, scrolling=False)
