from numpy import empty, zeros, ones
from copy import deepcopy

class SimulationStep(object):

    def __init__(self,N_h,N_vi):
        pass

    def copy(self):
        return deepcopy(self)


class Simulation(object):

    def __init__(self, params, households_data, locations_data, probs_init, model):
            self.params = params
            self.households_data = households_data
            self.probs_init = probs_init
            self.locations_data = locations_data
            self.model = model
            self.data_name = ""
            self.model_name = ""

            self.data_validate()
            self.init_steps()

    def set_data_name(self, name):
        self.data_name = name

    def set_model_name(self, name):
        self.model_name = name

    def make_step(self):
        return SimulationStep(
                len(self.households_data.H_h_0), len(self.locations_data.S_vi_0))

    def data_validate(self):
        for i in range(len(self.locations_data.S_vi_0)):
            if (self.locations_data.S_vi_0 > self.locations_data.R_vi).any():
                raise ValueError

    def init_steps(self):
        self.steps = [self.make_step() for t in range(0, self.params.T_MAX + 2)]
        self.steps[-1].b_h = self.households_data.b_h_m1
        self.steps[-1].P_h_vi = self.probs_init.P_h_vi_m1
        self.steps[0].gamma_vi = self.locations_data.gamma_vi_0
        self.steps[-1].gamma_vi = self.locations_data.gamma_vi_0.copy()
        self.steps[0].S_vi = self.locations_data.S_vi_0
        self.steps[-1].S_vi = self.locations_data.S_vi_0.copy()
        self.steps[-2].S_vi = self.locations_data.S_vi_0.copy()

        for t in range(-2,self.params.T_MAX):
            factor = ((1 + self.params.pop_growth_rate)**t)
            self.steps[t].H_h = self.households_data.H_h_0 * factor

    def run(self):
        for t in range(self.params.T_MAX):
            self.model.calc(self.steps,t)

