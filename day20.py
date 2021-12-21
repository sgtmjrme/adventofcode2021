#!/bin/python

import argparse
from math import sqrt
import numpy
import pdb

def printmap(map):
    for y in map:
        print(''.join(['#' if x==1 else ' ' for x in y]))

def loadFile(file,passes):
    convert_arr = []
    map = []
    with open(file,'r') as f:
        firstLine = f.readline().strip()
        for char in firstLine:
            convert_arr.append(1 if char=='#' else 0)
        f.readline() #Dump a line
        lines = f.read().splitlines()
    xlen = len(lines[0])
    for i in range(2*passes+1):
        map.append([0]*(xlen+4*(passes+1)))
    for line in lines:
        line = line.translate(str.maketrans('#.','10'))
        tmp = [0] * (2*(passes+1))
        for char in line:
            tmp.append(1 if char == '1' else 0)
        tmp.extend([0]*(2*(passes+1)))
        map.append(tmp)
    for i in range(2*passes+1):
        map.append([0]*(xlen+4*(passes+1))) 
    return convert_arr, map

def get_new_value(convert_arr, map, x,y):
    binary = ''
    for j in range(y-1,y+2):
        for i in range(x-1,x+2):
            binary += str(map[j][i])
    assert(len(binary)==9)
    return 1 if convert_arr[int(binary,2)] else 0

def calc_lights(map):
    return sum([sum(x) for x in map])

def fix_border(map,pas):
    val = (pas+1)%2
    for i in range(len(map[0])):
        map[0][i] = val
    for i in range(len(map[-1])):
        map[-1][i] = val
    for i in range(1,len(map)-1):
        map[i][0] = val 
        map[i][-1] = val
        

def p1(convert_arr, map,passes):
    
    #tmpmap just needs to be the same size, I don't actually care much
    tmpmap = []
    for line in map:
        tmpmap.append([0]*len(line))
    for pas in range(passes):
        for i in range(1,len(tmpmap[0])-1):
            for j in range(1,len(tmpmap)-1):
                try:
                    tmpmap[j][i] = get_new_value(convert_arr, map, i, j)
                except:
                    pass
        if convert_arr[0]: fix_border(tmpmap,pas)
        map, tmpmap = tmpmap, map #Swap the two around
    #Now to count
    sum = calc_lights(map)
    print(f'P1: {sum}')
    #Tries - 5565 - low
    
    pass

def p2(file):
    pass

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
    ap.add_argument(
        '--passes',
        required=True,
    )

    args = ap.parse_args()
    passes = int(args.passes)
    convert_arr, map = loadFile(args.file,passes)
    if args.p1: p1(convert_arr, map, 2)
    if args.p2: p1(convert_arr, map, passes)
