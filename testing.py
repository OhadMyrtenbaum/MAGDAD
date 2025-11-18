import random

# Card deck setup
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
          '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}


def create_deck():
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck


def calculate_hand_value(hand):
    """Calculate best possible score (handle Aces as 1 or 11)."""
    value = sum(values[card[0]] for card in hand)
    aces = sum(card[0] == 'A' for card in hand)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


def print_hand(player_name, hand, hide_first=False):
    """Print hand cards (optionally hide one for the dealer)."""
    if hide_first:
        print(f"{player_name}'s hand: [Hidden], {hand[1][0]} of {hand[1][1]}")
    else:
        cards = ', '.join([f"{r} of {s}" for r, s in hand])
        print(f"{player_name}'s hand: {cards}  (value: {calculate_hand_value(hand)})")


def play_round(deck):
    """Play a single round. Return the updated deck."""
    if len(deck) < 10:
        print("\nNot enough cards left to start another round. Game over!")
        return None

    print("\n=== New Round ===")
    num_players = int(input("Enter number of players for this round: "))
    min_cards_needed = (num_players + 1) * 2
    if len(deck) < min_cards_needed:
        print("Not enough cards for all players. Ending game.")
        return None

    # Initialize hands
    players = {f"Player {i+1}": [deck.pop(), deck.pop()] for i in range(num_players)}
    dealer = [deck.pop(), deck.pop()]

    # Player turns
    for name, hand in players.items():
        print("\n--------------------------------")
        while True:
            print_hand(name, hand)
            if calculate_hand_value(hand) > 21:
                print("Bust! Over 21.")
                break
            move = input(f"{name}, Hit or Stand? (h/s): ").strip().lower()
            if move == 'h':
                if not deck:
                    print("Deck is empty! No more cards.")
                    break
                hand.append(deck.pop())
            else:
                break

    # Dealer turn
    print("\n=== Dealer's Turn ===")
    print_hand("Dealer", dealer)
    while calculate_hand_value(dealer) < 17 and deck:
        dealer.append(deck.pop())
        print_hand("Dealer", dealer)
    dealer_value = calculate_hand_value(dealer)
    if dealer_value > 21:
        print("Dealer busts!")

    # Results
    print("\n=== Final Results ===")
    print_hand("Dealer", dealer)
    for name, hand in players.items():
        player_value = calculate_hand_value(hand)
        print_hand(name, hand)
        if player_value > 21:
            print(f"{name} loses (busted).")
        elif dealer_value > 21 or player_value > dealer_value:
            print(f"{name} wins!")
        elif player_value == dealer_value:
            print(f"{name} pushes (tie).")
        else:
            print(f"{name} loses.")

    print(f"\nCards remaining in deck: {len(deck)}")
    return deck


def play_blackjack():
    print("=== Blackjack Multi-Round ===")
    deck = create_deck()

    while True:
        deck = play_round(deck)
        if not deck or len(deck) < 10:
            break
        again = input("\nPlay another round? (y/n): ").strip().lower()
        if again != 'y':
            break

    print("\nThanks for playing! Final cards remaining:", len(deck))


if __name__ == "__main__":
    play_blackjack()
