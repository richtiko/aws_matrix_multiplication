# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 23:22:19 2019

@author: Tigran
"""
import threading
from matrix_utils import get_slice
from matrix_utils import multiply

class ThreadJob(threading.Thread):
    
    def __init__(self, function):
        self.result = None
        self.function = function
        threading.Thread.__init__(self)
    
    def run(self):
        print (threading.get_ident())
        self.result = self.function()
        
    def wait(self):
        self.join()
        
class ThreadJobCreator:
    def run(self, function):
        job = ThreadJob(function)
        job.start()
        return job
    
    def get_slice(self, mat, rows, rowe, cols, cole):
        return lambda: get_slice(mat, rows, rowe, cols, cole)
    
    def multiply(self, lambda1, lambda2):
        return self.run(lambda: multiply(lambda1(), lambda2()))