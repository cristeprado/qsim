#!/usr/bin/python
# coding: latin-1

from numpy import newaxis, sqrt

class Model(object):

    def __init__(self, params, households_data, locations_data):
        self.params = params;
        self.households_data = households_data
        self.locations_data = locations_data

    def calc(self, dm, t):
        self.curr=dm[t-1].copy()
        self.curr.H_h=dm[t].H_h.copy()
        self.curr.converge=False

        list_iters=[dm[t-1]]
        cnt=0
        while(cnt<self.params.iter_max and not self.curr.converge):
            #actualizacion
            self.old=self.curr
            self.curr=self.curr.copy()

            #calculos modelo
            self.curr.b_h_vi=self.calc_b_h_vi(dm,t)
            self.curr.b_h=self.calc_b_h(dm,t)

            self.curr.P_h_vi=self.calc_P_h_vi(dm,t)
            self.curr.r_vi=self.calc_r_vi(dm,t)
            self.curr.S_vi=self.calc_S_vi(dm,t)
            self.curr.gamma_vi=self.calc_gamma_vi(dm,t)

            #calculo error
            delta=self.calc_delta()

            print delta
            #actualiza contador
            cnt+=1

            #determina si hay convergencia
            self.curr.converge=(delta<self.params.tol)

            print "t=",t,", iteración",cnt,", converge?:",self.curr.converge

            self.curr.H_h_vi=self.calc_H_h_vi()
            self.curr.I_h_vi=self.calc_I_h_vi()
            self.curr.B_h_vi=self.calc_B_h_vi()
            self.curr.I2=self.calc_I2(dm)
            self.curr.avgZ_vi=self.calc_avgZ_vi(dm)

            list_iters.append(self.curr)

        self.curr.iters_count=cnt
        self.curr.iters=list_iters
        dm[t]=self.curr.copy()

    def calc_delta(self):
        return sqrt(sum((self.curr.b_h-self.old.b_h)**2)+((self.curr.P_h_vi-self.old.P_h_vi)**2).sum())

    def calc_b_h(self,dm,t):
        raise Exception("Not implemented")

    def calc_P_h_vi(self,dm,t):
        raise Exception("Not implemented")

    def calc_r_vi(self,dm,t):
        raise Exception("Not implemented")

    def calc_S_vi(self,dm,t):
        raise Exception("Not implemented")

    def calc_b_h_vi(self,dm):
        raise Exception("Not implemented")

    def calc_gamma_vi(self,dm,t):
        return(dm[t].gamma_vi)

    def calc_H_h_vi(self):
        H_h_vi = self.curr.H_h_vi=self.curr.S_vi*self.curr.P_h_vi
        return H_h_vi

    def calc_I_h_vi(self):
        I_h_vi = self.curr.H_h_vi/self.curr.S_vi.sum()
        return I_h_vi

    def calc_B_h_vi(self):
        B_h_vi = self.curr.b_h+self.curr.b_h_vi
        return B_h_vi

    def calc_I2(self,dm):
        avgZ_city = (self.households_data.Z_h*self.curr.H_h_vi).sum()/self.curr.H_h_vi.sum()
        avgZ_zone = (self.households_data.Z_h*self.curr.H_h_vi).sum(axis=0)[newaxis,:]/self.curr.H_h_vi.sum(axis=0)[newaxis,:]
        I2 = sqrt(((avgZ_city-avgZ_zone)**2).sum())
        return I2

    def calc_avgZ_vi(self,dm):
        avgZ_zone = (self.households_data.Z_h*self.curr.H_h_vi).sum(axis=0)[newaxis,:]/self.curr.H_h_vi.sum(axis=0)[newaxis,:]
        return avgZ_zone
