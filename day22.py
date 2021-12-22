#!/bin/python

import argparse
import pdb

def loadFile(file):
    with open(file,'r') as f:
        lines = f.read().splitlines()
    steps = []
    for line in lines:
        if line.startswith('#'): break
        tmp = []
        split1 = line.split(' ')
        tmp.append(1 if split1[0] == 'on' else 0)
        split2 = [sorted([int(z) for z in y.split('..')]) for y in [x.split('=')[1] for x in split1[1].split(',')]]
        tmp.extend(split2)
        steps.append(tmp)
    return steps


def p1(steps, limit):
    map = {}
    for step in steps:
        for x in range(max(-limit,step[1][0]),min(limit,step[1][1]+1)):
            if x<-limit or x>limit: continue
            for y in range(max(-limit,step[2][0]),min(limit,step[2][1]+1)):
                if y<-limit or y>limit: continue
                for z in range(max(-limit,step[3][0]),min(limit,step[3][1]+1)):
                    if z<-limit or z>limit: continue
                    map[f'{x},{y},{z}']=step[0]
    print(f'P1: {sum(map.values())}')

def axis_not_intersect(axis1: list, axis2: list):
    return axis2[0] > axis1[1] or axis2[1] < axis1[0]

def cubes_intersect(cube1: list, cube2: list):
    for val in range(3):
        if axis_not_intersect(cube1[val],cube2[val]):
            return False

    return True

def get_intersections(cube1, cube2):
    if not cubes_intersect(cube1, cube2):
        return [cube1]
    #Ok, we need to get the border cubes
    #Cube1 will ALWAYS be the active cube
    output_cubes = []
    x,y,z=0,1,2
    if cube1[z][1] > cube2[z][1]:
        #Top
        output_cubes.append([cube1[x],cube1[y],[cube2[z][1]+1,cube1[z][1]]])
    if cube1[z][0] < cube2[z][0]:
        #Bottom
        output_cubes.append([cube1[x],cube1[y],[cube1[z][0],cube2[z][0]-1]])
    newz = [max(cube1[z][0],cube2[z][0]),min(cube1[z][1],cube2[z][1])]
    if cube1[y][1] > cube2[y][1]:
        #Right
        output_cubes.append([cube1[x],[cube2[y][1]+1,cube1[y][1]],newz])
    if cube1[y][0] < cube2[y][0]:
        #Left
        output_cubes.append([cube1[x],[cube1[y][0],cube2[y][0]-1],newz])
    newy = [max(cube1[y][0],cube2[y][0]),min(cube1[y][1],cube2[y][1])]
    if cube1[x][1] > cube2[x][1]:
        #Front
        output_cubes.append([[cube2[x][1]+1,cube1[x][1]],newy,newz])
    if cube1[x][0] < cube2[x][0]:
        #Back
        output_cubes.append([[cube1[x][0],cube2[x][0]-1],newy,newz])
    return output_cubes

def sumCubes(cubes):
    total = 0
    x,y,z=0,1,2
    for cube in cubes:
        total += (cube[x][1]-cube[x][0]+1)*(cube[y][1]-cube[y][0]+1)*(cube[z][1]-cube[z][0]+1)
    return total

def p2(steps):
    #We should deal with the cube intersections now
    allCubes = []
    for step in steps:
        newCubes = []
        for cube in allCubes:
            newCubes.extend(get_intersections(cube, step[1:]))
        #pdb.set_trace()
        allCubes = newCubes
        if step[0]:
            allCubes.extend([step[1:]])
    assert(any([[cubes_intersect(x,y) for x in allCubes] for y in allCubes]))
    print(f'P2: {sumCubes(allCubes)}')

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
        dest='file',
        required=True
    )

    args = ap.parse_args()

    steps = loadFile(args.file)

    if args.p1: p1(steps,50)
    if args.p2: p2(steps)