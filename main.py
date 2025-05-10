import random
import time
from collections import Counter, defaultdict

SUITS = ['H', 'D', 'C', 'S']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DECK = [r + s for s in SUITS for r in RANKS]

def evaluate_hand(cards):
    counts = Counter(card[0] for card in cards)
    suits = Counter(card[1] for card in cards)
    values = sorted([RANKS.index(card[0]) for card in cards], reverse=True)
    is_flush = max(suits.values()) >= 5
    unique_values = sorted(set(values), reverse=True)
    straight = False
    for i in range(len(unique_values) - 4):
        if unique_values[i] - unique_values[i+4] == 4:
            straight = True
            break
    if is_flush and straight:
        return 8
    if 4 in counts.values():
        return 7
    if 3 in counts.values() and 2 in counts.values():
        return 6
    if is_flush:
        return 5
    if straight:
        return 4
    if 3 in counts.values():
        return 3
    if list(counts.values()).count(2) == 2:
        return 2
    if 2 in counts.values():
        return 1
    return 0

def get_deck(exclude):
    return [card for card in DECK if card not in exclude]

def deal_random_cards(deck, count):
    return random.sample(deck, count)

def ucb1(node_wins, node_visits, total_visits, c=1.4):
    if node_visits == 0:
        return float('inf')
    return node_wins / node_visits + c * (total_visits ** 0.5 / node_visits ** 0.5)

def simulate_once(my_hand, community):
    used = set(my_hand + community)
    deck = get_deck(used)
    opp_hand = deal_random_cards(deck, 2)
    used.update(opp_hand)
    board_left = 5 - len(community)
    rest_board = deal_random_cards(get_deck(used), board_left)
    full_community = community + rest_board
    my_score = evaluate_hand(my_hand + full_community)
    opp_score = evaluate_hand(opp_hand + full_community)
    if my_score >= opp_score:
        return 1
    return 0

def simulate_win_probability_ucb(my_hand, community, time_limit=10):
    start = time.time()
    wins = defaultdict(int)
    visits = defaultdict(int)
    total = 0
    while time.time() - start < time_limit:
        node = tuple(deal_random_cards(get_deck(set(my_hand + community)), 2))
        result = simulate_once(my_hand, community)
        wins[node] += result
        visits[node] += 1
        total += 1
    best_winrate = 0
    for node in visits:
        winrate = wins[node] / visits[node]
        if winrate > best_winrate:
            best_winrate = winrate
    return best_winrate

def make_decision(my_hand, community_cards):
    win_prob = simulate_win_probability_ucb(my_hand, community_cards, time_limit=10)
    print(f"Estimated win probability: {win_prob:.2%}")
    if win_prob >= 0.5:
        return "STAY"
    else:
        return "FOLD"

if __name__ == "__main__":
    full_deck = DECK[:]
    my_hand = deal_random_cards(full_deck, 2)
    used = set(my_hand)
    community = []

    print(f"My hand: {my_hand}")

    decision = make_decision(my_hand, community)
    if decision == "FOLD":
        print("Folded pre-flop.")
        exit()

    flop = deal_random_cards(get_deck(used), 3)
    community += flop
    used.update(flop)
    print(f"Flop: {flop}")
    decision = make_decision(my_hand, community)
    if decision == "FOLD":
        print("Folded at flop.")
        exit()

    turn = deal_random_cards(get_deck(used), 1)
    community += turn
    used.update(turn)
    print(f"Turn: {turn}")
    decision = make_decision(my_hand, community)
    if decision == "FOLD":
        print("Folded at turn.")
        exit()

    river = deal_random_cards(get_deck(used), 1)
    community += river
    used.update(river)
    print(f"River: {river}")
    decision = make_decision(my_hand, community)
    print(f"Final Decision after River: {decision}")
