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
    #Folder names
    dataFolderPath=op.normpath(op.relpath("Data"))
    outputFolderPath=op.normpath(op.relpath("Output"))
    datfilesFolderPath=op.normpath(op.relpath("datfiles"))
    modelsLibAbsPath=op.abspath("Models")


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


    dm.print_logfiles(currOutputFolderPath)
    with open(op.join(datfilesFolderPath,dm.NOMBRE_MODELO+dm.NOMBRE_DATA+".dat"),'w') as fdump:
        pickle.dump(dm,fdump)

    with open(op.join(datfilesFolderPath,"dm.dat"),'w') as fdump:
        pickle.dump(dm,fdump)


if __name__=="__main__":
    main()
