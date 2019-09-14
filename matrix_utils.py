# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 23:23:28 2019

@author: Tigran
"""
import threading

def read_matrix(filename):
    print("read_matrix from ",filename)
    fh = open(filename,"r")
    matrix1 = []
    line = fh.readline()
    line = line.strip(' \n\r')
    while len(line) != 0:
        #print(line)
        
        row = list(map(int, line.split(" ")))
        if len(row) != 0:
            matrix1.append(row)  
        line = fh.readline()
        line = line.strip(' \n\r')
        
    fh.close()       
    return matrix1

def save_to_file(filename, mat):
    fh = open(filename,"w")

    rows, cols = get_dimentions(mat)
    print("save_to_file ",filename," ",rows,"x",cols)
    for i in range(0,rows):
        for j in range(0,cols):
            fh.write("%d " % mat[i][j])
        fh.write("\n")
    fh.flush()
    fh.close()

def zeros(rows, cols=1):
    col = []
    for j in range(0, cols):
        col.append(0)
    arr = []
    for i in range(0,rows):
        arr.append(col.copy())
    return arr
    
def multiply(mat1, mat2):
    
    rows = len(mat1)
    cols = len(mat2[0])
    line = len(mat1[0])
    print ("multiply ",rows,"X",len(mat1[0])," and ",len(mat2)," X ",cols)
    if len(mat1[0]) != len(mat2) :
        raise RuntimeError("matrix does not match",rows,"X",len(mat1[0])," and ",len(mat2)," X ",cols )
    mat3 = zeros(rows,cols)
    
    for i in range(0,rows):
        for j in range(0,cols):
            for k in range(0,line):
                mat3[i][j] += mat1[i][k]*mat2[k][j]
    return mat3

def get_slice(mat, rows, rowe, cols, cole):
    print ("thread: ",threading.get_ident()," get_slice")
    new_rows = rowe - rows
    new_col = cole - cols
    arr = zeros(new_rows,new_col)
    for i in range(0,new_rows):
        for j in range(0,new_col):
            arr[i][j] = mat[rows+i][cols+j]
    return arr

def check_dimentions(mat1, mat2):
    mat1_cols = len(mat1[0])
    mat2_rows = len(mat2)
    if mat1_cols != mat2_rows:
        mat1_rows = len(mat1)
        mat2_cols = len(mat2[0])
        raise RuntimeError("matrix does not match",mat1_rows,"X",mat1_cols," and ",mat2_rows," X ",mat2_cols)

def get_dimentions(mat1):
    return len(mat1), len(mat1[0])

def multiply_parallel(mat1, mat2, job_creator):
    check_dimentions(mat1, mat2)
    mat1_rows, mat1_cols = get_dimentions(mat1)
    mat2_rows, mat2_cols = get_dimentions(mat2)
    
    mat1_middle_raw = int(mat1_rows/2)
    mat2_middle_col = int(mat1_cols/2)
    mat1_middle_col = mat2_middle_raw = int(mat2_rows/2)
    
    part_1 = job_creator.multiply(job_creator.get_slice(mat1, 0, mat1_rows, 0, mat1_middle_col), job_creator.get_slice(mat2, 0, mat2_middle_raw, 0, mat2_middle_col))
    part_2 = job_creator.multiply(job_creator.get_slice(mat1, 0, mat1_rows, 0, mat1_middle_col), job_creator.get_slice(mat2, 0, mat2_middle_raw, mat2_middle_col, mat2_cols))
    part_3 = job_creator.multiply(job_creator.get_slice(mat1, 0, mat1_middle_raw, mat1_middle_col, mat1_cols), job_creator.get_slice(mat2, mat2_middle_raw, mat2_rows, 0, mat2_cols))
    part_4 = job_creator.multiply(job_creator.get_slice(mat1, mat1_middle_raw, mat1_rows, mat1_middle_col, mat1_cols), job_creator.get_slice(mat2, mat2_middle_raw, mat2_rows, 0, mat2_cols))
    
    part_1.wait()
    part_3.wait()
    arr = zeros(mat1_rows,mat2_cols)
    for i in range(0,mat1_middle_raw):
        for j in range(0,mat2_middle_col):
            arr[i][j] = part_1.result[i][j]+part_3.result[i][j]
    
    part_2.wait()
    for i in range(0,mat1_middle_raw):
        for j in range(mat2_middle_col, mat2_cols):
            arr[i][j] = part_2.result[i][j-mat2_middle_col]+part_3.result[i][j]
    
    part_4.wait()
    for i in range(mat1_middle_raw,mat1_rows):
        for j in range(0,mat2_middle_col):
            arr[i][j] = part_1.result[i][j] + part_4.result[i-mat1_middle_raw][j]

    for i in range(mat1_middle_raw,mat1_rows):
        for j in range(mat2_middle_col,mat2_cols):
            arr[i][j] = part_2.result[i][j-mat2_middle_col] + part_4.result[i-mat1_middle_raw][j]
    return arr
    
#                     ________________
#                     |       |       | 
#                     |   e   |   f   | 
#                     |_______|_______| 
#                     |       |       | 
#                     |   g   |   h   | 
#                     |_______|_______|
#________________     ________________
#|       |       |    |       |       | 
#|   a   |   b   |    |a*e+b*g|a*f+b*h| 
#|_______|_______|    |_______|_______| 
#|       |       |    |       |       | 
#|   c   |   d   |    |c*e+d*g|c*f+d*h| 
#|_______|_______|    |_______|_______|
#
#_________
#|       |
#|  a*e  |
#|_______|
#|       |
#|  c*e  |
#|_______|
#
#_________
#|       |
#|  a*f  |
#|_______|
#|       |
#|  c*f  |
#|_______|
#
#________________
#|       |       |
#|  b*g  |  b*h  |
#|_______|_______|
#
#
#________________
#|       |       |
#|  d*g  |  d*h  |
#|_______|_______|


        