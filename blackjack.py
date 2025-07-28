'''
VERY BUGGY PIECE OF SHIT
'''
import random

deck=[2,3,4,5,6,7,8,9,10,"J","Q","K","A",2,3,4,5,6,7,8,9,10,"J","Q","K","A",2,3,4,5,6,7,8,9,10,"J","Q","K","A",2,3,4,5,6,7,8,9,10,"J","Q","K","A",]

playerIn=True
dealerIn=True
status=True
con=True
player_balance=100

dealerHand=[]
playerHand=[]

def dealHand(turn):

    card=random.choice(deck)
    turn.append(card)
    deck.remove(card)

def total(turn):
    total=0
    face= ["K",'Q','J']
    for card in turn:
        if card in range(1,11):
            total+=card
        elif card in face:
            total += 10
        else:
            if total>11:
                total+=1
            else:
                total+=11
    return total

def revealDealerHand():
    if len(dealerHand) == 2:
        return dealerHand[0]
    elif len(dealerHand) > 2:
        return dealerHand[0] , dealerHand[1]

for _ in range(2):
    dealHand(dealerHand)
    dealHand(playerHand)

while con==True:
    while status==True:
        print("Welcome to BlackJack!")
        print(f"Your balance is {player_balance}")
        bet=input("Enter your bet: ")
        if bet.isdigit():
            bet=int(bet)
            player_balance=player_balance-bet
            status=False
        else:
            print("\n PLEASE Enter numbers \n")
            continue

    while playerIn or dealerIn:
        print(f'Dealer has {revealDealerHand()} and X')
        print(f'You have {playerHand} and total {total(playerHand)}')
        if playerIn:
            stayorhit=input("1. Stay or 2. Hit?: ")
        if total(dealerHand)>16:
            dealerIn = False
        else:
            dealHand(dealerHand)
        if stayorhit == '1':
            playerIn = False
        else:
            dealHand(playerHand)
        if total(playerHand) >= 21:
            break
        elif total(dealerHand) >= 21:
            break


    if total(playerHand)==21:
        print(f"You have {playerHand} for a total {total(playerHand)} and dealer has {dealerHand} for a total of {total(dealerHand)}")
        print("You win!")
        player_balance+=bet*2
    elif total(dealerHand)==21:
        print(f"You have {playerHand} for a total {total(playerHand)} and dealer has {dealerHand} for a total of {total(dealerHand)}")
        print("Dealer wins!")
    elif total(playerHand) > 21:
        print(f"You have {playerHand} for a total {total(playerHand)} and dealer has {dealerHand} for a total of {total(dealerHand)}")
        print("You bust!")
    elif total(dealerHand) > 21:
        print(f"You have {playerHand} for a total {total(playerHand)} and dealer has {dealerHand} for a total of {total(dealerHand)}")
        print("Dealer busts!")
    elif 21 - total(dealerHand) < 21 - total(playerHand) :
        print(f"You have {playerHand} for a total {total(playerHand)} and dealer has {dealerHand} for a total of {total(dealerHand)}")
        print("Dealer wins!")
    elif 21 - total(dealerHand) > 21 - total(playerHand) :
        print(f"You have {playerHand} for a total {total(playerHand)} and dealer has {dealerHand} for a total of {total(dealerHand)}")
        print("Player win!")
        player_balance += bet * 2
    elif total(dealerHand) == total(playerHand) :
        print(f"You have {playerHand} for a total {total(playerHand)} and dealer has {dealerHand} for a total of {total(dealerHand)}")
        print("Draw!")
        player_balance += bet
        print(f"Your balance after game is {player_balance}")

    ask = input("Do you want to continue?(1-Yes/2-No): ")
    if ask == 1:
        continue
    elif ask == 2:
        break
    else:
        print("Please write numbers")
