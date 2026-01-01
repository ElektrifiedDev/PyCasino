import asyncio
import random
import os
from colorama import Fore, Style, init
import time
import sys
import json

init(autoreset=True)

def main_menu():
    return

def welcome():
    global cash
    cash = 100
    print(Fore.WHITE + "Welcome to the Casino!" + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "We have a number of games available, where you can gamble!" + Style.RESET_ALL)
    input()
    os.system('cls')

def game_select():
    print(f"Here is a list of games available:\n{Fore.LIGHTBLACK_EX + "\n1. Coin Flipping\n2. Dice" + Style.RESET_ALL}")
    userchoice = input("\nPlease enter the number corresponding to your game of choice:   ")

    if userchoice == "1":
        os.system('cls')
        print(f"Welcome to the {Fore.BLUE + "Coinflip" + Style.RESET_ALL} game. \nIn this game, you bet money on either Heads or Tails. If you win, you earn double of what you had bet. If you lose, you lose the money you had bet.")
        input()
        os.system('cls')
        game_coinflip()
    elif userchoice == "2":
        os.system('cls')
        print(f"Welcome to the {Fore.BLUE + "Dice" + Style.RESET_ALL} table. \nIn this game, you roll two dice and bet money on the result.")
        print(f"If you roll {Fore.CYAN + "two 6's" + Style.RESET_ALL}, you hit the jackpot and your bet gets multiplied by {Fore.YELLOW + "5x" + Style.RESET_ALL}.")
        print(f"If you roll for a {Fore.CYAN + "a total of 10 or 11" + Style.RESET_ALL}, your bet gets multipled by {Fore.YELLOW + "3x" + Style.RESET_ALL}.")
        print(f"If you roll for a {Fore.CYAN + "a total of 7, 8 or 9" + Style.RESET_ALL}, your bet gets multiplied by {Fore.YELLOW + "2x" + Style.RESET_ALL}.")
        input()
        os.system('cls')
        game_dice()
    else:
        print("That isn't a valid option!")
        input()
        os.system('cls')
        return game_select()
    
def bankrupt():
    print(f"\nUnfortunately, your bank has declared you {Fore.RED + "bankrupt" + Style.RESET_ALL}.")
    input("Press Enter to restart...")
    os.system('cls')
    return main_menu()

def game_coinflip():
    try:
        bet = float(input(f"You have ${cash} available. Enter your bet:   "))
    except ValueError:
        os.system('cls')
        print("Please enter a valid number.")
        return game_coinflip()
    
    if bet > cash:
        os.system('cls')
        print(f"You can't bet more than you have! Your maximum bet is {cash}")
        return game_coinflip()
    elif bet <= 0:
        os.system('cls')
        print("You cannot make a bet of 0 or less!")
        return game_coinflip()
    
    target = input("Please enter Heads (H) or Tails (T):   ").lower()
    if target not in ["h", "t"]:
        print("You have to enter either H or T")
        return game_coinflip()
    
    print(f"You bet ${bet} on {'Heads' if target == 'h' else 'Tails'}!")
    print("Flipping...")
    time.sleep(1.5)

    cash -= bet
    flip = random.choice(["h", "t"])

    if flip == target:
        bet *= 2
        cash += bet
        print(f"You won! You earned ${bet} and now have ${cash}.")
    else:
        print(f"You lost ${bet}. You now have ${cash}.")

    if cash <= 0:
        return bankrupt()
    
    again = input("Would you like to play again? (Y/N):   ").lower()
    if again == "y":
        os.system('cls')
        return game_coinflip()
    else:
        os.system('cls')
        return game_select()
    
def game_dice():
    try:
        bet = float(input(f"You have ${cash} available. Enter your bet:   "))
    except ValueError:
        print("Please enter a valid number.")
        input()
        os.system('cls')
        return game_dice()

    if bet > cash:
        print(f"You can't bet more than you have! Your maximum bet is {cash}")
        input()
        os.system('cls')
        return game_dice()
    elif bet <= 0:
        print("You cannot make a bet of 0 or less!")
        input()
        os.system('cls')
        return game_dice()

    print(f"\nYou bet ${bet}!")
    cash -= bet
    print("\nRolling...")
    time.sleep(1.5)

    dice1, dice2 = random.randint(1,6), random.randint(1,6)
    total = dice1 + dice2

    os.system('cls')

    print(f"You rolled {dice1} and {dice2} (total: {total})\n")

    if total == 12:
        print("JACKPOT! Double sixes!")
        bet *= 5
    elif total in [10, 11]:
        print(f"Great roll! Tripled your bet of ${bet}!")
        bet *= 3
    elif total in [7, 8, 9]:
        print(f"Nice! You doubled your bet of ${bet}!")
        bet *= 2
    else:
        print("Unfortunately, you didn't win anything this time!")
        if dice1 == dice2:
            print(f"However, you rolled doubles and got your bet of ${bet} back!")
            bet *= 1
        else:
            print("You lost this round.")
            bet = 0

    cash += bet
    print(f"\nYou earnt ${bet}.Your balance is now ${cash}!")

    if cash <= 0:
        return bankrupt()

    again = input("\nWould you like to play again? (Y/N):   ").lower()
    if again == "y":
        os.system('cls')
        return game_dice()
    else:
        os.system('cls')
        return game_select()
