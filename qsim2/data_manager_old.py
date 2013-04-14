#!/usr/local/bin/python
# coding: latin-1
from numpy import *
import data_struct
import sys
import os
import os.path as op
import custom_file_reader
import unittest


        self[0].subsid_h=self.subsid_h_0
        self[0].subsid_vi=self.subsid_vi_0

    #inicializa la matriz S_vi, cumpliendo las restricciones de regulación por zona y el total agregado de oferta (solución factible).
        self.init_S_vi()

        #inicializa los parámetros gamma al valor del archivo
        self[0].gamma_vi=self.gamma_vi_0

        #inicializa S_vi al valor actual en los períodos -1 y -2
        self[-1].S_vi=self[0].S_vi.copy()
        self[-2].S_vi=self[0].S_vi.copy()


    ##########################################
    def print_logfiles(self,currOutputFolderPath=""):

        #templates para los nombres de los archivos log
        log_general="log.txt"
        log_per_var_template="log_{var}.txt"

        if currOutputFolderPath!="":

            log_general=op.normpath(op.join(currOutputFolderPath,log_general))
            log_per_var_template=op.normpath(op.join(currOutputFolderPath,log_per_var_template))

        header_template="""DATA: "+ self.NOMBRE_DATA
@@@@@@@@@@@@@@@@@@@@@@@@@@
"N_h=" {N_h}
"N_vi=" {N_vi}
"T_MAX=" {T_MAX}
@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""

        #lista de variables para imprimir
        varname_list=["H_h","b_h","P_h_vi","b_h_vi","B_h_vi","r_vi",
                "S_vi","H_h_vi","I_h_vi","I2","converge","gamma_vi"]

        #abre stream para log general
        logfile_name=log_general.format(
                mod=mod,
                data=self.NOMBRE_DATA)
        ff_gen=open(logfile_name,'w')

        #imprime header en log general
        ff_gen.write(header_template.format(N_h=self.N_h,
                N_vi=self.N_vi,
                T_MAX=self.T_MAX))

        for x in varname_list:
            #imprime cada variable en log general
            ff_gen.write(self.string_output_var(x))

            #crea log de cada variable
            logfile_name=log_per_var_template.format(
                    mod=mod,
                    data=self.NOMBRE_DATA,
                    var=x)

            #imprime log de cada variable
            ff_var=open(logfile_name,'w')
            ff_var.write(self.string_output_var(x))
            ff_var.close()

        ff_gen.close()


    ##########################################
    def string_output_var(self,varName):
        result=[varName+"\n"]
        for t in range(-2,self.T_MAX):
            result.append("t={}\n".format(t))
            result.append("{}\n".format(self[t].var_dict[varName]))
        result.append("\n")

        return("".join(result))

    def time_serie_var(self,varName):
        result=[]
        for t in range(-2,self.T_MAX):
            result.append(self[t].var_dict[varName])

        return result

        #rangos t=-1, t=-2 corresponden a inicializaciones anteriores a t=0,
        #se ubican en los últimos elementos del array.
        # |0|1|2|...|T_MAX|-2||-1|
