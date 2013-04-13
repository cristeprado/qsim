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
    """Execute to run model and data specified in config file.
        syntax: main [model] [data]
        Model and data can be introduced as arguments.
    """

    #Folder names
    dataFolderPath=op.normpath(op.relpath("Data"))
    outputFolderPath=op.normpath(op.relpath("Output"))
    datfilesFolderPath=op.normpath(op.relpath("datfiles"))
    modelsLibAbsPath=op.abspath("Models")

    #inserts the folder "models" in system path in order to be able to retrieve it later
    sys.path.insert(0,modelsLibAbsPath)

    print "Comenzando programa"

    #read config file
    with open('qsim-config.txt','r') as ff:
        modelArg=ff.readline().split(",")[1].strip()
        dataArg=ff.readline().split(",")[1].strip()

    #use args if provided
    if len(sys.argv)>=3:
        modelArg=sys.argv[1]
        dataArg=sys.argv[2]

    print "Model: ",modelArg
    print "Dataset: ",dataArg

    #import model to be used
    currMod=__import__(modelArg)
    mod=currMod.Model(modelArg)
    dm=data_manager.DataManager(dataFolderPath,dataArg)
    dm.NOMBRE_MODELO=modelArg

    #path de output folder
    currOutputFolderPath=op.normpath(op.join(outputFolderPath,dm.NOMBRE_MODELO+dm.NOMBRE_DATA))

    #Creates output folder if needed
    if not op.exists(currOutputFolderPath):
        os.makedirs(currOutputFolderPath)

    #Executing model for each instant t.
    for t in range(dm.T_MAX):
        mod.ejecutar(dm,t,currOutputFolderPath)

    print "storing results (pickle)"

    dm.print_logfiles(currOutputFolderPath)
    with open(op.join(datfilesFolderPath,dm.NOMBRE_MODELO+dm.NOMBRE_DATA+".dat"),'w') as fdump:
        pickle.dump(dm,fdump)

    with open(op.join(datfilesFolderPath,"dm.dat"),'w') as fdump:
        pickle.dump(dm,fdump)


if __name__=="__main__":
    main()
