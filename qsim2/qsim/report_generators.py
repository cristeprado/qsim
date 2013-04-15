from os import makedirs
from os.path import exists, normpath, relpath, join
try:
   import cPickle as pickle
except:
   import pickle

class ReportGenerator(object):

    def __init__(self, sim, output_folder):
        self.sim=sim
        self.output_folder = normpath(relpath(output_folder))
        if not exists(self.output_folder):
            makedirs(self.output_folder)
        self.varname_list = self.sim.steps[0].__dict__.keys()

    def get_attr_if_exists(self,step, var):
        try:
            value = getattr(step,var)
        except AttributeError:
            value = "-"
        return value

    def generate_variable_reports(self):
        for var in self.varname_list:
            output_file_name = "log_{}.txt".format(var)
            output_file_path = normpath(join(self.output_folder, output_file_name))

            with open(output_file_path,'w') as ff:
                ff.write("Variable name: {}".format(var))
                for t in range(-2,self.sim.params.T_MAX):
                    ff.write("\n------t = {}------\n".format(t))
                    value = self.get_attr_if_exists(self.sim.steps[t],var)
                    ff.write("{}\n".format(value))

    def generate_step_reports(self):

        for t in range(self.sim.params.T_MAX):
            output_file_name = "iters_t{}.txt".format(t)
            output_file_path = normpath(join(self.output_folder, output_file_name))

            with open(output_file_path,'w') as ff:
                ff.write("t = {}".format(t))
                for cnt, iter_step in enumerate(self.sim.steps[t].iters):
                    ff.write("\n------Iteration {}------\n".format(-1+cnt))
                    for var in self.varname_list:
                        value = self.get_attr_if_exists(iter_step,var)
                        ff.write("{} = \n{}\n".format(var,value))

    def store_results(self):
        output_file_name = "data.pkl"
        output_file_path = normpath(join(self.output_folder, output_file_name))

        with open(output_file_path,'w') as ff:
            pickle.dump(self,ff)

