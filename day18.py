#!/bin/python

import argparse
from math import ceil, floor
import copy
import pdb

def findEnd(val: str):
    depth=0
    if not '[' in val: return val.find(',')
    for i in range(len(val)):
        if val[i]=='[': depth += 1
        if val[i]==']': depth -= 1
        if depth<1:
            return i+1
    return None

def str2list(val: str):
    #Are we at a regular number?
    if not ',' in val: return int(val)
    #We need to split still
    val=val[1:-1] #Strip the ['s]
    splitpoint = findEnd(val)
    left = val[0:splitpoint]
    right = val[splitpoint+1:]
    return [str2list(left),str2list(right)]

def addExplode(arr: list, direction: int, value: int) -> list:
    if isinstance(arr, int): return arr + value
    arr[direction] = addExplode(arr[direction],direction,value)
    return arr


def recurseExplode(arr: list, depth: int) -> list:
    #Returns [exploding: bool, [leftval,rightval]]
    exploding = False
    if depth >= 4:
        #This starts the explosion
        #pdb.set_trace()
        if isinstance(arr[0],list):
            exploding = True
            arr[1] = addExplode(arr[1],0,arr[0][1])
            retarr = arr[0]
            arr[0]=0
            return exploding, [retarr[0],0]
        elif isinstance(arr[1],list):
            exploding = True
            arr[0] = addExplode(arr[0],1,arr[1][0])
            retarr = arr[1]
            arr[1] = 0
            return exploding, [0,retarr[1]]
    else:
        #This continues explosions
        if isinstance(arr[0],list):
            explode, nums = recurseExplode(arr[0],depth+1)
            if explode:
                #This must return!!!!
                if nums[1] > 0:
                    arr[1] = addExplode(arr[1],0,nums[1])
                    return True, [0,0]
                return True, nums
        if isinstance(arr[1],list):
            explode, nums = recurseExplode(arr[1],depth+1)
            if explode:
                if nums[0] > 0:
                    arr[0] = addExplode(arr[0],1,nums[0])
                    return True, [0,0]
                return True, nums
    return exploding, []

def recurseSplit(arr: list):
    #Handle split
    if isinstance(arr[0],list): 
        if recurseSplit(arr[0]): return True
    elif arr[0] > 9:
        arr[0] = [floor(arr[0]/2),ceil(arr[0]/2)]
        return True
    if isinstance(arr[1],list):
        if recurseSplit(arr[1]): return True
    elif arr[1] > 9:
        arr[1] = [floor(arr[1]/2),ceil(arr[1]/2)]
        return True
    return False

def add(ar1: list, ar2: list) -> list:
    '''
    Adds val1 and val2, returning it after reducing
    '''
    tmparr = [copy.deepcopy(ar1),copy.deepcopy(ar2)]
    exploded = False
    while True:
        #pdb.set_trace()
        exploded = recurseExplode(tmparr,1)[0]
        if not exploded:
            if not recurseSplit(tmparr):
                break #It will break out if not exploded or not split
    return tmparr
    
def magnitude(arr):
    if isinstance(arr,int): return arr
    return 3*magnitude(arr[0])+2*magnitude(arr[1])

def p1(file):
    with open(file,'r') as f:
        #pdb.set_trace()
        curArray=str2list(f.readline().strip())
        for line in f.read().splitlines():
            curArray = add(curArray, str2list(line))
        print(curArray)
        print(f'P1 - {magnitude(curArray)}')

def p2(file):
    max = 0
    with open(file,'r') as f:
        allLines = [str2list(x) for x in f.read().splitlines()]
        for i in range(len(allLines)):
            for j in range(len(allLines)):
                if i != j:
                    mag = magnitude(add(allLines[i],allLines[j]))
                    if mag > max:
                        print(f'New max! {mag}')
                        print(allLines[i])
                        print(allLines[j])
                        max = mag
    print(max)


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
    if args.p1: p1(args.file)
    if args.p2: p2(args.file)
