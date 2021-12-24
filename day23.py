#!/bin/python

import argparse
import pdb
import sys

def loadExample():
    #I'm just going to build this myself
    hallway = ['.','.',0,'.',1,'.',2,'.',3,'.','.']
    #rooms = [['A','B'],['D','C'],['C','B'],['A','D']]
    rooms = ['ADDB','DBCC','CABB','ACAD']
    return hallway, rooms

def loadFile():
    #I'm just going to build this myself
    hallway = ['.','.',0,'.',1,'.',2,'.',3,'.','.']
    rooms = ['CD','AB','DA','BC']
    return hallway, rooms

def n2l(num):
    return 'ABCD'[num]

def l2n(l):
    return 'ABCD'.find(l)

def nPos(num):
    if num==0: return 2
    if num==1: return 4
    if num==2: return 6
    if num==3: return 8

def l2c(l):
    return [1,10,100,1000][l2n(l)]

def roomHelper(room, num):
    return '.' if len(room) < num else room[num-1]

def printmap(hallway, rooms, roomSize):
    print('01234567890')
    print(''.join([str(val) for val in hallway]))
    for i in range(roomSize):
        print(f' #{roomHelper(rooms[0],roomSize-i)}#{roomHelper(rooms[1],roomSize-i)}#{roomHelper(rooms[2],roomSize-i)}#{roomHelper(rooms[3],roomSize-i)}#')

def roomsComplete(rooms,roomSize):
    return all([rooms[i] == n2l(i)*roomSize for i in range(len(rooms))])
    #for i in range(len(rooms)):
    #    if rooms[i] != n2l(i)*roomSize: return False
    #return True

def getCanMove(roomSize, hallway, rooms, energy, minenergy,path):
    #printmap(hallway, rooms,roomSize)
    if energy >= minenergy: return minenergy
    if roomsComplete(rooms,roomSize): 
        print(f'Found a new minimum energy! {energy} Path {path}')
        return energy
    empty = []
    #Prefer moving from the hallway
    for i in range(len(hallway)):
        val = hallway[i]
        if val=='.': 
            empty.append(i)
            continue #Empty space
        elif isinstance(val,int): continue
        #It's a letter
        target=l2n(val)
        door=nPos(target)
        direction = 1 if door > i else -1
        canMakeIt = True
        for j in range(i+direction,door,direction):
            if isinstance(hallway[j],int): continue
            if hallway[j] in 'ABCD':
                canMakeIt = False
                break
        if canMakeIt:
            #Can I go into this room? 
            pathenergy = sys.maxsize
            if len(rooms[target]) < 4:
                #Does it contain anything else?
                if any([thing != val for thing in rooms[target]]): continue
                dist = abs(door - i) + roomSize-len(rooms[target])
                cost = dist * l2c(val)
                newhallway = hallway.copy()
                newrooms = rooms.copy()
                newhallway[i] = '.'
                newrooms[target] += val 
                newpath = f'{path}H{i}-{val}-{target}={cost},'
                pathenergy = getCanMove(roomSize, newhallway,newrooms,energy + cost, minenergy,newpath)
            if pathenergy < minenergy: minenergy = pathenergy
    #If I can't move from the hallway, move from a room
    for i in range(len(rooms)):
        room = rooms[i]
        if len(room) < 1: continue #Nothing to do here... Nobody is home
        #Are the roommates in here the correct ones? 
        toMove = False
        for j in range(len(room)-1,-1,-1):
            if n2l(i) != room[j]: 
                toMove = True
                break #this room is already set, nothing to do
        if not toMove: continue #This room has the correct people, don't do anything
        #So we have to evict somebody to the hallway
        newrooms = rooms.copy()
        char = newrooms[i][-1]
        newrooms[i] = newrooms[i][0:-1]
        for j in empty:
            #These are the empty hallway spaces we can put someone in
            door=nPos(i)
            direction = 1 if door < j else -1
            canMakeIt = True
            for k in range(door + direction,j,direction):
                if isinstance(hallway[k],int): continue
                if hallway[k] in 'ABCD':
                    canMakeIt = False
                    break
            if not canMakeIt: continue
            newhallway = hallway.copy()
            newhallway[j] = char
            cost = l2c(char) * (roomSize - len(newrooms[i]) + abs(j-nPos(i)))
            newpath = f'{path}R{i}-{char}-{j}={cost},'
            pathenergy = getCanMove(roomSize, newhallway,newrooms,energy + cost, minenergy,newpath)
            if pathenergy < minenergy: minenergy = pathenergy
    #If I got here... we're done?  Maybe? 
    return minenergy


def p1(hallway, rooms, energy = 0, minenergy = sys.maxsize) -> int: #The path length is returned
    empString = ''
    SampleLower = 18500
    print(f'P1: {getCanMove(2, hallway,rooms,energy,SampleLower,empString)}')
    printmap(hallway,rooms)

def p2(hallway, rooms, guess, energy=0, minenergy = sys.maxsize):
    empString = ''
    print(f'P2: {getCanMove(4, hallway,rooms,energy,guess,empString)}')
    printmap(hallway,rooms,4)

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
    ap.add_argument(
        '-ex',
        action='store_true',
        help='Run example',
        dest='ex'
    )
    ap.add_argument(
        '-g',
        dest='guess',
        default=sys.maxsize
    )

    args = ap.parse_args()

    hex,rex = loadExample()
    #pdb.set_trace()
    if args.ex: p2(hex,rex,int(args.guess))

    hallway, rooms = loadFile()
    p2hallway = hallway.copy()

    if args.p1: p1(hallway,rooms)

    #Part 2 actually can be the same as part 1... just with a bigger input
      #D#C#B#A#
      #D#B#A#C#
    rooms = ['CDDD','ABCB','DABA','BCAC']
    printmap(hallway,rooms,4)
    if args.p2: p2(p2hallway,rooms, int(args.guess))