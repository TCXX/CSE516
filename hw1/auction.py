# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 22:29:06 2017

@author: XIN

Referenced github.com/EvanOman/AuctionAlgorithmCPP
"""

import sys , re #regular expression
from datetime import datetime

number_regex = re.compile(r"\d+")
INF = 100000000
verbose = True

N = 256 #number of agents
M = 10000000 #max value
trial = 1000 #number of trials

# Parse data from given file
def readFile(inputFile):
    try:	
        B = []
        file = open(inputFile, 'r')
        minN = INF
        
        for line in file:
            numbers = number_regex.findall(line)
            temp = []
            for s in numbers:
                temp.append(int(s))
            if (minN > len(numbers)):
                minN = len(numbers)
            B.append(temp)
        
        print("%d agents in total!" %minN)
        
        #determine N and make sure the matrix a square
        C = []
        for i in range(0, len(B)):
            temp = []
            for j in range(0, len(B)):
                temp.append(B[i][j])
            C.append(temp)
        return C
    except IOError:
        sys.exit("IOE Error: Fail to open %s !" % inputFile)
    except:
        printArray(B)
        sys.exit("Error: Unknown error! List has %d elements. " %len(C))
    else:
        file.close()

# Generate a random iarray of n*n within price m
def generateRandomArray(n, m):
    import random
    wtp = []
    for i in range(0, n):
        wtp.append([])
        for j in range(0, n):
            value = random.randint(0, m)
            wtp[i].append(value)
    return wtp

# Print preference values
def printArray(C):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in C]))

# Print solved mathes       
def printSolution(a, C):
    objValue = 0
    for i in range(0, len(a)):
        print ("%d matches %d" %(i, a[i]))
        objValue += C[a[i]][i]
    print("Object Value: %d" %objValue)

#For given scale and preferences values, find optimal matches  
def solveAuction(C):
    #begin timing 
    startTime = datetime.now()    
    
    if (len(C) == 0):
        sys.exit("Error: Empty list of preferences. ")
    
    n = len(C[0])
       
    assignments = [INF] * n
    prices = [0] * n
    epsilon = 1.0
    nIter = 0

    while (epsilon > 1.0/n):
        #reset assignment
        for i in assignments:
            i = INF
         
        ifHasUnassign = True
        while (ifHasUnassign):
            nIter += 1

            # round starts here
            tmpBidded = []
            tmpBids = []
            unassignedIdxList = []
            
            for i in range(0, len(assignments)):
                if (assignments[i] == INF):
                   unassignedIdxList.append(i)
                   
                   optValForI = -INF
                   secOptValForI = -INF
                   optObjForI = -1
                   #secOptObjForI = -1
            
                   for j in range(0, n):
                       curVal = C[j][i] - prices[j]
                       if (curVal > optValForI):
                           secOptValForI = optValForI
                           #secOptObjForI = optObjForI
                           optValForI = curVal
                           optObjForI = j
                       elif (curVal > secOptValForI):
                           secOptValForI = curVal
                           #secOptObjForI = j
                   
                   #highest reasonable bid
                   bidForI = optValForI - secOptValForI + epsilon
                   
                   tmpBidded.append(optObjForI)
                   tmpBids.append(bidForI)
                   
            for j in range(0, n):
                
                #get indices with value
                indices = []
                for k in range(0, len(tmpBidded)):
                    if (tmpBidded[k] == j):
                        indices.append(k)
                
                if (len(indices) > 0):
                    highestBidForJ = -INF
                    i_j = -1
                    for i in range(0, len(indices)):
                        curVal = tmpBids[indices[i]]
                        if (curVal > highestBidForJ):
                            highestBidForJ = curVal
                            i_j = indices[i]
                    for i in range(0, len(assignments)):
                        if (assignments[i] == j):
                            assignments[i]= INF
                            break
                    assignments[unassignedIdxList[i_j]] = j
                    prices[j] += highestBidForJ

            ifHasUnassign = False
            for i in assignments:
                if (i == INF):
                    ifHasUnassign = True
        epsilon *= 0.25
    
    if (verbose):
        printSolution(assignments, C)
    
    #time for solving one single trial
    endTime = datetime.now()
    usedTime = endTime - startTime
    print(str(nIter) + " iterations, " 
        + str(n) +" agents in " 
        + str(usedTime))
    
# Main
if __name__ == "__main__":
    startTime = datetime.now()   
    
    # Randomize instances if no arguments for input file
    if len(sys.argv) < 2:
        for i in range(0, trial):
            C = generateRandomArray(N, M)
            solveAuction(C) 
            #time for solving multiple trials
        endTime = datetime.now()
        usedTime = endTime - startTime
        print(str(trial) +" trials, " + str(N) + " agents of max " 
            + str(M) + " in " 
            + str(usedTime))
    else:
        C = readFile(sys.argv[1])
    
        # Print the instance
        printArray(C)
        solveAuction(C)
    

    
    
    