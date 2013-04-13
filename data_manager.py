#!/usr/local/bin/python
# coding: latin-1
from numpy import *
import data_struct
import sys
import os
import os.path as op
import custom_file_reader
import unittest

class DataManager(list):
    #TODO: implementar __getitem__
    #nuevos nombres: qsim, nueva estructura
    """Clase que contiene la data para los modelos"""

    ##########################################
    def __init__(self,dataFolderPath,dataArg):
        print "inicializando DataManager"

        currDataFolderPath= op.normpath(op.join(dataFolderPath,dataArg))

        self.NOMBRE_DATA=dataArg

        #lista de archivos con la data, con sus propiedades
        fileList=[['data_parameters.txt','horizontal','str'],
            ['data_h.txt','vertical','float'],
            ['data_vi.txt','horizontal','float'],
            ['data_P_h_vi_m1.txt','matrix','float'],
            ['subsid_h.txt','vertical','float'],
            ['subsid_vi.txt','horizontal','float']]

        if currDataFolderPath!="":
            for lf in fileList:
                lf[0]=op.normpath(op.join(currDataFolderPath,lf[0]))
        
        #descarga data en un diccionario self.dd
        self.dd=self.unload_data_from_files_to_dict(fileList)

        #descarga data desde el diccionario a las variables
        self.unload_data_from_dict_to_vars(self.dd)
        print self.dd

        #inicializa la lista de la clase super
        list.__init__(self,[data_struct.DataStruct(self.N_h,self.N_vi) for t in range(2+self.T_MAX)])

        #asigna ciertas variables en la lista
        self[-1].b_h=self.b_h_m1
        self[-1].P_h_vi=self.P_h_vi_m1
        self[0].subsid_h=self.subsid_h_0
        self[0].subsid_vi=self.subsid_vi_0

        #inicializa la matriz H_h para cada t.
        #la matriz H_h es exógena, acá se inicializa por defecto
        #usando una tasa de crecimiento fija.
        self.init_H_h()
        
        #inicializa la matriz S_vi, cumpliendo las restricciones de regulación por zona y el total agregado de oferta (solución factible).
        self.init_S_vi()

        #inicializa los parámetros gamma al valor del archivo
        self[0].gamma_vi=self.gamma_vi_0

        #inicializa S_vi al valor actual en los períodos -1 y -2
        self[-1].S_vi=self[0].S_vi.copy()
        self[-2].S_vi=self[0].S_vi.copy()

        print "Data {0} inicializada".format(self.NOMBRE_DATA)

    ##########################################
    def unload_data_from_files_to_dict(self,fileList):
        print "Leyendo archivos de parámetros"
        dd=dict()
        for fileName,type,parser_string in fileList:
			currFile=custom_file_reader.CustomFileReader(open(fileName,"r"),type,parser_string)
			dd.update(currFile.get_dict())

        return dd
		
		   ##########################################
    # def unload_data_from_dict_to_vars(self,dd):
        # try:
            # parameters
            # self.T_MAX=int(dd.get('T_MAX',[-1])[0])
            # self.mu=float(dd.get('mu',[-1])[0])
            # self.lambd=float(dd.get('lambd',[-1])[0])
            # self.iter_max=int(dd.get('iter_max',[-1])[0])
            # self.tol=float(dd.get('tol',[-1])[0])
            # self.nu=float(dd.get('nu',[-1])[0])
            # self.w=float(dd.get('w',[-1])[0])


            datos h
            # self.h=array(dd.get('h',[-1]))[:,newaxis]
            # self.H_h_0=array(dd.get('H_h_0',[-1]))[:,newaxis]
            # self.alpha_h=array(dd.get('alpha_h',[-1]))[:,newaxis]
            # self.Z_h=array(dd.get('Z_h',[-1]))[:,newaxis]
            # self.b_h_m1=array(dd.get('b_h_m1',[-1]))[:,newaxis]

            datos vi
            # self.vi=array(dd.get('vi',[-1]))[newaxis,:]
            # self.S_vi_0=array(dd.get('S_vi_0',[-1]))[newaxis,:]
            # self.gamma_vi_0=array(dd.get('gamma_vi_0',[-1]))[newaxis,:]
            # self.R_vi=array(dd.get('R_vi',[-1]))[newaxis,:]

            datos P_h_vi_m1
            # self.P_h_vi_m1=array(dd.get('P_h_vi_m1',[-1]))

            subsidios
            # self.subsid_h_0=array(dd.get("subsid_h_0"))[:,newaxis]
            # self.subsid_vi_0=array(dd.get("subsid_vi_0"))[newaxis,:]


            # self.N_h=self.H_h_0.size
            # self.N_vi=self.S_vi_0.size

        # except KeyError as e:
            # print "Warning: Missing data available in files"
            # print e
            # sys.exc_clear()
            # ©pass
            # sys.exit()


    ##########################################

    ##########################################
    def unload_data_from_dict_to_vars(self,dd):
        #try:
            #parameters
			nameList=['T_MAX','mu','lambd','iter_max','tol','nu','w']
			parserList=[int,float,float,int,float,float,float]

			for each name in nameList
				self.__dict__[name]=int(dd.get(name,[-1])[0])
           
            #datos h
			for each name in ['h','H_h_0','alpha_h','Z_h','b_h_m1','subsid_h_0']
				self.__dict__[name]=array(dd.get(name,[-1]))[:,newaxis]

            #datos vi
			for each name in ['vi','S_vi_0','gamma_vi_0','R_vi','subsid_vi_0']
				self.__dict__[name]=array(dd.get(name,[-1]))[newaxis,:]
          
            #datos P_h_vi_m1
			for each name in ['P_h_vi_m1']
				self.__dict__[name]=array(dd.get(name,[-1]))


            self.N_h=self.H_h_0.size
            self.N_vi=self.S_vi_0.size

        #except KeyError as e:
            #print "Warning: Missing data available in files"
            #print e
            #sys.exc_clear()
            #©pass
            #sys.exit()


    ###########################################
    def init_H_h(self):
        tasa_crec_pop=0.1
        #TODO: TASA DE CRECIMIENTO DE POBLACION; SACAR DE ACA Y PONER EN ARCHIVO DE PARAMETROS

        for t in range(-2,self.T_MAX):
            self[t].H_h=self.H_h_0*((1+tasa_crec_pop)**(t))

        #for t in range(-2,1):
        #    self[t].H_h=self.H_h_0*((1+tasa_crec_pop)**(t))

    #    for t in range(1,self.T_MAX):
     #       self[t].H_h=self.H_h_0*((1+tasa_crec_pop)**((t+1)/2.0))


    #########################################
    def init_S_vi(self):
        self[0].S_vi=self.S_vi_0

        print "Solución inicial original"
        print self[0].S_vi

        remainder=0
        for i in range(0,self.N_vi):
            if self[0].S_vi[0,i]>self.R_vi[0,i]:
                remainder+=self[0].S_vi[0,i]-self.R_vi[0,i]
                self[0].S_vi[0,i]=self.R_vi[0,i]

        for i in range(0,self.N_vi):
            if self[0].S_vi[0,i]<self.R_vi[0,i]:
                slack=self.R_vi[0,i]-self[0].S_vi[0,i]
                if remainder>slack:
                    remainder-=slack
                    self[0].S_vi[0,i]=self.R_vi[0,i]
                else:
                    self[0].S_vi[0,i]+=remainder
                    remainder=0
        print "Solución inicial factible:"
        print self[0].S_vi

        if remainder>0:
            #launch exception
            print "Advertencia: El problema de oferta es infactible debido al conjunto de restricciones de regulación utilizado. Se ha descartado el excedente de oferta para permitir la ejecución."

    ##########################################
    def print_logfiles(self,currOutputFolderPath=""):

        #templates para los nombres de los archivos log
        log_general="log.txt"
        log_per_var_template="log_{var}.txt"

        if currOutputFolderPath!="":

            log_general=op.normpath(op.join(currOutputFolderPath,log_general))
            log_per_var_template=op.normpath(op.join(currOutputFolderPath,log_per_var_template))

        header_template="""DATA: "+ self.NOMBRE_DATA
@@@@@@@@@@@@@@@@@@@@@@@@@@
"N_h=" {N_h}
"N_vi=" {N_vi}
"T_MAX=" {T_MAX}
@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""

        #lista de variables para imprimir
        varname_list=["H_h","b_h","P_h_vi","b_h_vi","B_h_vi","r_vi",
                "S_vi","H_h_vi","I_h_vi","I2","converge","gamma_vi"]

        #abre stream para log general
        logfile_name=log_general.format(
                mod=mod,
                data=self.NOMBRE_DATA)
        ff_gen=open(logfile_name,'w')

        #imprime header en log general
        ff_gen.write(header_template.format(N_h=self.N_h,
                N_vi=self.N_vi,
                T_MAX=self.T_MAX))

        for x in varname_list:
            #imprime cada variable en log general
            ff_gen.write(self.string_output_var(x))

            #crea log de cada variable
            logfile_name=log_per_var_template.format(
                    mod=mod,
                    data=self.NOMBRE_DATA,
                    var=x)

            #imprime log de cada variable
            ff_var=open(logfile_name,'w')
            ff_var.write(self.string_output_var(x))
            ff_var.close()

        ff_gen.close()


    ##########################################
    def string_output_var(self,varName):
        result=[varName+"\n"]
        for t in range(-2,self.T_MAX):
            result.append("t={}\n".format(t))
            result.append("{}\n".format(self[t].var_dict[varName]))
        result.append("\n")

        return("".join(result))

    def time_serie_var(self,varName):
        result=[]
        for t in range(-2,self.T_MAX):
            result.append(self[t].var_dict[varName])
   
        return result

        #rangos t=-1, t=-2 corresponden a inicializaciones anteriores a t=0,
        #se ubican en los últimos elementos del array.
        # |0|1|2|...|T_MAX|-2||-1|
