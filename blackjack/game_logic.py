# blackjack/game_logic.py

import random

# Define ranks and suits for a standard deck
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['H', 'D', 'C', 'S']  # Hearts, Diamonds, Clubs, Spades

class Card:
    def __init__(self, rank, suit):
        self.rank = rank  # e.g., 'A', 'K', '10', etc.
        self.suit = suit  # e.g., 'H', 'D', 'C', 'S'

    def value(self):
        """Return the blackjack value of the card (Ace as 1 here; we'll handle 11 logic elsewhere)."""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        if self.rank == 'A':
            return 1  # Treat Ace as 1 by default (we'll add 10 later if it doesn't bust)
        return int(self.rank)

    def __repr__(self):
        return f"{self.rank}{self.suit}"  # e.g., "AH" for Ace of Hearts

class Deck:
    def __init__(self, num_decks=1):
        self.cards = [Card(rank, suit) for rank in RANKS for suit in SUITS] * num_decks
        random.shuffle(self.cards)

    def deal_card(self):
        """Pop a card from the deck (shuffles new deck if empty)."""
        if not self.cards:
            self.__init__()  # reinitialize and shuffle if deck is empty
        return self.cards.pop()

def evaluate_hand(cards):
    """Return the total value of the hand and whether it is soft (i.e., contains an Ace counted as 11)."""
    # Sum all card values treating Aces as 1
    total = sum(card.value() for card in cards)
    has_ace = any(card.rank == 'A' for card in cards)
    soft = False
    # If there's an ace and counting one of them as 11 doesn't bust, treat one ace as 11 (add 10 to total)
    if has_ace and total + 10 <= 21:
        total += 10
        soft = True
    return total, soft

def is_blackjack(cards):
    """Check if the hand is a natural blackjack (2 cards: Ace + 10-value)."""
    if len(cards) == 2:
        vals = sorted([card.value() for card in cards])
        return vals == [1, 10]  # one Ace (counted as 1 here) and one 10 or face card
    return False

# BASIC STRATEGY DECISION LOGIC (TO BE CHANGED)

def basic_strategy_decision(player_cards, dealer_up_card):
    total, soft = evaluate_hand(player_cards)
    dealer_value = dealer_up_card.value()
    # Check for pair
    if len(player_cards) == 2 and player_cards[0].rank == player_cards[1].rank:
        rank = player_cards[0].rank
        # Pairs: simplified rules for demonstration
        if rank == 'A' or rank == '8':
            return 'P'  # always split aces and eights
        if rank in ['10', 'J', 'Q', 'K']:
            return 'S'  # never split tens (stand on 20)
        if rank == '5':
            # Pair of 5s is essentially a hard 10, better to double against certain dealer cards
            if dealer_value in range(2, 10):
                return 'D'
            else:
                return 'H'
        if rank == '9':
            # Split 9s except when dealer has 7, 10, or Ace (then stand on 18)
            if dealer_value in [7, 10, 11]:
                return 'S'
            else:
                return 'P'
        # Default for other pairs (2,3,4,6,7): split if dealer up-card is 2-7, otherwise hit.
        if dealer_value in range(2, 8):
            return 'P'
        else:
            return 'H'
    # If not a pair (or after handling split logic), handle soft totals vs hard totals:
    if soft:
        # Soft totals (one Ace counted as 11)
        if total == 17:  # e.g., A-6 (soft 17)
            if dealer_value in range(3, 7):
                return 'D'  # double on soft 17 against 3-6 if allowed
            else:
                return 'H'
        if total in range(13, 18):  # A-2 to A-6 (soft 13 to soft 18)
            if dealer_value in range(4, 7):
                return 'D'  # double soft 13-18 vs dealer 4-6
            else:
                return 'H'
        if total >= 19:
            return 'S'  # soft 19 or more, always stand (soft 18 stands except vs certain dealer values, simplified)
    else:
        # Hard totals (no ace or ace counted as 1)
        if total <= 8:
            return 'H'  # always hit hard 8 or less
        if total == 9:
            if dealer_value in range(3, 7):
                return 'D'  # double 9 vs dealer 3-6
            else:
                return 'H'
        if total == 10:
            if dealer_value < 10:
                return 'D'  # double 10 vs dealer 2-9
            else:
                return 'H'
        if total == 11:
            return 'D'  # always double 11 (unless dealer has Ace which might be a 10-value check, but we'll double anyway)
        if total == 12:
            if dealer_value in range(4, 7):
                return 'S'  # stand on hard 12 vs 4-6
            else:
                return 'H'
        if total in range(13, 17):
            if dealer_value <= 6:
                return 'S'  # stand on 13-16 vs dealer 2-6 (dealer likely to bust)
            else:
                return 'H'  # hit 13-16 vs dealer 7-A
        if total >= 17:
            return 'S'  # always stand on hard 17+
    # Default fallback
    return 'H'

