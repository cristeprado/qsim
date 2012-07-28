#!/usr/local/bin/python
# coding: latin-1
from numpy import *
from modelo import *
class Model(ModelTemplate):
    """Modelo"""

    def __init__(self,modelName):
        ModelTemplate.__init__(self,modelName)

    def calc_b_h_vi(self,dm,t):
        b_h_vi=dm.alpha_h*(dm.Z_h*self.curr.P_h_vi).sum(axis=0)[newaxis,:]
        return b_h_vi

    def calc_b_h(self,dm,t):
        b_h=(-1/dm.mu)*(log(( self.old.S_vi*exp(dm.mu*self.curr.b_h_vi)/
            (dm[t].H_h*exp(dm.mu*(self.old.b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:]
                ).sum(axis=1)[:,newaxis]))

        return(b_h)

    def calc_P_h_vi(self,dm,t):
        P_h_vi=(dm[t].H_h*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))/
                ((dm[t].H_h*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:]))
        return(P_h_vi)

    def calc_r_vi(self,dm,t):
        r_vi=(1/dm.mu)*log((dm[t].H_h*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:])
        return(r_vi)

    def calc_S_vi(self,dm,t):
        if t==0:
            S_vi=dm[0].S_vi
        else:
            tasa=sum(dm[t].H_h)/sum(dm[t-1].H_h)
            S_vi=dm[t-1].S_vi*tasa
        return(S_vi)

