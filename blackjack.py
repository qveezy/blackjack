#NOT BUGGY PIECE OF SHIT#

import random

cards = [2 , 3 , 4 , 5 , 6, 7 , 8 , 9 , 10 , 'J', 'Q' , 'K' , 'A'] * 4





player_cards=[]
dealer_cards=[]


def load_balance():
    try:
        with open("balance.txt" , "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 100
    except ValueError:
        return 100

def create_deck():
    global  cards
    cards = [2 , 3 , 4 , 5 , 6, 7 , 8 , 9 , 10 , 'J', 'Q' , 'K' , 'A'] * 4
    return cards



balance=load_balance()

def save_balance(balance):
    with open("balance.txt", "w") as f:
        f.write(str(balance))


def shuffle():
    random.shuffle(cards)


def deal(turn , num):
    for x in range(num):
        card=random.choice(cards)
        turn.append(card)
        cards.remove(card)
    return card

def total(turn):
    total=0
    face=['J','Q','K']
    for card in turn:
        if card in range(1,11):
            total+=card
        elif card in face:
            total+=10
        else:
            if total > 11:
                total+=1
            else:
                total+=11
    return total




def revealplayer():
    print(f"Player has {' | '.join(str(cards) for cards in player_cards)} , TOTAL: {total(player_cards)}")

def revealdealer():
    if len(dealer_cards)==2:
        print(f"Dealer has {dealer_cards[0]} | X , TOTAL: X")
    elif len(dealer_cards)>2:
        print(f"Dealer has {' | '.join(str(cards) for cards in dealer_cards)}, TOTAL: {total(dealer_cards)}")

def blackjack():


    face=['J','Q','K']
    allowedbet=[5,10,15,20]
    global balance

    print("-------------------------")
    print("| Welcome to BlackJack! |")
    print("-------------------------")

    print(f"Your balance is {balance}")



    game_over = False

    while not game_over:
        bet_input = input("Place a bet [5/10/15/20] : ")
        if bet_input.isdigit():
            bet = int(bet_input)
            if bet in allowedbet:
                balance-=bet
                deal(player_cards, 2)
                deal(dealer_cards, 2)
                shuffle()
                revealdealer()
                revealplayer()

                if dealer_cards[0] == 'A' :
                    insurance = input("Do you want to take insurance, it will cost 10?(y/n): ").lower().strip()
                    if insurance == "y":
                        balance -= 10
                        if total(dealer_cards) == 21:
                            balance += bet + 10
                            break


                    elif insurance == "n":
                        if total(dealer_cards) == 21:
                            print("You lost!")
                            break
                    else:
                        continue

                while True:

                    if total(player_cards) == 21 and len(player_cards) == 2:
                        print("You won!")
                        balance+=bet*2
                        break
                    choice=input("Y to hit , N to stay: ").lower().strip()
                    if choice == 'y':
                        deal(player_cards, 1)
                        revealplayer()
                        if total(player_cards) > 21:
                            print("Bust! You lost!")
                            game_over = True
                            break
                    elif choice == 'n':
                        break
                    else:
                        print("Please enter Y or N.")

                if not game_over:
                    if total(player_cards) !=21:
                        while total(dealer_cards) < 17:
                            deal(dealer_cards, 1)
                        print(f"Dealer has {' | '.join(str(cards) for cards in dealer_cards)} , TOTAL: {total(dealer_cards)}")

                        if total(dealer_cards) > 21 or total(player_cards) > total(dealer_cards):
                            print("You win")
                            balance+=bet*2
                        elif total(player_cards) == total(dealer_cards):
                            print("Draw")
                            balance+=bet
                        else:
                            print('Dealer wins.')

                    save_balance(balance)
                    game_over = True

if __name__ == "__main__":
    while True:
        blackjack()
        shuffle()
        player_cards.clear()
        dealer_cards.clear()
        create_deck()


        while True:
            again = input("Do you want to play again(Y/N): ").lower().strip()

            if again == 'y':
                break
            elif again == "n":
                exit()
            else:
                continue
