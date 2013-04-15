from qsim import Simulation, MatrixReader, ParameterSetReader, VerticalVectorReader, HorizontalVectorReader, ReportGenerator, Plotter
from importlib import import_module

data_name = "test_data"
model_name = "test_model"
#simulation name, usually "modelname-dataname"
sim_name = model_name+"-"+data_name

#Importing model from package
mod = import_module("qsim.models."+model_name).Model

#reading households' data using VerticalVectorReader
households_data = VerticalVectorReader(
       'data/'+data_name+'/households_data.txt').get_data()

#reading locations' data using HorizontalVectorReader
locations_data = HorizontalVectorReader(
       'data/'+data_name+'/locations_data.txt').get_data()

#reading parameters using ParameterSetReader
params = ParameterSetReader('data/test_data/parameters.txt').get_data()

#reading initial value for probabilities using MatrixReader
probs_init = MatrixReader('data/'+data_name+'/data_P_h_vi_m1.txt').get_data()

#initializing model with data
model = mod(params, households_data, locations_data)

#initializing simulation with data and model
sim = Simulation(
       params, households_data, locations_data, probs_init, model, sim_name)

#running simulation
sim.run()

#generating reports with ReportGenerator in a new folder named
#after the simulation, inside folder "output/"
repgen = ReportGenerator(sim,"output/")
repgen.generate_variable_reports()
repgen.generate_step_reports()
repgen.store_results()

#plotting results with Plotter
Plotter(sim).plot()

