#!/usr/local/bin/python
# coding: latin-1
from numpy import *
from model_template import *
class Model(ModelTemplate):
    """Modelo"""

    def __init__(self,modelName):
        ModelTemplate.__init__(self,modelName)

    def calc_b_h_vi(self,dm,t):
        return dm.alpha_h*(dm.Z_h*dm[t-1].P_h_vi).sum(axis=0)[newaxis,:]

    def calc_b_h(self,dm,t):
        print dm[t-1].S_vi
        b_h=(-1/dm.mu)*(log(( dm[t-1].S_vi*exp(dm.mu*self.curr.b_h_vi)/(dm[t].H_h*exp(dm.mu*(dm[t-1].b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:]).sum(axis=1)[:,newaxis]))

        return(b_h)

    def calc_P_h_vi(self,dm,t):
        print self.curr.b_h
        print self.curr.b_h_vi
        P_h_vi=(dm[t].H_h*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))/
                ((dm[t].H_h*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:]))
        return(P_h_vi)

    def calc_r_vi(self,dm,t):
        r_vi=(1/dm.mu)*log((dm[t].H_h*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:])
        return(r_vi)

    def calc_S_vi(self,dm,t):
        S_vi=sum(dm[t].H_h)*exp(dm.lambd*(self.curr.r_vi-dm[t-1].gamma_vi))/(exp(dm.lambd*(self.curr.r_vi-dm[t-1].gamma_vi))).sum(axis=1)[:,newaxis]
        return(S_vi)

    def calc_gamma_vi(self,dm,t):
        gamma_vi=(self.curr.S_vi>dm.R_vi)*(1/dm.lambd)*log(((sum(dm[t].H_h))/dm.R_vi)*(exp(dm.lambd*(self.curr.r_vi))/(exp(dm.lambd*(self.curr.r_vi-dm[t-1].gamma_vi))).sum(axis=1)[:,newaxis]))
        return(gamma_vi)
