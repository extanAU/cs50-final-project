from flask import Flask, session, jsonify, request, render_template
from flask_session import Session
from blackjack.game_logic import GameState, evaluate_hand, basic_strategy_decision 
import json


app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure secret key

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'
app.config['SESSION_PERMANENT'] = False
Session(app)

# Helper to convert GameState object to JSON-friendly dict
def serialize_game_state(game):
    return {
        "deck": game.deck,
        "player_hands": game.player_hands,
        "dealer_hand": game.dealer_hand,
        "active_hand": game.active_hand,
        "round_over": game.round_over,
        "outcomes": game.outcomes,
        "multipliers": game.multipliers
    }

@app.route("/")
def index():
    return render_template("index.html")

# Helper to restore GameState from session
def load_game():
    game_data = session.get("game_state")
    if not game_data:
        return None
    game = GameState()
    game.__dict__.update(json.loads(game_data))
    return game

@app.route('/start-round', methods=['POST'])
def start_round():
    game = GameState()
    game.start_round()
    session['game_state'] = json.dumps(serialize_game_state(game))
    return jsonify({
        "playerHands": game.player_hands,
        "playerTotals": [evaluate_hand(hand)[0] for hand in game.player_hands],
        "playerTotal": evaluate_hand(game.player_hands[game.active_hand])[0],
        "dealerTotal": evaluate_hand(game.dealer_hand)[0],
        "playerCards": game.player_hands[game.active_hand],
        "dealerCards": [game.dealer_hand[0], ("?", "?")],
        "wagerMultipliers": game.multipliers,
        "activeHand": game.active_hand,
        "roundOver": False,
        "results": None,
        "message": "New round started."
    })

@app.route('/player-action', methods=['POST'])
def player_action():
    action = request.json.get('action')
    game = load_game()
    if not game:
        return jsonify({"error": "No active game in session"}), 400

    message = ""
    if action == "hit":
        game.player_hit()
        message = "You hit."
    elif action == "stand":
        game.player_stand()
        message = "You stand."
    elif action == "double":
        game.player_double()
        message = "You double down."
    elif action == "split":
        game.player_split()
        message = "You split your hand."
    else:
        return jsonify({"error": "Invalid action"}), 400

    results = None
    if game.round_over:
        results = game.outcomes
        stats = session.get("stats", {"wins": 0, "losses": 0, "pushes": 0, "history": []})
        for outcome in results:
            if outcome == "win":
                stats["wins"] += 1
            elif outcome == "loss":
                stats["losses"] += 1
            elif outcome == "push":
                stats["pushes"] += 1
        stats["history"].append({
            "playerHands": game.player_hands,
            "dealerHand": game.dealer_hand,
            "outcomes": results
        })
        session["stats"] = stats
        message = f"Round over. Result(s): {', '.join(results)}"

    session['game_state'] = json.dumps(serialize_game_state(game))
    dealer_cards = game.dealer_hand if game.round_over else [game.dealer_hand[0], ("?", "?")]

    return jsonify({
        "playerHands": game.player_hands,
        "playerTotals": [evaluate_hand(hand)[0] for hand in game.player_hands],
        "playerTotal": evaluate_hand(game.player_hands[game.active_hand])[0],
        "dealerTotal": evaluate_hand(game.dealer_hand)[0],
        "playerCards": None if game.round_over else game.player_hands[game.active_hand],
        "dealerCards": dealer_cards,
        "activeHand": game.active_hand,
        "wagerMultipliers": game.multipliers,
        "roundOver": game.round_over,
        "results": results,
        "message": message,
        "canSplit": False
    })

@app.route('/bot-decision', methods=['POST'])
def bot_decision():
    game = load_game()
    if not game:
        return jsonify({"error": "No active game in session"}), 400

    current_hand = game.player_hands[game.active_hand]
    dealer_up = game.dealer_hand[0]
    suggestion_code = basic_strategy_decision(current_hand, dealer_up)

    # Human-readable version of the bot's suggestion
    suggestions = {'H': 'Hit', 'S': 'Stand', 'D': 'Double', 'P': 'Split'}
    suggestion_text = suggestions.get(suggestion_code, 'Unknown')

    message = f"Bot suggests: {suggestion_text}"

    return jsonify({
        "message": message,
        "suggestion": suggestion_text
    })

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify(session.get("stats", {"wins": 0, "losses": 0, "pushes": 0, "history": []}))

if __name__ == '__main__':
    app.run(debug=True)
