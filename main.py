from qsim import Simulation, MatrixReader, ParameterSetReader, VerticalVectorReader, HorizontalVectorReader, ReportGenerator
from importlib import import_module

data_name = "D0"
model_name = "GqsR"

output_name = model_name+"-"+data_name
mod = import_module("qsim.models."+model_name).Model

households_data = VerticalVectorReader(
       'data/'+data_name+'/households_data.txt').get_data()
params = ParameterSetReader('data/test_data/parameters.txt').get_data()
locations_data = HorizontalVectorReader(
       'data/'+data_name+'/locations_data.txt').get_data()
probs_init = MatrixReader('data/'+data_name+'/data_P_h_vi_m1.txt').get_data()

model = mod(params, households_data, locations_data)
sim = Simulation(
       params, households_data, locations_data, probs_init, model)
sim.run()
repgen = ReportGenerator(sim,"output/"+output_name)
repgen.generate_variable_reports()
repgen.generate_step_reports()
repgen.store_results()
