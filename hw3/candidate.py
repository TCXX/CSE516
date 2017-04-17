#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:16:07 2017

@author: XIN
"""

import re #regular expression

#To read and parse an input file concerning game data.
def count(inputFile):
    #player data    
    plural = []
    borda = []
    approval = []
    
    #matching rules
    valid_regex = re.compile(r"[[0-9,. \t]+$")
    number_regex = re.compile(r"\d+")
    numberEnd_regex = re.compile(r"\d+$")
    
    try:
        file = open(inputFile, 'r')
        for line in file:
            if len(plural) == 0:
                number = numberEnd_regex.match(line)
                if number is not None:
                    for i in range(0, int(line)):
                        plural.append(0)
                        borda.append(0)
                        approval.append(0)
                    continue
            
            valid = valid_regex.match(line)
            if valid is not None:
                matches = number_regex.findall(line)
                #time = int(matches[0])
                
                #validate preference range
                isValid = True
                for i in range(1, len(matches)):
                    can = int(matches[i])
                    if can > len(borda):
                        isValid = False
                if isValid:
                    #plural
                    can = int(matches[1])
                    plural[can-1] += 1
    
                    #borda
                    for i in range(1, len(matches)):
                        can = int(matches[i])
                        borda[can-1] += len(borda)-i
                        
                    #approval
                    for i in range(1, len(matches)):
                        can = int(matches[i])
                        approval[can-1] += 1
        print("Plurality vote: %s " % plural)
        print("Borda count: %s " % borda)
        print("Approval vote: %s " % approval)
    except IOError:
        sys.exit("IOE Error: Fail to open %s !" % inputFile)
    else:
        file.close()
        #calculate batting average

#main        
if __name__ == "__main__":
    
    inputFile = 'ED-00016-00000001.txt'
    
    count(inputFile)