#!/usr/local/bin/python
# coding: latin-1
from numpy import *
from model_template import *
class Model(ModelTemplate):
    """Modelo"""

    def __init__(self,modelName):
        ModelTemplate.__init__(self,modelName)

    def calc_b_h_vi(self,dm,t):
        b_h_vi_tokens=[]

        b_h_vi_tokens.append(dm.alpha_h*(dm.Z_h*dm[t-1].P_h_vi).sum(axis=0)[newaxis,:])
        b_h_vi_tokens.append(dm[t].subsid_h)
        b_h_vi_tokens.append(dm[t].subsid_vi)
        #b_h_vi_tokens.append(-(dm.Z_h-median(dm.Z_h))*(dm.vi+1))

        #for i in [0,3]:
            #tok=b_h_vi_tokens[i]
            #maxtok=absolute(b_h_vi_tokens[i]).max()
            #if maxtok<>0:
                #b_h_vi_tokens[i]=tok/maxtok

        #b_h_vi=sum(b_h_vi_tokens)
        b_h_vi=(b_h_vi_tokens[0]+
                b_h_vi_tokens[1]+
                b_h_vi_tokens[2])
                #5*b_h_vi_tokens[3])

        return b_h_vi

    def calc_phi_hvi(self,dm,t):
        phi_hvi_1=1/(1+((1-dm.nu)/dm.nu)*exp(dm.w*(-(dm[t-1].b_h+self.curr.b_h_vi))))
        phi_hvi_2=1/(1+((1-dm.nu)/dm.nu)*exp(dm.w*((dm[t-1].b_h+self.curr.b_h_vi-dm.Z_h))))
        print phi_hvi_2
        print 'bh',dm[t-1].b_h

        phi_hvi=phi_hvi_1*phi_hvi_2
        return(phi_hvi)

    def calc_b_h(self,dm,t):
        b_h=(-1/dm.mu)*(log(( dm[t-1].S_vi*self.curr.phi_hvi*exp(dm.mu*self.curr.b_h_vi)/(dm[t].H_h*self.curr.phi_hvi*exp(dm.mu*(dm[t-1].b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:]).sum(axis=1)[:,newaxis]))

        return(b_h)

    def calc_P_h_vi(self,dm,t):
        P_h_vi=(dm[t].H_h*self.curr.phi_hvi*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))/
                ((dm[t].H_h*self.curr.phi_hvi*exp(dm.mu*(self.curr.b_h+self.curr.b_h_vi))).sum(axis=0)[newaxis,:]))
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

