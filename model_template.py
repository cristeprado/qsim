#!/usr/local/bin/python
# coding: latin-1
from numpy import *
import data_struct
import os.path as op

class ModelTemplate:
    """Modelo"""

    def __init__(self,NOMBRE_MODELO):
        self.NOMBRE_MODELO=NOMBRE_MODELO
        print "Modelo {0} inicializado".format(self.NOMBRE_MODELO)

    def ejecutar(self,dm,t,currOutputFolderPath=""):
        print "Iniciando ejecución de {mod}{data} con t={t}".format(
                mod=self.NOMBRE_MODELO,
                data=dm.NOMBRE_DATA,
                t=t)

        #nombre archivo log (ej: logG0DSp_t0.txt)
        log_filename="log_t{t}.txt".format(
                mod=self.NOMBRE_MODELO,
                data=dm.NOMBRE_DATA,
                t=t)

        if currOutputFolderPath!="":
            log_filename=op.normpath(op.join(currOutputFolderPath,log_filename))


        #stream para log
        print "creando archivo log",log_filename
        ff=open(log_filename,'w')

        #inicializa contador de iteraciones
        self.cnt=0

        #inicializo con los valores del período anterior
        print "inicializando con los valores del período anterior"
        self.curr=dm[t-1].copy()
        if t==0:
            self.curr.S_vi=dm[t].S_vi.copy()
        self.curr.H_h=dm[t].H_h.copy()
        self.curr.subsid_h=dm[t].subsid_h.copy()
        self.curr.subsid_vi=dm[t].subsid_vi.copy()
        #TO DO: volver a esquema hardcopy_model_vars
        self.curr.converge=False

        self.curr.H_h_vi=self.calc_H_h_vi()
        self.curr.I_h_vi=self.calc_I_h_vi()
        self.curr.B_h_vi=self.calc_B_h_vi()

        self.delta=100*dm.tol
        #dm inicializa como converge=False

        list_iters=[self.curr]
        while(self.cnt<dm.iter_max and not self.curr.converge):
            #actualizacion
            self.old=self.curr
            self.curr=self.old.copy()

            #calculos modelo
            self.curr.b_h_vi=self.calc_b_h_vi(dm,t)
            self.curr.b_h=self.calc_b_h(dm,t)
            self.curr.P_h_vi=self.calc_P_h_vi(dm,t)
            self.curr.r_vi=self.calc_r_vi(dm,t)
            self.curr.S_vi=self.calc_S_vi(dm,t)

            #calculo error
            self.delta=self.calc_delta()

            #actualiza contador
            self.cnt+=1

            #determina si hay convergencia
            self.curr.converge=(self.delta<dm.tol)

            #imprime resultados de la iteracion
            self.imprimir_iter(dm,ff)

            print "t=",t,", iteración",self.cnt,", converge?:",self.curr.converge

            self.curr.H_h_vi=self.calc_H_h_vi()
            self.curr.I_h_vi=self.calc_I_h_vi()
            self.curr.B_h_vi=self.calc_B_h_vi()
            self.curr.I2=self.calc_I2(dm)
            self.curr.avgZ_vi=self.calc_avgZ_vi(dm)

            list_iters.append(self.curr)

        self.curr.iters_count=self.cnt
        self.curr.iters=list_iters
        dm[t]=self.curr
        ff.close()

    def calc_delta(self):
        delta=sqrt(sum((self.curr.b_h-self.old.b_h)**2)+((self.curr.P_h_vi-self.old.P_h_vi)**2).sum())
        return(delta)

    def calc_b_h(self,dm,t):        pass
    def calc_P_h_vi(self,dm,t):        pass
    def calc_r_vi(self,dm,t):        pass
    def calc_S_vi(self,dm,t):        pass
    def calc_b_h_vi(self,dm):        pass

    def calc_H_h_vi(self):
        H_h_vi=self.curr.H_h_vi=self.curr.S_vi*self.curr.P_h_vi
        return H_h_vi

    def calc_I_h_vi(self):
        I_h_vi=self.curr.H_h_vi/self.curr.S_vi.sum()
        return I_h_vi

    def calc_B_h_vi(self):
        B_h_vi=self.curr.b_h+self.curr.b_h_vi
        return B_h_vi
 
    def calc_I2(self,dm):
        avgZ_city=(dm.Z_h*self.curr.H_h_vi).sum()/self.curr.H_h_vi.sum()
        avgZ_zone=(dm.Z_h*self.curr.H_h_vi).sum(axis=0)[newaxis,:]/self.curr.H_h_vi.sum(axis=0)[newaxis,:]
        I2=sqrt(((avgZ_city-avgZ_zone)**2).sum())
        return I2

    def calc_avgZ_vi(self,dm):
        avgZ_zone=(dm.Z_h*self.curr.H_h_vi).sum(axis=0)[newaxis,:]/self.curr.H_h_vi.sum(axis=0)[newaxis,:]
        return avgZ_zone

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
