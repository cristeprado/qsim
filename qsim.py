#!/usr/local/bin/python
# coding: latin-1
import data_manager
import sys
import matplotlib
import os
import os.path as op
try:
   import cPickle as pickle
except:
   import pickle

def main():
    dataFolderPath=op.normpath(op.relpath("Data"))
    outputFolderPath=op.normpath(op.relpath("Output"))
    modelsLibAbsPath=op.abspath("Models")
    sys.path.insert(0,modelsLibAbsPath)

    print "Comenzando programa"
    ff=open('qsim-config.txt','r')

    modelArg=ff.readline().split(",")[1].strip()
    dataArg=ff.readline().split(",")[1].strip()

    if len(sys.argv)>=2:
        modelArg=sys.argv[1]
    if len(sys.argv)>=3:
        dataArg=sys.argv[2]

    print modelArg
    print dataArg

    currMod=__import__(modelArg)

    currDataFolderPath= op.normpath(op.join(dataFolderPath,dataArg))

    mod=currMod.Model(modelArg)
    dm=data_manager.DataManager(currDataFolderPath)
    dm.NOMBRE_DATA=dataArg

    currOutputFolderPath=op.normpath(op.join(outputFolderPath,mod.NOMBRE_MODELO+dm.NOMBRE_DATA))

    if not op.exists(currOutputFolderPath):
        os.makedirs(currOutputFolderPath)

    for t in range(dm.T_MAX):
        mod.ejecutar(dm,t,currOutputFolderPath)

    print "almacenando resultados (pickle)"

    dm.print_logfiles(currOutputFolderPath)
    fdump=open(mod.NOMBRE_MODELO+dm.NOMBRE_DATA+".dat",'w')
    pickle.dump(dm,fdump)
    fdump.close()
    
    fdump=open("dm.dat",'w')
    pickle.dump(dm,fdump)
    fdump.close()


if __name__=="__main__":
    main()
