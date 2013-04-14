#!/usr/bin/python
# coding: latin-1

from numpy import newaxis, sqrt

class Model(object):

    def __init__(self, params):
        self.params = params;

    def calc(self, dm, t):
        self.curr=dm[t-1].copy()
        if t==0:
            self.curr.S_vi=dm[t].S_vi.copy()
        self.curr.H_h=dm[t].H_h.copy()
        self.curr.subsid_h=dm[t].subsid_h.copy()
        self.curr.subsid_vi=dm[t].subsid_vi.copy()
        #TODO: volver a esquema hardcopy_model_vars
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
            self.curr.phi_hvi=self.calc_phi_hvi(dm,t)
            self.curr.b_h=self.calc_b_h(dm,t)

            self.curr.P_h_vi=self.calc_P_h_vi(dm,t)
            self.curr.r_vi=self.calc_r_vi(dm,t)
            self.curr.S_vi=self.calc_S_vi(dm,t)
            self.curr.gamma_vi=self.calc_gamma_vi(dm,t)

            #calculo error
            self.delta=self.calc_delta()

            print self.delta
            #actualiza contador
            self.cnt+=1

            #determina si hay convergencia
            self.curr.converge=(self.delta<dm.tol)

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

    def calc_phi_hvi(self,dm,t):
        return(dm[t].phi_h_vi)

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
        avgZ_city = (self.params.Z_h*self.curr.H_h_vi).sum()/self.curr.H_h_vi.sum()
        avgZ_zone = (self.params.Z_h*self.curr.H_h_vi).sum(axis=0)[newaxis,:]/self.curr.H_h_vi.sum(axis=0)[newaxis,:]
        I2 = sqrt(((avgZ_city-avgZ_zone)**2).sum())
        return I2

    def calc_avgZ_vi(self,dm):
        avgZ_zone = (self.params.Z_h*self.curr.H_h_vi).sum(axis=0)[newaxis,:]/self.curr.H_h_vi.sum(axis=0)[newaxis,:]
        return avgZ_zone
