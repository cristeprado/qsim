from numpy import empty, zeros, ones
from copy import deepcopy

class SimulationStep(object):

    def __init__(self,N_h,N_vi):
        self.H_h = empty( (N_h,1) )
        self.b_h = empty( (N_h,1) )
        self.P_h_vi = empty( (N_h, N_vi) )
        self.b_h_vi = empty( (N_h, N_vi) )
        self.B_h_vi=  empty( (N_h, N_vi) )
        self.r_vi = empty( (1, N_vi) )
        self.gamma_vi = zeros( (1, N_vi) )
        self.phi_h_vi = ones( (N_h,N_vi) )
        self.S_vi = empty( (1, N_vi) )
        self.H_h_vi = empty( (N_h,N_vi) )
        self.I_h_vi = empty( (N_h,N_vi) )
        self.I2 = 0
        self.subsid_h = empty( (N_h,1) )
        self.subsid_vi = empty( (1,N_vi) )
        self.converge = False
        self.iters = []
        self.iters_count = 0

    def copy(self):
        return deepcopy(self)


class Simulation(object):

    def __init__(self, params, households_data, probs_init, locations_data, model):
            self.params = params
            self.households_data = households_data
            self.probs_init = probs_init
            self.locations_data = locations_data
            self.model = model

            self.data_validate()
            self.init_steps()

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
        self.steps[0].S_vi = self.locations_data.S_vi_0

        for t in range(-2,self.params.T_MAX):
            factor = ((1 + self.params.pop_growth_rate)**t)
            self.steps[t].H_h = self.households_data.H_h_0 * factor

    def run(self):
        for t in range(self.params.T_MAX):
            self.model.calc(self.steps,t)
