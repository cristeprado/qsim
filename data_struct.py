#!/usr/local/bin/python
# coding: latin-1
from numpy import *

class DataStruct:
    """Clase que maneja las variables del modelo"""

    def __init__(self,N_h,N_vi):
        self.H_h=empty( (N_h,1) )
        self.b_h=empty( (N_h,1) )
        self.P_h_vi=empty( (N_h, N_vi) )
        self.b_h_vi=empty( (N_h, N_vi) )
        self.r_vi=empty( (1, N_vi) )
        self.S_vi=empty( (1, N_vi) )

    def copy(self):
        newcopy=DataStruct(1,1)
        newcopy.H_h=self.H_h.copy()
        newcopy.b_h=self.b_h.copy()
        newcopy.P_h_vi=self.P_h_vi.copy()
        newcopy.b_h_vi=self.b_h_vi.copy()
        newcopy.r_vi=self.r_vi.copy()
        newcopy.S_vi=self.S_vi.copy()
        return newcopy
