#!/usr/local/bin/python
# coding: latin-1
from numpy import *
import data_struct

class Modelo:
    """Modelo"""

    def __init__(self,NOMBRE_MODELO):
        self.NOMBRE_MODELO=NOMBRE_MODELO
        self.converge=False
        print "Modelo {0} inicializado".format(self.NOMBRE_MODELO)

    def ejecutar(self,dm,t):
        print "Iniciando ejecución de {modelo}{data}".format(
                modelo=self.NOMBRE_MODELO,
                data=dm.NOMBRE_DATA)

        #stream para log
        ff=open('log'+self.NOMBRE_MODELO+dm.NOMBRE_DATA+'.txt','w')

        #inicializa contador de iteraciones
        self.cnt=0

        #inicializo con los valores del período anterior
        self.curr=dm[t-1].copy() #TO DO: asegurarse de q es deep copy.
       #REVISAR COPIAS POR REFERENCIA Y POR VALOR. ESTOY MODIFICANDO DM.DS???? 
        self.delta=100*dm.tol

        while(self.cnt<dm.iter_max and self.delta>dm.tol):
            #actualizacion
            self.old=self.curr
            self.curr=data_struct.DataStruct(dm.N_h,dm.N_vi)

            #calculos modelo
            print "aa"
            print self.old.P_h_vi
            print "bb"
            print dm[t].S_vi
            self.curr.b_h_vi=dm.fn_postura(self.old.P_h_vi,dm[t].S_vi)
            self.curr.b_h=self.calc_b_h(dm,t)
            self.curr.P_h_vi=self.calc_P_h_vi(dm,t)
            self.curr.r_vi=self.calc_r_vi(dm,t)
            self.curr.S_vi=self.calc_S_vi(dm,t)

            #calculo error
            self.delta=self.calc_delta()

            #actualiza contador
            self.cnt+=1
            
            #imprime resultados de la iteracion
            self.imprimir_iter(dm,ff)

        if (self.delta<dm.tol):
            self.converge=1

        dm[t]=self.curr
        ff.close()
    

    def calc_delta(self):
        delta=sqrt(sum((self.curr.b_h-self.old.b_h)**2)+((self.curr.P_h_vi-self.old.P_h_vi)**2).sum())
        return(delta)

    def calc_b_h(self,dm,t):
        pass

    def calc_P_h_vi(self,dm,t):
        pass

    def calc_r_vi(self,dm,t):
        pass

    def calc_S_vi(self,dm,t):
        pass

    def imprimir_iter(self,dm,ff):
        
        #definición plantillas para output
        informe_iter= """
--------ITERACION {0}-------
b_h_vi=
{1}
b_h_curr=
{2}
P_h_vi_curr=
{3}
r_vi_curr=
{4}
S_vi_curr=
{5}"""

        informe_conv="""
Delta={0}<tol={1}?:{2}"""

        #caso primera iteración: imprime iteración 0 (condiciones inic.)
        if(self.cnt==1):
            texto=informe_iter.format(0,
                    self.old.b_h_vi,
                    self.old.b_h,
                    self.old.P_h_vi,
                    self.old.r_vi,
                    self.old.S_vi)
            ff.write(texto)
            print texto
        
        #imprime resultados para iteración actual
        texto1=informe_iter.format(self.cnt,
                    self.curr.b_h_vi,
                    self.curr.b_h,
                    self.curr.P_h_vi,
                    self.curr.r_vi,
                    self.curr.S_vi)

        texto2=informe_conv.format(self.delta,
                    dm.tol,
                    self.delta<dm.tol)

        texto=texto1+texto2

        ff.write(texto)
        print texto
