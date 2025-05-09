# app.py
from flask import Flask, jsonify, render_template, request, redirect, url_for
from blackjack.old.game_logic1 import Deck, play_round, basic_strategy_decision, is_blackjack, evaluate_hand, Card

# Flask Application Initialization and Route Definitions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from dotenv import load_dotenv

# app = Flask(__name__) -> no longer needed

# Create a single deck of cards (you can adjust number of decks)
deck = Deck(num_decks=6)
stats = {"wins": 0, "losses": 0, "pushes": 0, "history": []}

@app.route("/")
def index():
    # Serve the main game interface
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

@app.route("/play-round")
def play_round_route():
    """Play one round of blackjack and return the result as JSON."""
    result = play_round(deck)
    # Update stats
    # If split, result["outcome"] might be a list of outcomes
    outcomes = result["outcome"]
    if isinstance(outcomes, list):
        # count each hand outcome
        for out in outcomes:
            if out == "win":
                stats["wins"] += 1
            elif out == "lose":
                stats["losses"] += 1
            elif out == "push":
                stats["pushes"] += 1
            stats["history"].append(out)
    else:
        out = outcomes
        if out == "win":
            stats["wins"] += 1
        elif out == "lose":
            stats["losses"] += 1
        elif out == "push":
            stats["pushes"] += 1
        stats["history"].append(outcomes)
    return jsonify(result)

@app.route("/stats")
def stats_route():
    """Return win/loss statistics."""
    # We can provide total counts and a history list (e.g., sequence of outcomes)
    return jsonify(stats)


