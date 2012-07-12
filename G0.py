#!/usr/local/bin/python
# coding: latin-1
from numpy import *
from modelo import *
class G0(Modelo):
    """Modelo"""

    def __init__(self):
        Modelo.__init__(self,"G0")


    def calc_b_h(self,dm,t):
        b_h=(-1/dm.mu)*(log(( dm[t].S_vi*exp(dm.mu*self.curr.b_h_vi)/
                (dm[t].H_h*exp(dm.mu*(self.old.b_h+self.curr.b_h_vi))).sum(axis=0)
                ).sum(axis=1)[:,newaxis]))

        return(b_h)

    def calc_P_h_vi(self,dm,t):
        P_h_vi=(dm[t].H_h*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))/
                    ((dm[t].H_h*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))).sum(axis=0)))
        return(P_h_vi)

    def calc_r_vi(self,dm,t):
        r_vi=(1/dm.mu)*log((dm[t].H_h*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))).sum(axis=0))
        return(r_vi)

    def calc_S_vi(self,dm,t):
        tasa=sum(dm[t].H_h)/sum(dm[t-1].H_h)
        print tasa
        S_vi=dm[t-1].S_vi*tasa
        print S_vi
        return(S_vi)
