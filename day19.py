#!/bin/python

import argparse
from math import sqrt
import numpy
import pdb

rotations = [
      [[1, 0, 0], [0, 1, 0], [0, 0, 1]], #0
      [[0, -1, 0], [1, 0, 0], [0, 0, 1]], #1
      [[-1, 0, 0], [0, -1, 0], [0, 0, 1]], #2
      [[0, 1, 0], [-1, 0, 0], [0, 0, 1]], #3
      [[0, 0, 1], [0, 1, 0], [-1, 0, 0]], #4
      [[0, 0, 1], [1, 0, 0], [0, 1, 0]], #5
      [[0, 0, 1], [0, -1, 0], [1, 0, 0]], #6
      [[0, 0, 1], [-1, 0, 0], [0, -1, 0]], #7
      [[-1, 0, 0], [0, 1, 0], [0, 0, -1]], #8
      [[0, 1, 0], [1, 0, 0], [0, 0, -1]], #9
      [[1, 0, 0], [0, -1, 0], [0, 0, -1]], #10
      [[0, -1, 0], [-1, 0, 0], [0, 0, -1]], #11
      [[0, 0, -1], [0, 1, 0], [1, 0, 0]], #12
      [[0, 0, -1], [1, 0, 0], [0, -1, 0]], #13
      [[0, 0, -1], [0, -1, 0], [-1, 0, 0]], #14
      [[0, 0, -1], [-1, 0, 0], [0, 1, 0]], #15
      [[1, 0, 0], [0, 0, -1], [0, 1, 0]], #16
      [[0, -1, 0], [0, 0, -1], [1, 0, 0]], #17
      [[-1, 0, 0], [0, 0, -1], [0, -1, 0]], #18
      [[0, 1, 0], [0, 0, -1], [-1, 0, 0]], #19
      [[-1, 0, 0], [0, 0, 1], [0, 1, 0]], #20
      [[0, 1, 0], [0, 0, 1], [1, 0, 0]], #21
      [[1, 0, 0], [0, 0, 1], [0, -1, 0]], #22
      [[0, -1, 0], [0, 0, 1], [-1, 0, 0]] #23
    ]

def loadFile(file):
    with open(file,'r') as f:
        lines = f.read().splitlines()
    scanner = 0
    output = {} 
    for line in lines:
        if line.startswith('---'):
            scanner = int(line.split(' ')[2])
            next
        elif ',' in line: #This is hacky...
            #tmparr = [int(x) for x in line.split(',')]
            tmparr = numpy.array([int(x) for x in line.split(',')])
            #tmparr.append(sqrt(sum([x**2 for x in tmparr])))
            output[scanner] = [*output[scanner],tmparr] if scanner in output else [tmparr]
    return output

def get_distances(arr: list) -> list:
    output = {}
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            dist = numpy.sum((arr[i]-arr[j])**2,axis=0)
            if dist in output: output[dist].append([arr[i],arr[j]])
            else: output[dist] = [arr[i],arr[j]]
    return output

def dot(ar1,ar2):
    return [sum(ar1*ar2[0]),sum(ar1*ar2[1]),sum(ar1*ar2[2])]

def test_rotation(arr: list, testval):
    for i in range(len(rotations)):
        #test_val = [arr * rotations[i][0], arr * rotations[i][1], arr * rotations[i][2]]
        test_val = dot(arr,rotations[i])
        if all(test_val == testval):
            return i
    pdb.set_trace()


#def get_matching_points(arr: list, side: int):
#    output = [] 
#    for match in arr:
#        for x in match[side]:
#            if not any([(x == y).all() for y in output]):
#                output.append(x)
#    return output

def p1(file):
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

    args = ap.parse_args()
    positions = loadFile(args.file)
    req_matches = (12*(12-1)/2) #The number of matches for 12 points to be in both scanners
    distances = {x:get_distances(positions[x]) for x in positions}
    scanners_mapped = []
    scanners_to_map = [0]
    total_scanners = 1 #I always match with the starting value!
    while len(scanners_to_map):
        #Handle which scanner to read
        #pdb.set_trace()
        scanner = scanners_to_map.pop()
        if scanner in scanners_mapped: continue #We're going to base everything on scanner 0
        scanners_mapped.append(scanner)

        #We have a scanner we need to map - let's map it then! 
        for newscanner in positions:
            if newscanner in scanners_mapped: continue #I've already mapped it - why do it again?
            if newscanner in scanners_to_map: continue #I've already found a way to map it, but haven't processed it yet - don't look again.  
            count=0
            distance_matches = []
            for distance in distances[scanner]:
                if distance in distances[newscanner]: 
                    distance_matches.append([distances[scanner][distance], distances[newscanner][distance]])
                    count += 1
                    if count >= 3: break
            if count >= 3:  #So apparently there needs to be 12 points that match (I don't think so) but it makes searching easier
                #TODO need to do more here
                
                pdb.set_trace()
                orig_dist1 = distance_matches[0][0] #This is the orig match, first distance
                orig_dist2 = distance_matches[1][0]
                new_dist1 = distance_matches[0][1]
                new_dist2 = distance_matches[1][1]
                base_point = None
                for i in orig_dist1:
                    for j in orig_dist2:
                        if all(i==j):
                            base_point = i
                            break

                if(base_point is None):
                    pdb.set_trace()
                    print('Note to me - my assumption here wasn\'t good!')
                ##I want to make sure I find a match...
                #for i in distance_matches:
                #    if all(movement_point == distance_matches[i][0][0]):
                #        orig_dist2 = distance_matches[i][0][0]
                #        break
                #    if all(movement_point == distance_matches[i][0][1]):
                #        orig_dist2 = 
                matching_point = None
                for i in new_dist1:
                    for j in new_dist2:
                        if all(i==j):
                            matching_point = i
                            break
                if matching_point is None:
                    pdb.set_trace()
                    print('Note to me - my assumption here wasn\'t good!')

                movement_necessary = base_point - matching_point

                #Move it
                orig_opp = None
                if all(orig_dist1[0] == base_point):
                    orig_opp = orig_dist1[1]
                else: orig_opp = orig_dist1[0]
                new_opp = None
                if all(new_dist1[0] == matching_point):
                    new_opp = new_dist1[1]
                else: new_opp = new_dist1[0]
                
                #Find rotation - set so that the opposite point is relative to 0,0,0
                orig_opp = orig_opp - base_point
                new_opp = new_opp - matching_point

                rotation = test_rotation(new_opp,orig_opp)
                #Fix rotations
                for i in range(len(positions[newscanner])):
                    positions[newscanner][i] = dot(positions[newscanner][i],rotations[rotation])
                #Fix movement
                for i in range(len(positions[newscanner])):
                    positions[newscanner][i] = positions[newscanner][i] + movement_necessary

                #TEST
                newcount = 0
                for i in positions[0]:
                    for j in positions[newscanner]:
                        if all(i == j):
                            newcount += 1 
                print(f'newcount is {newcount}')

                
    if args.p1: p1(args.file)
    if args.p2: p2(args.file)
