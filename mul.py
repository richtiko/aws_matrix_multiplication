# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 21:46:49 2019

@author: Tigran
"""
import sys        
from Matrix import Matrix
from ProcessJob import ProcessJobCreator

import argparse       
parser = argparse.ArgumentParser()

parser.add_argument("-file1", dest="file1", type=str)
parser.add_argument("-file2", dest="file2", type=str)
parser.add_argument("-output", dest="output", type=str)
parser.add_argument("-parallel", dest="parallel", default=False,  type=bool)
args = parser.parse_args()

matrix1 = Matrix() 
matrix2 = Matrix() 


matrix1.read_from_file(args.file1)
matrix2.read_from_file(args.file2)


expected = matrix1.multiply(matrix2)
if args.parallel:    
    mat1 = matrix1.multiply_parallel(matrix2, ProcessJobCreator())
    if mat1.matrix != expected.matrix:
        raise RuntimeError("ERROR");
else:
    mat1 = expected

if args.output != None:
    mat1.save_to_file(args.output)
#print(mat1.matrix)
    
