#!/bin/python

import argparse
import pdb
from collections import deque

def loadFile(file):
    output = {}
    with open(file,'r') as f:
        for line in f:
            (a,b) = line.split('-')
            b=b.strip()
            #Add only if they don't point at start
            if b != 'start': 
                output[a] = [*output[a],b] if a in output else [b]
            if a != 'start': 
                output[b] = [*output[b],a] if b in output else [a]
    del output['end'] #Strip out end - we won't go anywhere else
    return output

def recursion(map: dict,path: list,twiced: bool):
    if path[-1] == 'end':
        map['count'] += 1
    else:
        for next in map[path[-1]]:
            if next.islower():
                if not next in path:
                    recursion(map,[*path,next],twiced)
                elif not twiced:
                    recursion(map,[*path,next],True)
            else:
                recursion(map,[*path,next],twiced)
        

def p1(map):
    #Set count to 0
    map['count'] = 0 #I'll just keep track of count here!
    recursion(map,['start'],True)
    print(f'P1: {map["count"]}')

def p2(map):
    #Set count to 0
    map['count'] = 0 #I'll just keep track of count here!
    recursion(map,['start'],False)
    print(f'P2: {map["count"]}' )

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
        '--file',
        required=True,
        help='File to read',
        dest='file'
    )

    args = ap.parse_args()
    map = loadFile(args.file)
    if args.p1: p1(map)
    if args.p2: p2(map)