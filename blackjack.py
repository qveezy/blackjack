#NOT BUGGY PIECE OF SHIT
#DASODJNIPJOI9    FU2VI3UFSEPJFNVAWEUF90W=IVFWE9-
import random
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4

player_hand_1 = []
player_hand_2 = []

player_cards = []
dealer_cards = []


def load_balance():
    try:
        with open("balance.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 100
    except ValueError:
        return 100


def create_deck():
    global cards
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
    return cards


def reveal_hand(hand):
    print(f"Hand: {' | '.join(str(card) for card in hand)} , TOTAL: {total(hand)}")


def play_hand(hand, bet):
    global balance
    doubled = False

    reveal_hand(hand)

    if len(hand) == 2 and balance >= bet:
        double_choice = input("Do you want to double down on this hand? (y/n): ").lower().strip()
        if double_choice == 'y':
            balance -= bet
            bet *= 2
            deal(hand, 1)
            reveal_hand(hand)
            print("Double down — one card only.")
            return bet

    while True:
        if total(hand) == 21 and len(hand) == 2:
            print("Blackjack!")
            return bet

        choice = input("Y to hit, N to stay: ").lower().strip()
        if choice == 'y':
            deal(hand, 1)
            reveal_hand(hand)
            if total(hand) > 21:
                print("Bust!")
                break
        elif choice == 'n':
            break
        else:
            print("Invalid input.")

    return bet


balance = load_balance()


def save_balance(balance):
    with open("balance.txt", "w") as f:
        f.write(str(balance))


def clearcards():
    player_cards.clear()
    dealer_cards.clear()


def shuffle():
    random.shuffle(cards)


def deal(turn, num):
    for x in range(num):
        card = random.choice(cards)
        turn.append(card)
        cards.remove(card)
    return card


def total(turn):
    total = 0
    face = ['J', 'Q', 'K']
    for card in turn:
        if card in range(1, 11):
            total += card
        elif card in face:
            total += 10
        else:
            if total > 11:
                total += 1
            else:
                total += 11
    return total


def fullrevealdealer():
    print(f"Dealer has {' | '.join(str(cards) for cards in dealer_cards)} , TOTAL: {total(dealer_cards)}")


def revealplayer():
    print(f"Player has {' | '.join(str(cards) for cards in player_cards)} , TOTAL: {total(player_cards)}")


def revealdealer():
    if len(dealer_cards) == 2:
        print(f"Dealer has {dealer_cards[0]} | X , TOTAL: X")
    elif len(dealer_cards) > 2:
        print(f"Dealer has {' | '.join(str(cards) for cards in dealer_cards)}, TOTAL: {total(dealer_cards)}")


def blackjack():
    global balance
    face = ['J', 'Q', 'K']
    allowedbet = [5, 10, 15, 20]
    balance = load_balance()

    clear_console()
    print("-------------------------")
    print("| Welcome to BlackJack! |")
    print("-------------------------")

    print(f"Your balance is {balance}")

    game_over = False

    while not game_over:
        if balance < 5:
            print("Not enough money to play")
            break

        bet_input = input("Place a bet [5/10/15/20] : ").strip()
        if bet_input.isdigit():
            bet = int(bet_input)
            if bet in allowedbet and balance >= bet:
                balance -= bet
                save_balance(balance)

                # Очищаем карты для нового раунда
                clearcards()

                deal(player_cards, 2)
                deal(dealer_cards, 2)
                shuffle()
                revealdealer()
                revealplayer()

                # Проверка на страховку
                if dealer_cards[0] == 'A':
                    insurance = input("Do you want to take insurance, it will cost 10?(y/n): ").lower().strip()
                    if insurance == "y":
                        if balance >= 10:
                            balance -= 10
                            if total(dealer_cards) == 21:
                                balance += bet + 20  # Возвращаем ставку + выигрыш по страховке
                                print("Dealer has blackjack! Insurance pays off.")
                                fullrevealdealer()
                                continue
                        else:
                            print("Not enough balance for insurance.")

                    if total(dealer_cards) == 21:
                        print("Dealer has blackjack! You lost!")
                        fullrevealdealer()
                        continue

                # Проверка на блэкджек игрока
                if total(player_cards) == 21 and len(player_cards) == 2:
                    print("Blackjack! You won!")
                    if total(dealer_cards) == 21:
                        print("Push! Both have blackjack.")
                        balance += bet
                    else:
                        balance += int(bet * 2.5)
                    save_balance(balance)
                    continue


                split_played = False
                if player_cards[0] == player_cards[1]:
                    split_choice = input("You have a pair. Do you want to split? (y/n): ").lower().strip()
                    if split_choice == 'y':
                        if balance >= bet:
                            balance -= bet
                            save_balance(balance)

                            player_hand_1 = [player_cards[0]]
                            player_hand_2 = [player_cards[1]]

                            deal(player_hand_1, 1)
                            deal(player_hand_2, 1)

                            print("\n--- Playing first hand ---")
                            bet1 = play_hand(player_hand_1, bet)

                            print("\n--- Playing second hand ---")
                            bet2 = play_hand(player_hand_2, bet)


                            while total(dealer_cards) < 17:
                                deal(dealer_cards, 1)

                            fullrevealdealer()


                            for idx, (hand, b) in enumerate(zip([player_hand_1, player_hand_2], [bet1, bet2]), start=1):
                                if total(hand) > 21:
                                    print(f"Hand {idx}: Bust!")
                                elif total(dealer_cards) > 21:
                                    print(f"Hand {idx}: Dealer busts! You win!")
                                    balance += b * 2
                                elif total(hand) > total(dealer_cards):
                                    print(f"Hand {idx}: You win!")
                                    balance += b * 2
                                elif total(hand) == total(dealer_cards):
                                    print(f"Hand {idx}: Push.")
                                    balance += b
                                else:
                                    print(f"Hand {idx}: Dealer wins.")

                            save_balance(balance)
                            split_played = True
                        else:
                            print("Not enough balance to split.")


                if not split_played:
                    player_busted = False

                    while True:
                        choice = input("Y to hit, N to stay: ").lower().strip()
                        if choice == 'y':
                            deal(player_cards, 1)
                            revealplayer()
                            if total(player_cards) > 21:
                                print("Bust! You lost!")
                                player_busted = True
                                break
                        elif choice == 'n':
                            break
                        else:
                            print("Please enter Y or N.")


                    if not player_busted:
                        while total(dealer_cards) < 17:
                            deal(dealer_cards, 1)

                        fullrevealdealer()


                        player_total = total(player_cards)
                        dealer_total = total(dealer_cards)

                        if dealer_total > 21:
                            print("Dealer busts! You win!")
                            balance += bet * 2
                        elif player_total > dealer_total:
                            print("You win!")
                            balance += bet * 2
                        elif player_total == dealer_total:
                            print("Push! It's a tie.")
                            balance += bet
                        else:
                            print("Dealer wins!")

                    save_balance(balance)

                print(f"Your balance is now: {balance}")


                while True:
                    next_action = input(
                        "Do you want to play again?(Y/N/(Q)uit): ").lower().strip()
                    if next_action == 'y':
                        break
                    elif next_action == 'n':
                        break
                    elif next_action == 'q':
                        return "quit"
                    else:
                        print("Please enter Y or N")
            else:
                if bet not in allowedbet:
                    print("Invalid bet amount. Choose from [5/10/15/20]")
                else:
                    print("Not enough balance for this bet.")
        else:
            print("Please enter a valid number.")


def play_blackjack():
    result = blackjack()
    create_deck()
    return result


                exit()
            else:
                continue
