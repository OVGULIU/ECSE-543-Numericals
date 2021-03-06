# -*- coding: utf-8 -*-
"""
Sharhad Bashar
260519664
ECSE 543
Assignment 1
Question 1
basicDefinitions.py
""" 

import math
from scipy import random
import numpy as np
import csv

######################################################################################
#Function that checks if a matrix is 1D or 2D 
def is1Dor2D (A):
    while True:
        try:
            length = len(A[0]) #If true, A is 2D
            return A
            break
        except TypeError: #else A is 1D
            return [A]
            break
######################################################################################
#function that creates floats from lists
def list2float(A):  
    length = len(A)
    floatA = [0 for x in range(length)]
    for i in range (length):
        numVal = ''
        stringVal = list(str(A[i]))
        for j in range (1,len(stringVal)-1,1):        
            numVal = numVal + stringVal[j]
        floatVal = float(numVal)
        floatA [i] = floatVal
    return floatA
######################################################################################
#Function that transposes a Matrix            
def matTranspose(A):
    A = is1Dor2D(A)
    rowsA = len(A)
    colsA = len(A[0])
    C = [[0 for rows in range (rowsA)] for cols in range(colsA)]
    for i in range (colsA):
        for j in range (rowsA):
            C[i][j] = A[j][i]
    return C
######################################################################################
#Function that adds or subtracts two matricies
def matrixAddorSub(A,B,operation):
    A = is1Dor2D(A)
    B = is1Dor2D(B)    
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])  
    if (rowsA == rowsB and colsA == colsB):
        C = [[0 for row in range(colsA)] for col in range(rowsA)]
        if (operation == 'a'):
            for i in range (rowsA):
                for j in range (colsA):
                    C[i][j] = A[i][j]+B[i][j]
        elif (operation == 's'):
            for i in range (rowsA):
                for j in range (colsA):
                    C[i][j] = A[i][j]-B[i][j]                 
    return C    
######################################################################################
#Function that multiplies two matricies    
def matrixMult (A, B):
    A = is1Dor2D(A)
    B = is1Dor2D(B)
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])      
    if (rowsA == colsB or colsA == rowsB):
        C = [[0 for row in range(colsB)] for col in range(rowsA)]
        for i in range(rowsA):
            for j in range(colsB):
                for k in range(colsA):
                # Create the result matrix
                # Dimensions would be rows_A x cols_B
                    C[i][j] += A[i][k] * B[k][j]
    else:
      print ("Cannot multiply the two matrices. Incorrect dimensions.")
      return
    return C   
######################################################################################
#Function that creates a diagonal matrix   
def diogMat (A):
    length = len(A)
    floatA = [0 for x in range(length)]
    for i in range (length):
        numVal = ''
        stringVal = list(str(A[i]))
        for j in range (1,len(stringVal)-1,1):        
            numVal = numVal + stringVal[j]
        floatVal = float(numVal)
        floatA [i] = floatVal
    diognalMatrix = [[0 for x in range(length)] for y in range(length)]
    for i in range (length):
        diognalMatrix[i][i] = 1/floatA[i]
    return diognalMatrix
######################################################################################
#Function that creates random A, given a length input
def randomSPD(length):
    A = [[0 for x in range(length)] for y in range(length)]
    L = random.rand(length,length)
    A = np.dot(L,L.T)    
    return A    
######################################################################################
#Function that performs the Cholesky decomposition and returns L
def cholesky(A,length):
    global sum 
    L = [[0 for x in range(length)] for y in range(length)]
    for i in range(length):
        for k in range(i + 1):
            sum = 0
            for j in range(k):
                sum += L[i][j] * L[k][j]    
            if (i == k):
                L[i][k] = math.sqrt(abs(A[i][i] - sum))
            else: 
                L[i][k] = (A[i][k]-sum) / L[k][k] 
    return L
######################################################################################
#Function that solves y in Ly = b
def forwElim (L,b,length):    
    b = list2float(b)
    global sum
    y = [0 for x in range (length)]
    for i in range (length):
        sum = 0.00         
        for j in range (i):
            sum += L[i][j] * y[j]
        y[i] = (b[i]-sum)/L[i][i]
    return y
###################################################################################### 
#Function that solves for x in L^Tx = y
def backSub (L,y,length):
    global sum
    X = [0 for x in range(length)]
    for i in range (length - 1, -1, -1):
        sum = 0
        for j in range (i + 1, length, 1):
            sum += L[j][i] * X[j]
        X[i] = (y[i]-sum) / L[i][i]
    return X
######################################################################################
#Solves the (AYA^T)Vn = A(J_YE) Equation
def voltageSolver(incidentMatrix, E, J, R):
    #Equation to solve: (A*Y*A^T)Vn = A(J-Y*E)
    #step_1 = Y*E
    #Step_2 = J-Step_1
    #Step_3 = A*Step_2
    #Step_4 = A^T
    #Step_5 = Y*Step_4
    #Step_6 = A*Step_5    
    #Gives B    
    Y = diogMat(R)
    Step_1 = matrixMult(Y,E)
    Step_2 = matrixAddorSub(J,Step_1,'s')
    Step_3 = matrixMult(incidentMatrix,Step_2)    
    #Gives A
    Step_4 = matrixMult(incidentMatrix,Y)
    Step_5 = matTranspose(incidentMatrix)
    Step_6 = matrixMult(Step_4,Step_5)
    
    #computes the volatage
    length = len(Step_6)
    Step_7a = cholesky(Step_6,length)
    Step_7b = forwElim(Step_7a,Step_3, length)
    Step_7c = backSub(Step_7a,Step_7b, length)    
    return Step_7c
######################################################################################    
#Reads values from the csv file
def readCell(x, y):
    with open('testCircuit_1D.csv', 'r') as data:
        reader = csv.reader(data)
        yCount = 0
        for n in reader:
            if (yCount == y):
                rawCellValue = n[x]
                cellValue = float(rawCellValue)
                return cellValue
            yCount += 1    
#######################################################################################    
