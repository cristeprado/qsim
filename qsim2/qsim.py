from numpy import array

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
            setattr(out, vector['name'].strip(), array([vector['values']]))

        return out


class DataSet(object):
    pass

class ParameterSet(DataSet):
    pass
