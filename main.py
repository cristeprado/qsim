#!/usr/local/bin/python
# coding: latin-1
from numpy import *
import G0
import numpy
import data_manager
import matplotlib

def main():
    print "Comenzando programa"
    print numpy.__version__
    print matplotlib.__version__
    modG0=G0.G0()
    dm=data_manager.DataManager()
    
    #dm.imprimir()

    #modG0.ejecutar(dm,0)


if __name__=="__main__":
    main()
