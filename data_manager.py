#!/usr/local/bin/python
# coding: latin-1
from numpy import *
import data_struct
import sys
import os
import os.path as op

class DataManager(list):
    #TODO: implementar __getitem__
    """Clase que contiene la data para los modelos"""

    ##########################################
    def __init__(self,currDataFolderPath=""):
        print "inicializando DataManager"

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
        self[0].S_vi=self.S_vi_0
        self[0].subsid_h=self.subsid_h_0
        self[0].subsid_vi=self.subsid_vi_0

        #inicializa la matriz H_h para cada t.
        #la matriz H_h es exógena, acá se inicializa por defecto
        #usando una tasa de crecimiento fija.
        self.init_H_h()

        print "Data {0} inicializada".format(self.NOMBRE_DATA)

    ##########################################
    def unload_data_from_files_to_dict(self,fileList):
        print "Leyendo archivos de parámetros"
        dd=dict()

        for fileName,type,parser_string in fileList:
            fileStream=open(fileName,"r")
            self.read_data_file(dd,fileStream,type,parser_string)
        return dd

    ##########################################
    def unload_data_from_dict_to_vars(self,dd):
        try:
            #parameters
            self.T_MAX=int(dd['T_MAX'][0])
            self.NOMBRE_DATA=dd['NOMBRE_DATA'][0]
            self.mu=float(dd['mu'][0])
            self.lambd=float(dd['lambd'][0])
            self.iter_max=int(dd['iter_max'][0])
            self.tol=float(dd['tol'][0])

            #datos h
            self.h=array(dd['h'])[:,newaxis]
            self.H_h_0=array(dd['H_h_0'])[:,newaxis]
            self.alpha_h=array(dd['alpha_h'])[:,newaxis]
            self.Z_h=array(dd['Z_h'])[:,newaxis]
            self.b_h_m1=array(dd['b_h_m1'])[:,newaxis]

            #datos vi
            self.vi=array(dd['vi'])[newaxis,:]
            self.S_vi_0=array(dd['S_vi_0'])[newaxis,:]

            #datos P_h_vi_m1
            self.P_h_vi_m1=array(dd['P_h_vi_m1'])

            #subsidios
            self.subsid_h_0=array(dd["subsid_h_0"])[:,newaxis]
            self.subsid_vi_0=array(dd["subsid_vi_0"])[newaxis,:]


            self.N_h=self.H_h_0.size
            self.N_vi=self.S_vi_0.size

        except KeyError as e:
            print "Exception: Not enough data available in files"
            print e
            sys.exit()


    ##########################################
    @staticmethod
    def read_data_file(dd,fileStream,type,parser_string='str'):
        #TO DO: ARREGLAR COMENTARIOS CON # y agregar strip()

        import csv

        #print "leyendo", fileName
        reader=csv.reader(fileStream)

        #elige parser
        if(parser_string=='int'):
            parser=int
        elif(parser_string=='float'):
            parser=float
        else:#parser_str=='str'
            parser=str
            
        #lee datos
        if(type=='vertical'):
            #acá los headers están en la primera fila.
            #los datos son todos doubles.
            for row,x in enumerate(reader):
                if x[0].startswith('#'): continue
                if row==0:
                    varNames =x
                    for varName in varNames:
                        dd[varName]=[]

                else:
                    for i in range(len(varNames)):
                        dd[varNames[i]].append(parser(x[i]))

        if(type=='horizontal'):
            #acá los headers están en la primera columna
            #los datos se extraen como string para parsear después. (inconsistencia?)
            for row,x in enumerate(reader):
                if x[0].startswith('#'): continue
                (varName,value)=(x[0],x[1:])
                dd[varName]=map(parser,value)
        
        if(type=='matrix'):
            #acá la primera fila tiene el nombre de la variable
            #acá hay headers en la segunda fila y en la primera columna.
            #el archivo corresponde a una sola variable, 

            result_list=[]
            varNameDone=False
            for row,x in enumerate(reader):
                if x[0].startswith('#'): continue
                if not varNameDone:
                    varName=x[0]
                    varNameDone=True
                elif row==1:
                    pass
                else:
                    (index_h,value)=(x[0],x[1:])
                    result_list.append(map(parser,value))

            dd[varName]=result_list


    ##########################################
    def init_H_h(self):
        tasa_crec_pop=0.5

        for t in range(-2,self.T_MAX):
            self[t].H_h=self.H_h_0*((1+tasa_crec_pop)**t)


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
                "S_vi","H_h_vi","I_h_vi","I2","converge"]

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
