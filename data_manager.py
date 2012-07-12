#!/usr/local/bin/python
# coding: latin-1
from numpy import *
import data_struct

class DataManager(list):
    """Clase que contiene la data para los modelos"""

    def __init__(self):

        self.T_MAX=3

        self.N_h=2
        self.N_vi=2

        list.__init__(self,[data_struct.DataStruct(self.N_h,self.N_vi) for t in range(2+self.T_MAX)])

        self.NOMBRE_DATA="DSp" #Data for model with supply support, for python. 
        
        self.mu=0.5
        self.iter_max=10
        self.tol=1e-1


        self.init_H_h()

        self[-1].b_h=zeros( (self.N_h,1) )
        self[-1].P_h_vi=array( [[0,1],[1,0]] )
        self[-1].S_vi=array( [[4.0/3,4.0/3]] )
        self[0].S_vi=array( [[2,2]] )
        
        #self.P_t_h_vi[-1]=ones( (self.N_h,self.N_vi) )/self.N_h

        #b_t_h[-2] y P_t_h_vi[-2] no son utilizados actualmente, quedan inicializados en valor por defecto empty.

        print "Data {0} inicializada".format(self.NOMBRE_DATA)
    

    def init_H_h(self):
        H_h_0=array( [[1],[3]] )
        tasa_crec_pop=0.5

        for t in range(-2,self.T_MAX):
            self[t].H_h=H_h_0*((1+tasa_crec_pop)**t)


    def fn_postura(self,P_h_vi,S_vi):
        alpha_h=array( [[1],[2]] )
        Z_h=( [[1],[2]] )
        b_h_vi=alpha_h*(Z_h*P_h_vi*S_vi).sum(axis=0)
        return b_h_vi
    
    def imprimir(self):
        print
        print "DATA: "+ self.NOMBRE_DATA
        print
        print "N_h=" + str(self.N_h)
        print "N_vi=" + str(self.N_vi)
        print "T_MAX=" + str(self.T_MAX)
        print
        print "S_t_vi[0:T_MAX]"
        aux_gen= (self[t].S_vi for t in range(-2,self.T_MAX))
        for x in aux_gen: print x
        print
        print "H_t_h[0:T_MAX]"
        aux_gen= (self[t].H_h for t in range(-2,self.T_MAX))
        for x in aux_gen:print x


        #rangos t=-1, t=-2 corresponden a inicializaciones anteriores a t=0,
        #se ubican en los últimos elementos del array.
        # |0|1|2|...|T_MAX|-2||-1|
