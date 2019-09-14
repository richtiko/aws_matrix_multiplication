# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 23:24:31 2019

@author: Tigran
"""


import os.path
import time
import subprocess 
from matrix_utils import read_matrix
from matrix_utils import save_to_file
from matrix_utils import get_slice

class ProcessJob:
    
    def __init__(self,filename1,filename2,resultfilename):
        self.filename1 = filename1
        self.filename2 = filename2
        self.resultfilename = resultfilename
        self.result = None
        
    def run(self):
        subprocess.call(["python", "mul.py","-file1",self.filename1, "-file2",self.filename2, "-output", self.resultfilename])
        pass
    def wait(self):
        #TODO: make chack of competion more stable
        while os.path.exists(self.resultfilename) == False:
            time.sleep(0.1)
        time.sleep(1)
        self.result = read_matrix(self.resultfilename)
        
class ProcessJobCreator:
#    def run(self, function):
#        job = Job(function)
#        job.start()
#        return job
    
    def multiply(self, filename1, filename2):
        filename3 = "result_"+filename1+"_"+filename2
        p_job = ProcessJob(filename1, filename2, filename3)
        p_job.run()
        return p_job
        
    def get_slice(self, mat,rows,rowe,cols,cole):
        #filename = os.path.abspath(os.path.curdir+os.path.sep+ "mat_"+str(rows)+"_"+str(rowe)+"_"+str(cols)+"_"+str(cole))
        filename = "mat_"+str(rows)+"_"+str(rowe)+"_"+str(cols)+"_"+str(cole)
        save_to_file(filename, get_slice(mat,rows,rowe,cols,cole))
        return filename
        