#!/usr/local/bin/python
# coding: latin-1

from numpy import newaxis, log, exp

from model import Model as BaseModel

class Model(BaseModel):

    def __init__(self, params, households_data, locations_data):
        BaseModel.__init__(self, params, households_data, locations_data)

    def calc_b_h_vi(self,dm,t):
        return self.households_data.alpha_h*(self.households_data.Z_h*dm[t-1].P_h_vi).sum(axis=0)[newaxis,:]

    def calc_b_h(self,dm,t):
        b_h=(-1/self.params.mu)*(log(( dm[t-1].S_vi*exp(self.params.mu*self.curr.b_h_vi)/(dm[t].H_h*exp(self.params.mu*(dm[t-1].b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:]).sum(axis=1)[:,newaxis]))

        return(b_h)

    def calc_P_h_vi(self,dm,t):
        P_h_vi=(dm[t].H_h*exp(self.params.mu*(self.curr.b_h+self.curr.b_h_vi))/
                ((dm[t].H_h*exp(self.params.mu*(self.curr.b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:]))
        return(P_h_vi)

    def calc_r_vi(self,dm,t):
        r_vi=(1/self.params.mu)*log((dm[t].H_h*exp(self.params.mu*(self.curr.b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:])
        return(r_vi)

    def calc_S_vi(self,dm,t):
        S_vi=sum(dm[t].H_h)*exp(self.params.lambd*(self.curr.r_vi-dm[t-1].gamma_vi))/(exp(self.params.lambd*(self.curr.r_vi-dm[t-1].gamma_vi))).sum(axis=1)[:,newaxis]
        return(S_vi)

    def calc_gamma_vi(self,dm,t):
        gamma_vi=(self.curr.S_vi>self.locations_data.R_vi)*(1/self.params.lambd)*log(((sum(dm[t].H_h))/self.locations_data.R_vi)*(exp(self.params.lambd*(self.curr.r_vi))/(exp(self.params.lambd*(self.curr.r_vi-dm[t-1].gamma_vi))).sum(axis=1)[:,newaxis]))
        return(gamma_vi)
