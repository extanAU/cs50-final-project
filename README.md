# cs50-final-project

https://www.youtube.com/watch?v=7KcytwumfdU&ab_channel=EthanTan

## Project Name: Blackjack!
Ethan Tan & Christoph von Pezold

Welcome to the Blackjack!, a full‑stack casino‑style card game built with Flask and JS!  
This README will guide you through everything you need to know to install, configure, and play the game locally. 

## Features
1. Interactive Blackjack gameplay: Hit, Stand, Double, Split
2. Visual card display: Real card images on a felt‑style background.
3. Specially coded-bot that provides suggestions based on the optimal move in a given position
4. Decision log: Step‑by‑step action transcript.
5. Performance chart: Cumulative net win tracker rendered with Chart.js.
6. Session‑based play: Uses Flask’s session for per‑user game state and statistics.

## Prerequisites
- Contained by downloading requirements.txt
    - To do this, navigate to the CS50-Final-Project directory, then input
    - pip install -r requirements.txt
- To do this, you must ensure that Python is installed on your operating system
- To check if pip is installed run this command in your terminal
    - pip --version
- If Python is installed but Pip is missing, run this command
    - python -m ensurepip --upgrade
- Basic requirements include Flask, dotenv, a modern web browser (Chrome/Firefox/Safari)

## Installation
1. Clone the cs50-final-project repository from GitHub, or download from Gradescope
2. Create and activate a virtual environment
   - python3 -m venv venv
   - source venv/bin/activate    # on macOS/Linux
   - .\venv\Scripts\activate   # on Windows PowerShell
3. Install Dependencies
- pip install -r requirements.txt
4. IF you wish to use server-side sessions, add
- Flask-Session>=0.4.0
then
- pip install Flask-Session

## Running the Application
With your virtual environment activated: 
- export FLASK_APP=blackjack.app       # macOS/Linux
- set FLASK_APP=blackjack.app          # Windows
- flask run                             # runs on http://localhost:5000
- OR 
- flask --app blackjack.app run

For Debug Mode and Auto-Reload:
flask --debug run

Once Running, Open Browser To:
http://localhost:5000

## How to Play Blackjack
1. Start a new round by clicking Start New Round.

2. Player action buttons (Hit, Stand, Double, Split) light up when legal:

- Hit: Draw another card.

- Stand: End your turn, let the dealer play.

- Double: Double your bet, draw one more card, then stand.

- Split: Split a starting pair into two hands (only on first two cards).

- Ask Bot: Request a recommended move according to basic strategy.

3. Decision Log: See each action recorded step by step.

4. Cumulative Net Wins: Chart tracks wins minus losses over rounds.

5. After each round ends, you can start another or let the bot take over.

## Troubleshooting
- Cookie Too Large warning: Use Flask‑Session or reduce session data size (see Configuration).

- Asset 404 Errors: Ensure static/cards/ contains all 52 card images plus back.png.

- Venv Errors: Delete files labelled "venv" in directory, deactivate venv by running "deactive" in terminal, and reactivate venv from instructions above

- Port Already in Use: Change port with: flask run --port 5001 (or any other port) 

## License
Feel free to adapt and share! Thank you for playing and reviewing this project.

