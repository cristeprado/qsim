from numpy import array, empty, newaxis, zeros, ones

class DataReader(object):

    def __init__(self, filename):
        self.file_handler = open(filename)

class ParameterSetReader(DataReader):

    def get_data(self):
        out = ParameterSet()
        for line in self.file_handler:
            var_name, var_value = tuple(line.split(','))
            try:
                var_value = int(var_value)
            except ValueError:
                var_value = float(var_value)
            setattr(out, var_name, var_value)
        return out

class VerticalVectorReader(DataReader):

    def get_data(self):
        lines = self.file_handler.readlines()
        vectors = []
        out = DataSet()

        var_names = lines[0].split(',')

        for name in var_names:
            vectors.append({
                'name': name,
                'values': []
            })

        for line in lines[1:]:
            values = [float(x) for x in line.split(',')]
            for i, value in enumerate(values):
                vectors[i]['values'].append(value)

        for vector in vectors:
            setattr(out, vector['name'].strip(), array(vector['values'])[:,newaxis])

        return out

class HorizontalVectorReader(DataReader):
    def get_data(self):
        out = DataSet()
        for line in self.file_handler:
            line_values=tuple(line.split(','))
            var_name, var_value = line_values[0],line_values[1:]
            var_value = map(float,var_value)
            setattr(out, var_name, array(var_value)[newaxis,:])
        return out


class DataSet(object):
    pass


class ParameterSet(DataSet):
    pass


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


class Simulation(object):

    def __init__(self, params, households_data, probs_init, locations_data, model):
            self.params = params
            self.households_data = households_data
            self.probs_init = probs_init
            self.locations_data = locations_data
            self.model = model

            self.init_steps()


    def make_step(self):
        return SimulationStep(
                len(self.households_data.H_h_0), len(self.locations_data.S_vi_0))

    def init_steps(self):
        self.steps = [self.make_step() for t in range(0, params.T_MAX + 2)]


