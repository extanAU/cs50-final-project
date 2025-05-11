import random

def card_value(rank):
    if rank in ['J', 'Q', 'K']:
        return 10
    if rank == 'A':
        return 11
    return int(rank)

def evaluate_hand(hand):
    total = 0
    aces = 0
    for rank, _ in hand:
        if rank in ['J', 'Q', 'K']:
            total += 10
        elif rank == 'A':
            total += 1
            aces += 1
        else:
            total += int(rank)
    if aces > 0 and total + 10 <= 21:
        return total + 10, True
    return total, False

class GameState:
    def __init__(self):
        self.deck = self._create_shuffled_deck()
        self.player_hands = [[]]        # list of hands (for split support)
        self.dealer_hand = []
        self.active_hand = 0            # index of current hand (0 or 1 if split)
        self.round_over = False
        self.outcomes = []              # outcomes for each hand at end of round ("win", "loss", "push")
        self.multipliers = [1 for _ in self.player_hands]  # multipliers for each hand (for double down support)
    
    def _create_shuffled_deck(self):
        ranks = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
        suits = ['H', 'S', 'C', 'D']
        deck = [(str(r), s) for r in ranks for s in suits]
        random.shuffle(deck)
        return deck

    def start_round(self):
        self.deck = self._create_shuffled_deck()
        self.player_hands = [[self.deck.pop(), self.deck.pop()]]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.active_hand = 0
        self.round_over = False
        self.outcomes = [None]
        self.multipliers = [1]

    def player_hit(self):
        if self.round_over:
            return
        hand = self.player_hands[self.active_hand]
        hand.append(self.deck.pop())
        if evaluate_hand(hand)[0] > 21:
            self.outcomes[self.active_hand] = "loss"
            if self.active_hand < len(self.player_hands) - 1:
                self.active_hand += 1
            else:
                self._dealer_play_and_settle()

    def player_stand(self):
        if self.round_over:
            return
        # record a stand as “pending” (actually will be set in settlement)
        self.outcomes[self.active_hand] = None
        if self.active_hand < len(self.player_hands) - 1:
            self.active_hand += 1
        else:
            self._dealer_play_and_settle()

    def player_double(self):
        hand = self.player_hands[self.active_hand]
        # only double if exactly two cards
        if len(hand) != 2 or self.round_over:
            return
        # double the wager
        self.multipliers[self.active_hand] *= 2

        hand.append(self.deck.pop())
         # immediately move on
        if self.active_hand < len(self.player_hands) - 1:
            self.active_hand += 1
        else:
            self._dealer_play_and_settle()
    

    def player_split(self):
        hand = self.player_hands[0]
        if len(hand) == 2 and hand[0][0] == hand[1][0]:
            second_card = hand.pop()
            new_hand1 = [hand[0], self.deck.pop()]
            new_hand2 = [second_card, self.deck.pop()]
            self.player_hands = [new_hand1, new_hand2]
            self.multipliers = [1 for _ in self.player_hands]
            self.active_hand = 0
            self.outcomes = [None] * len(self.player_hands)


    def _dealer_play_and_settle(self):
        while evaluate_hand(self.dealer_hand)[0] < 17:
            self.dealer_hand.append(self.deck.pop())
        dealer_total = evaluate_hand(self.dealer_hand)[0]
        for i, hand in enumerate(self.player_hands):
            if self.outcomes[i] is not None:
                continue
            player_total = evaluate_hand(hand)[0]
            if player_total > 21:
                self.outcomes[i] = "loss"
            elif dealer_total > 21:
                self.outcomes[i] = "win"
            elif player_total > dealer_total:
                self.outcomes[i] = "win"
            elif player_total < dealer_total:
                self.outcomes[i] = "loss"
            else:
                self.outcomes[i] = "push"
        self.round_over = True

# implementation of standard basic strategy for blackjack
def basic_strategy_decision(player_hand, dealer_up_card):
    total, soft = evaluate_hand(player_hand)
    dealer_value = card_value(dealer_up_card[0])
    
    if len(player_hand) == 2 and player_hand[0][0] == player_hand[1][0]:
        rank = player_hand[0][0]
        if rank == 'A' or rank == '8':
            return 'P'
        if rank in ['10', 'J', 'Q', 'K']:
            return 'S'
        if rank == '5':
            if dealer_value in range(2, 10):
                return 'D'
            else:
                return 'H'
        if rank == '9':
            if dealer_value in [7, 10, 11]:
                return 'S'
            else:
                return 'P'
        if dealer_value in range(2, 8):
            return 'P'
        else:
            return 'H'

    if soft:
        if total == 17:
            if dealer_value in range(3, 7) and len(player_hand) == 2:
                return 'D'
            else:
                return 'H'
        if total in range(13, 18):
            if dealer_value in range(4, 7) and len(player_hand) == 2:
                return 'D'
            else:
                return 'H'
        if total >= 19:
            return 'S'
    else:
        if total <= 8:
            return 'H'
        if total == 9:
            if dealer_value in range(3, 7) and len(player_hand) == 2:
                return 'D'
            else:
                return 'H'
        if total == 10:
            if dealer_value < 10:
                if len(player_hand) == 2 :
                    return 'D'
                else: 
                    return 'H'
            else:
                return 'H'
        if total == 11:
            if len(player_hand) == 2 :
                return 'D'
            else: 
                return 'H'
        if total == 12:
            if dealer_value in range(4, 7):
                return 'S'
            else:
                return 'H'
        if total in range(13, 17):
            if dealer_value <= 6:
                return 'S'
            else:
                return 'H'
        if total >= 17:
            return 'S'
    return 'H'
