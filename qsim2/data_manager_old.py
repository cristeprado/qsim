#!/usr/local/bin/python
# coding: latin-1
from numpy import *
import data_struct
import sys
import os
import os.path as op
import custom_file_reader
import unittest

    ##########################################
    def print_logfiles(self,currOutputFolderPath=""):


        log_per_var_template=

        if currOutputFolderPath!="":
            log_per_var_template=op.normpath(op.join(currOutputFolderPath,log_per_var_template))


        #lista de variables para imprimir




    ##########################################
    def string_output_var(self,varName):

    def time_serie_var(self,varName):
        result=[]
        for t in range(-2,self.T_MAX):
            result.append(self[t].var_dict[varName])

        return result

        #rangos t=-1, t=-2 corresponden a inicializaciones anteriores a t=0,
        #se ubican en los últimos elementos del array.
        # |0|1|2|...|T_MAX|-2||-1|
