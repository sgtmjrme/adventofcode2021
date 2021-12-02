#!/bin/python

import argparse
import pdb
from collections import deque

def p1(file):
    count=0
    with open(file,'r') as f:
        prev=int(f.readline())
        for num in f:
            num=int(num)
            if prev != None:
                if (num > prev): count += 1
            prev = num
    print('p1:{0}'.format(count))

def p2(file):
    count=0
    arr = deque()
    prevsum=0
    with open(file,'r') as f:
        for x in range(3):
            arr.append(int(f.readline()))
        prevsum=sum(arr)
        arr.pop()
        for num in f:
            arr.append(int(num))
            newsum = sum(arr)
            if newsum > prevsum: count += 1
            prevsum=newsum
            arr.popleft()
    print('p2:{0}'.format(count))

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