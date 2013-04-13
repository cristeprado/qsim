#!/usr/local/bin/python
# coding: latin-1
from numpy import *

class DataStruct:
    """Clase que maneja las variables del modelo"""

    def __init__(self,N_h,N_vi):
        self.var_dict={}
        self.var_dict["H_h"] = empty( (N_h,1) )
        self.var_dict["b_h"] = empty( (N_h,1) )
        self.var_dict["P_h_vi"] = empty( (N_h, N_vi) )
        self.var_dict["b_h_vi"] = empty( (N_h, N_vi) )
        self.var_dict["B_h_vi"]=  empty( (N_h, N_vi) )
        self.var_dict["r_vi"] = empty( (1, N_vi) )
        self.var_dict["gamma_vi"]=zeros( (1, N_vi) )
        self.var_dict["phi_h_vi"]=ones( (N_h,N_vi) )
        self.var_dict["S_vi"] = empty( (1, N_vi) )
        self.var_dict["H_h_vi"] = empty( (N_h,N_vi) )
        self.var_dict["I_h_vi"] = empty( (N_h,N_vi) )
        self.var_dict["I2"]=0
        self.var_dict["subsid_h"]= empty( (N_h,1) )
        self.var_dict["subsid_vi"]= empty( (1,N_vi) )
        self.var_dict["converge"] = False
        self.var_dict["iters"] = []
        self.var_dict["iters_count"] = 0

        self.__dict__.update(self.var_dict)
        self.var_dict=self.__dict__

    def copy(self):
        newcopy=DataStruct(1,1)
        newcopy.H_h=self.H_h.copy()
        newcopy.b_h=self.b_h.copy()
        newcopy.P_h_vi=self.P_h_vi.copy()
        newcopy.b_h_vi=self.b_h_vi.copy()
        newcopy.r_vi=self.r_vi.copy()
        newcopy.gamma_vi=self.gamma_vi.copy()
        newcopy.S_vi=self.S_vi.copy()
        newcopy.H_h_vi=self.H_h_vi.copy()
        newcopy.I_h_vi=self.I_h_vi.copy()
        newcopy.converge=self.converge
        return newcopy


#TO DO: Usar el diccionario como la estructura principal para almacenar las variables, y crear properties para recuperar los valores de las variables desde el diccionario usando el nombre. (i.e. ds.H_h debe devolver ds.dd["H_h"] usando properties.
