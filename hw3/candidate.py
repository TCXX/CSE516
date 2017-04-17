#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:16:07 2017

@author: XIN
"""

import sys, operator
import re #regular expression

#To read and parse an input file concerning game data.
def readFile(inputFile):
    #player data    
    votes = []
    
    #matching rules
    valid_regex = re.compile(r"[[0-9,. ]+$")
    number_regex = re.compile(r"\d+")
    numberEnd_regex = re.compile(r"\d+$")
    
    try:
        file = open(inputFile, 'r')
        for line in file:
            if len(votes) == 0:
                number = numberEnd_regex.match(line)
                if number is not None:
                    for i in range(0, int(line)):
                        votes.append(0)
            
            #validate format
            valid = valid_regex.match(line)
            if valid is not None:
                #extract characters
                matches = number_regex.findall(line)
                time = int(matches[0])
                for i in range(1, len(matches)):
                    can = int(matches[i])
                    if can <= len(votes):
                        votes[can-1] += time
        return votes
    except IOError:
        sys.exit("IOE Error: Fail to open %s !" % inputFile)
    else:
        file.close()
        #calculate batting average

#main        
if __name__ == "__main__":
    
    inputFile = 'ED-00016-00000001.txt'
    
    theList=readFile(inputFile)
    print(theList)