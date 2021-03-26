import os
import time
from colorama import Fore, Style
import random
from array import array

#Vars
limit = 7.5
max_num = 21
deal = False
nodeal = True
card_type = ['bastos','oros','copas', 'espadas']
card_value = [1,2,3,4,5,6,7,8,9,10,11,12]
hand = []
handParsed = []
hand_total = 0

def Rules():
    print('#######################################################################################################################################################')
    print('#            Uno de los jugadores ha de actuar de Banca, el cual puede venderla al jugador que desee por la cantidad que crea justa.                  #')
    print('#                          La banca reparte una carta boca abajo a cada jugador y a sí misma. Cada jugador apuesta y,                                 #')
    print('#     por turno, puede pedir cartas a la banca, con la condición de que una sola de las que tiene permanezca tapada, de modo que si destapa todas,    #')
    print('#  la banca se la da tapada, y si guarda una boca abajo, la banca le da otra destapada. Se puede plantar en cualquier momento si ha llegado a siete   #')
    print('#                   y media, o si está por debajo. Si tiene siete y media o se pasa, no tiene que descubrir la carta tapada.                          #')
    print('#                                                                                                                                                     #')
    print('#             Cuando todos los jugadores han jugado, le toca el turno a la banca, que descubre su carta y juega, a la vista de todos,                 #')
    print('#                   hasta plantarse o pasarse. Gana todo aquel que tenga más puntos que la banca, sin pasar de siete y media.                         #')
    print('#######################################################################################################################################################')
    print('')
    start = False
    while start == False:
        print('¿Deseas empezar a jugar?')
        seleccion = input('>> ')
        if seleccion.upper() == 'S':
            Main()
        elif seleccion.upper() == 'N':
            Rules()

def barajar():
    newCardParsed = ""
    while True:
        new_card = card_value[random.randint(0, 9)] #Add a random card to hand
        new_type = card_type[random.randint(0,3)] #Add a random
        if new_card == 10: #Add new value to the card parsed
            newCardParsed = "sota"
            new_card = 0.5
        elif new_card == 11:
            newCardParsed = "caballo"
            new_card = 0.5        
        elif new_card == 12:
            newCardParsed = "rey"
            new_card = 0.5
        else:
            newCardParsed = str(new_card)
        if newCardParsed not in hand:
            break
    hand.append(newCardParsed)
    handParsed.append(newCardParsed+ " de "+ new_type)
    return new_card, newCardParsed, new_type


def crupier(money, bet_money, hand_total):
    #cartas de la maquina
    hand_totalm = 0
    while hand_totalm <= 6:
        new_cardm, newCardParsedm, new_typem = barajar()
        print("El croupier ha sacado un "+newCardParsedm+" de "+new_typem + '\n')
        hand_totalm = hand_totalm + new_cardm

    faltante = 7.5-hand_total
    faltantem = 7.5-hand_totalm
    
    if faltante > faltantem and faltantem >= 0:
        print(Fore.RED + 'Has perdido' + Fore.RED)
        print("Tu apuesta ha sido " + Fore.GREEN + str(bet_money) + '€' + Fore.WHITE)
        print('Has perdido' + Fore.RED + ' +'  + str(bet_money) + '€' + Fore.WHITE)
    if faltante < faltantem or not faltantem >= 0:
        print(Fore.GREEN + 'Has ganado' + Fore.WHITE)
        print(Fore.WHITE + "Tu apuesta ha sido" + Fore.GREEN + str(bet_money), '€' + Fore.WHITE)
        print(Fore.WHITE + 'Has ganado' + Fore.GREEN + '+' + str(bet_money*2) + '€' + Fore.WHITE)

        money = money + (bet_money * 2)
    return money 


def AddCard(hand_total): #Draw card and add the card on hand
    new_card, newCardParsed, new_type = barajar()
    value = newCardParsed + ' de ' + new_type #Set the name of the cars without the value
    
    hand_total = hand_total + new_card #Add card value to the hand (Only Value)
    print('')
    print("- Has sacado un " + value + '\n') #Print the name with number and type
    print('Tus cartas:')
    i = 0
    for item in handParsed:
        print("-> " + handParsed[i] + " ")
        i += 1
    return hand_total, new_card


def Check(hand_total, new_card, money, bet_money): #Check if the player wins the game

    if hand_total > limit:
        print(Fore.RED +  'Has perdido' + Fore.WHITE)
    elif hand_total == limit:
        print(Fore.GREEN +  'Has ganado' + Fore.WHITE)
        money = money + (bet_money * 2)
    elif hand_total < limit:
        lost = limit - hand_total
        print('\nTe has quedado a ' + str(lost))
    return money

def Bet(money):

    while True:
        print('')
        print('Tu dinero:' + Fore.GREEN + str(money) + '€' + Fore.WHITE)
        print('')
        print('Cuanto desea apostar? (Apuesta mínima' + Fore.GREEN + ' 2€' + Fore.WHITE + ')')
        print('')
        bet_money = input('>> ' + Fore.GREEN)
        print(Fore.WHITE + "")
        try:
            bet_money = int(bet_money)
        except:
            continue
        if bet_money > money:
            print("No apuestes mas de lo que tienes...")
            continue
        if 1 >= bet_money:
            print("Tienes que apostar algo...")
            continue
        print('Desea apostar ' + Fore.GREEN + str(bet_money) + '€?' + Fore.WHITE)

        sel = input('>> ')
        sel = sel.lower()

        if sel == "s":
            print('Has apostado ' + Fore.GREEN + str(bet_money) + '€' + Fore.WHITE) 
            money = money - bet_money
            break

        elif sel == "n":
            print('Elige otra cantidad')

        else: 
            print('Elige una cantidad válida')

    return money, bet_money

def Start(hand_total, money): #Open start function
    money, bet_money = Bet(money)
    hand_total, new_card = AddCard(hand_total)
    money = Check(hand_total, new_card, money, bet_money)
    while hand_total < limit:
        ans = input('\nDeseas continuar?\n >>  ')
        print('')
        if ans.lower() == "s":
            hand_total, new_card = AddCard(hand_total)
            money = Check(hand_total, new_card, money, bet_money)
        elif ans.lower() == "n":
            money = crupier(money, bet_money, hand_total)
            break
    return money
    

def Main():
    money = 100
    os.system('cls')
    start = False
    while start == False:
        hand_total = 0
        print('###############################################################################################')
        print('#                                                                                             #')
        print('#                     Este es el sistema de juego. ¿Qué deseas hacer?                         #')
        print('#                                                                                             #')
        print('###############################################################################################')
        print('#                                                                                             #')
        print('#                                1 - Iniciar juego                                            #')
        print('#                                2 - Leer normas                                              #')
        print('#                                3 - Salir del juego                                          #')
        print('#                                                                                             #')
        print('###############################################################################################')
        print('')
        sel = input('>> ')
        start = False
        romper1 = False
        if sel == '1':
            money = Start(hand_total, money)
            romper1 = True
            break
        elif sel == '2':
            os.system("cls")
            
        elif sel == '3':
            exit()
            break
        if romper1:
            os.system('cls')
            break
    
    while 1:
        hand_total = 0
        if money <= 0:
            print('')
            input('Te has quedado sin dinero, si quiere volver a jugar reinicia el juego.')
            break
            
    return hand, handParsed

def RestartGame(hand_total, money, hand,handParsed):
    os.system('clear')
    for i in handParsed:
        handParsed.pop()
    time.sleep(0.5)
    money = Start(hand_total, money)
    return hand, handParsed

if __name__ == "__main__":
    Main()
