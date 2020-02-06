# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:53:58 2019

@author: nitis
"""
# =============================================================================
# Bloom Filter -> m size of sample, n bit array, k hash fxns, p false prob
# =============================================================================
import numpy as np
import math
from bitarray import bitarray
import mmh3

def calculateK(m, n):
    """ Caluclates the optimal K """
    return math.ceil((n/m) * np.log(2))

def falsePositiveProb(m, n, k):
    """ Calculates the false positive probability """
    return (1 - math.exp(-1*k*m/n))**k
    
def getHashValues(username, n, k):
    """ applies k hash functions to the string username """
    hash_values = []
    for i in range(0,k):
        h = mmh3.hash(username, seed=i, signed=False) % n
        hash_values.append(h)
    return hash_values

# =============================================================================
# Caluculating the optimal parameters for the Bloom Filter
# =============================================================================

with open("listed_username_30.txt", 'r', encoding="utf-8") as monthData:
    m = len(monthData.readlines())
    p = 1  ## default 1
    
    for i in range(m*10, m*10+100000):
        kTemp = calculateK(m,i)
        pTemp = falsePositiveProb(m, i, kTemp)
        if pTemp < p:
            k = kTemp
            p = pTemp
            n = i
print("Optimal M is ", m)
print("Optimal N is ", n)
print("Optimal K is ", k)
print("P is ", p)

# =============================================================================
# Creating a Bloom filter with the above m,n,k values
# =============================================================================
BitArray = bitarray(n)
with open("listed_username_30.txt", 'r', encoding="utf-8") as monthData:
    
    BitArray.setall(True)
    
    for line in monthData:
        hash_values = getHashValues(line, n, k)
        for hValue in hash_values:
            BitArray[hValue] = False

# =============================================================================
# Using the Bloom filter on the stream 
# =============================================================================
totalCount = 0
falsePositives = 0
print("++++++++++++++++++++++")
with open("listed_username_365.txt", 'r', encoding="utf-8") as yearData:
    for line in yearData:
        isSpam = False
        totalCount += 1
        hash_values = getHashValues(line, n, k)
        for hValue in hash_values:
            if BitArray[hValue] == False:
                isSpam = True
                break;
        if isSpam == False:
            falsePositives += 1
                
print("False Positive Rate is ", falsePositives/totalCount * 100, "percent")
            
            