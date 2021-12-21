#!/bin/python

import argparse
import pdb

def roll_die(cur,max):
    sum = 0
    for i in range(3):
        sum = sum + cur
        cur=cur%max+1
    return sum

def player_new_pos(cur,max,movement):
    return (cur - 1 + movement)%max + 1

def loop(p1_start,p2_start,boardsize,dicemax):
    p1sum=0
    p2sum=0
    dierolls=0
    cur_die = 1
    p1_place = p1_start
    p2_place = p2_start
    while True:
        #P1
        dierolls += 3
        movement = roll_die(cur_die, dicemax)
        cur_die += 3
        p1_place = player_new_pos(p1_place,boardsize,movement)
        p1sum += p1_place
        if p1sum >= 1000:
            return p2sum, dierolls
        #Repeat for P2... I'm lazy today
        dierolls += 3
        movement = roll_die(cur_die, dicemax)
        cur_die += 3
        p2_place = player_new_pos(p2_place,boardsize,movement)
        p2sum += p2_place
        if p2sum >= 1000:
            return p1sum, dierolls

possible_rolls = [3,4,5,6,7,8,9] #This is all the rolls that can exist
wins_for_roll = [27,26,23,17,10,4,1]
scores = [0,0]
def p2_recurse(is_player: bool, player_score: int, opponent_score: int, player_place: int, opponent_place: int):
    for roll in possible_rolls:
        place = player_new_pos(player_place, 10, roll)
        player_score += place
        if player_score >= 1000:
            scores[is_player] += wins_for_roll[roll-3]
            #print(f'Player {is_player} won {wins_for_roll[roll-3]} games! New wins: {scores}')
            return
        p2_recurse(not is_player, opponent_score, player_score, opponent_place, player_place)

def p1(p1_start,p2_start,boardsize,dicemax):
    losing, rolls = loop(p1_start,p2_start, boardsize, dicemax)            
    print(f'P1: {losing * rolls}')

def p2(file):
    pass

def print_winner(arr):
    if arr[0]>arr[1]:
        print(f'Opponent won with {arr[0]} wins against {arr[1]} wins')
    else:
        print(f'Player won with {arr[1]} wins against {arr[0]} wins')

if __name__ == "__main__": 
    ap = argparse.ArgumentParser()
    ap.add_argument(
        '-p1',
        action='store_true',
        help='Run part 1!',
        dest='p1'
    )
    ap.add_argument(
        '-p2',
        action='store_true',
        help='Run part 2!',
        dest='p2'
    )

    args = ap.parse_args()
    #Try1 - 674388 - no info
    #p1(4,8,10,100)
    if args.p1: p1(2,7,10,100)
    if args.p2: 
        #Example
        p2_recurse(True, 0,0,4,8)
        print_winner(scores)
        scores = [0,0]