def play_round(deck):
    """Simulate one round of blackjack. Return a dict with details of the round."""
    # Initial deal
    player_cards = [deck.deal_card(), deck.deal_card()]
    dealer_cards = [deck.deal_card(), deck.deal_card()]
    dealer_up = dealer_cards[0]
    round_info = {
        "player_initial": [repr(c) for c in player_cards],
        "dealer_initial": [repr(dealer_cards[0]), "Hidden"]  # second card hidden initially
    }
    decisions_log = []  # to record actions taken

    # Check for natural blackjacks
    player_blackjack = is_blackjack(player_cards)
    dealer_blackjack = is_blackjack(dealer_cards)
    if player_blackjack or dealer_blackjack:
        # If either has blackjack, determine outcome immediately (no hits taken)
        round_info["player_final"] = [repr(c) for c in player_cards]
        round_info["dealer_final"] = [repr(c) for c in dealer_cards]
        if player_blackjack and dealer_blackjack:
            round_info["outcome"] = "push"
            round_info["reason"] = "Both player and dealer have blackjack."
        elif player_blackjack:
            round_info["outcome"] = "win"
            round_info["reason"] = "Player has blackjack."
        else:
            round_info["outcome"] = "lose"
            round_info["reason"] = "Dealer has blackjack."
        round_info["decisions"] = decisions_log
        return round_info

    # Determine if a split is to be done
    split_performed = False
    split_hand_cards = []  # to store cards for second hand if split
    if len(player_cards) == 2 and player_cards[0].rank == player_cards[1].rank:
        action = basic_strategy_decision(player_cards, dealer_up)
        if action == 'P':  # Split
            split_performed = True
            # Create two hands from the pair
            second_card = player_cards.pop()  # remove second card from player_cards
            # Deal one new card to each split hand
            player_cards = [player_cards[0], deck.deal_card()]       # original hand gets one new card
            split_hand_cards = [second_card, deck.deal_card()]       # second hand
            decisions_log.append("Split pair into two hands")
    # Now we have either one or two player hands to play out
    player_hands = [player_cards]
    if split_performed:
        player_hands.append(split_hand_cards)

    # Play out each player hand (bot decisions)
    outcomes = []  # collect outcome for each hand vs dealer
    final_player_hands = []  # store final cards for each hand
    hand_index = 0
    for hand in player_hands:
        hand_index += 1
        hand_active = True
        # Check if we should double on initial two-card hand
        if len(hand) == 2:
            action = basic_strategy_decision(hand, dealer_up)
            if action == 'D':
                # Perform double: take one card and finish
                new_card = deck.deal_card()
                hand.append(new_card)
                decisions_log.append(f"Hand {hand_index}: Double down (drew {new_card})")
                hand_active = False  # no further hits after doubling
        # If not doubled, and hand not finished, keep hitting or standing as per strategy
        while hand_active:
            action = basic_strategy_decision(hand, dealer_up)
            if action == 'H':
                new_card = deck.deal_card()
                hand.append(new_card)
                decisions_log.append(f"Hand {hand_index}: Hit (drew {new_card})")
                total, _ = evaluate_hand(hand)
                if total > 21:  # bust
                    decisions_log.append(f"Hand {hand_index}: Bust with {total}")
                    hand_active = False
                # else, continue loop to decide next action on new total
            elif action == 'S':
                decisions_log.append(f"Hand {hand_index}: Stand on total {evaluate_hand(hand)[0]}")
                hand_active = False
            elif action == 'D':
                # If we reach here, it means a double was suggested but we already are beyond first move,
                # so just treat it as a hit (this scenario is rare due to how we structured logic).
                new_card = deck.deal_card()
                hand.append(new_card)
                decisions_log.append(f"Hand {hand_index}: (Late) Double as hit (drew {new_card})")
                hand_active = False
            else:
                # 'P' shouldn't occur here because we only consider splitting at the start.
                decisions_log.append(f"Hand {hand_index}: Stand on total {evaluate_hand(hand)[0]}")
                hand_active = False
        # Record the final hand
        final_player_hands.append([repr(c) for c in hand])
    # After player actions, play out dealer's hand
    # Reveal the dealer's hole card and hit until at least 17
    round_info["dealer_initial"][1] = repr(dealer_cards[1])  # reveal hidden card
    dealer_total, dealer_soft = evaluate_hand(dealer_cards)
    while dealer_total < 17 or (dealer_total == 17 and dealer_soft):
        new_card = deck.deal_card()
        dealer_cards.append(new_card)
        dealer_total, dealer_soft = evaluate_hand(dealer_cards)
        # (dealer hits on soft 17 if rule demands; here we assume dealer hits on soft 17)
    round_info["dealer_final"] = [repr(c) for c in dealer_cards]

    # Determine outcome for each player hand against dealer
    dealer_total = evaluate_hand(dealer_cards)[0]
    for idx, hand in enumerate(final_player_hands, start=1):
        player_total = evaluate_hand([Card(card[:-1], card[-1]) for card in hand])[0]  # reconstruct cards to evaluate
        if player_total > 21:
            outcome = "lose"  # player bust
        elif dealer_total > 21:
            outcome = "win"   # dealer busts
        elif player_total < dealer_total:
            outcome = "lose"
        elif player_total > dealer_total:
            outcome = "win"
        else:
            outcome = "push"
        outcomes.append(outcome)
        decisions_log.append(f"Hand {idx}: Result = {outcome.upper()}")
    # If there were two hands, we can combine outcome, else single
    round_info["outcome"] = outcomes if len(outcomes) > 1 else outcomes[0]
    round_info["decisions"] = decisions_log
    round_info["player_final"] = final_player_hands if len(final_player_hands) > 1 else final_player_hands[0]
    return round_info

