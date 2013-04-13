import unittest

import qsim
from numpy import array


class QSimTest(unittest.TestCase):

    def assertVectorEquals(self, v1, v2):
        self.assertTrue((v1 == v2).all())


    def test_read_parameters(self):
        """A parameters file can be read and loaded into a ParameterSet
        object.

        """
        reader = qsim.ParameterSetReader('test_data/parameters.txt')
        parameterSet = reader.get_data()

        self.assertEquals(int, type(parameterSet.T_MAX))
        self.assertEquals(30, parameterSet.T_MAX)
        self.assertEquals(0.5, parameterSet.mu)
        self.assertEquals(0.5, parameterSet.lambd)
        self.assertEquals(100, parameterSet.iter_max)
        self.assertEquals(1e-10, parameterSet.tol)
        self.assertEquals(0.99, parameterSet.nu)

    def test_read_vertical_vector(self):
        """A vertical vector file can be read and loaded into a
        DataSet.

        """
        reader = qsim.VerticalVectorReader('test_data/vertical.txt')
        data_set = reader.get_data()

        self.assertVectorEquals(array([0,1,2]), array([0,1,2]))
        self.assertVectorEquals(array([[0,1,2]]), data_set.var1)
        self.assertVectorEquals(array([[1,0,2]]), data_set.var2)


    def test_qsim(self):
        pass

        # qsim = Qsim(params, data, model)
        # qsim.run()



if __name__ == '__main__':
    unittest.main()

