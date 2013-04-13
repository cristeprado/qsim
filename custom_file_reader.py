#!/usr/local/bin/python
# coding: latin-1
from numpy import *

class CustomFileReader(list):
    """Lector de archivos de texto en diversos formatos personalizados. 
	
	**3 tipos de estructura de archivos: **
	
	- verticales ('vertical'), corresponden a archivos de la forma
	
	label1	label2	label3
	x1	y1	z1
	x2	y2	z2

	-horizontales ('horizontal'): de la forma

	label1	x1	x2
	label2	y1	y2

	-matriciales ('matrix') de la forma

		label1	label2	label3
	labela	x1	x2	x3
	labelb	x4	x5	x6
	labelc	x7	x8	x9

	** 3 tipos de parser soportados **
	Los datos se leen como strings por defecto. Es posible precisar un parser de los siguientes:

	- 'float': lee y almacena los datos como tipo float
	- 'int': lee y almacena los datos como tipo int
	
	- 'str': tipo por defecto, lee y almacena los datos como string.

	Los labels siempre se leen como string.

"""


    ##########################################
    def __init__(self,fileStream,type,parser_string):
	self.fileStream=fileStream
	self.type=type
	self.parser_string=parser_string
	self.dd=dict()
	self.read_data_file()

#########################################
    def read_data_file(self):
        #TO DO: ARREGLAR COMENTARIOS CON # y agregar strip()

        import csv

        #print "leyendo", fileName
        reader=csv.reader(self.fileStream)

        #elige parser
        if(self.parser_string=='int'):
            parser=int
        elif(self.parser_string=='float'):
            parser=float
        else:#parser_str=='str'
            parser=str
            
        #lee datos
        if(self.type=='vertical'):
            #acá los headers están en la primera fila.
            #los datos son todos doubles.
            for row,x in enumerate(reader):
                if x[0].startswith('#'): continue
                if row==0:
                    varNames =x
                    for varName in varNames:
                        self.dd[varName]=[]

                else:
                    for i in range(len(varNames)):
                        self.dd[varNames[i]].append(parser(x[i]))

        if(self.type=='horizontal'):
            #acá los headers están en la primera columna
            #los datos se extraen como string para parsear después. (inconsistencia?)
            for row,x in enumerate(reader):
                if x[0].startswith('#'): continue
                (varName,value)=(x[0],x[1:])
                self.dd[varName]=map(parser,value)
        
        if(self.type=='matrix'):
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

            self.dd[varName]=result_list

    def get_dict(self):
	return self.dd


