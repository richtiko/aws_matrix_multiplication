# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 23:24:55 2019

@author: Tigran
"""
import matrix_utils
import ThreadJob

class Matrix:
    def __init__(self, rows=None, columns=None):
        if rows == None or columns == None:
            self.matrix = None
        else:
            self.matrix = matrix_utils.zeros(rows, columns)
        
    def read_from_file(self, filename):
        self.matrix = matrix_utils.read_matrix(filename)
    
    def multiply(self, other_matrix):
        res = Matrix()
        res.matrix = matrix_utils.multiply(self.matrix, other_matrix.matrix)
        return res
            
    def multiply_parallel(self, other_matrix, job_creator = ThreadJob.ThreadJobCreator()):
        res = Matrix()
        res.matrix = matrix_utils.multiply_parallel(self.matrix, other_matrix.matrix, job_creator)
        return res
    
    def save_to_file(self, file):
        matrix_utils.save_to_file(file, self.matrix)
