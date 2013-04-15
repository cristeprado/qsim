#!/usr/local/bin/python
# coding: latin-1
from numpy import *
import data_struct
import os.path as op

class ModelTemplate:
    """Modelo"""

    def __init__(self,NOMBRE_MODELO):
        self.NOMBRE_MODELO=NOMBRE_MODELO

    def ejecutar(self,dm,t,currOutputFolderPath=""):
        log_filename="log_t{}.txt".format(t)

        ff=open(log_filename,'w')

        while(self.cnt<dm.iter_max and not self.curr.converge):
            self.imprimir_iter(dm,ff)

        ff.close()

    def imprimir_iter(self,dm,ff):

        #definición plantillas para output
        informe_iter= """
--------ITERACION {}-------
H_h=
{}
b_h_vi=
{}
b_h_curr=
{}
P_h_vi_curr=
{}
r_vi_curr=
{}
S_vi_curr=
{}
Delta={}<tol={}?:{}"""

        #caso primera iteración: imprime iteración 0 (condiciones inic.)
        if(self.cnt==1):
            texto=informe_iter.format(0,
                    self.old.H_h,
                    self.old.b_h_vi,
                    self.old.b_h,
                    self.old.P_h_vi,
                    self.old.r_vi,
                    self.old.S_vi,
                    "",
                    "",
                    "")
            ff.write(texto)

        #imprime resultados para iteración actual
        texto=informe_iter.format(self.cnt,
                    self.curr.H_h,
                    self.curr.b_h_vi,
                    self.curr.b_h,
                    self.curr.P_h_vi,
                    self.curr.r_vi,
                    self.curr.S_vi,
                    self.delta,
                    dm.tol,
                    self.delta<dm.tol)


        ff.write(texto)
