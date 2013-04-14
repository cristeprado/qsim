import unittest

from qsim import SimulationStep, Simulation, \
        ParameterSetReader, VerticalVectorReader, HorizontalVectorReader
from numpy import array


class BaseTest(unittest.TestCase):

    def assertVectorEquals(self, v1, v2):
        msg = "Vectors are not equal: \n %s \n\n vs \n\n %s " % (v1, v2)
        self.assertTrue((v1 == v2).all(), msg)

    def assertIsClass(self, var, a_class):
        self.assertTrue(var.__class__ == a_class)


class ReaderTests(BaseTest):

    def test_read_parameters(self):
        """A parameters file can be read and loaded into a ParameterSet
        object.

        """
        reader = ParameterSetReader('test_data/parameters.txt')
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
        reader = VerticalVectorReader('test_data/vertical.txt')
        data_set = reader.get_data()

        self.assertVectorEquals(array([0,1,2]), array([0,1,2]))
        self.assertVectorEquals(array([[0],[1],[2]]), data_set.var1)
        self.assertVectorEquals(array([[1],[0],[2]]), data_set.var2)

    def test_read_horizontal_vector(self):
        """A horizontal vector file can be read and loaded into a
        DataSet

        """

        reader = HorizontalVectorReader('test_data/horizontal.txt')
        data_set = reader.get_data()

        self.assertVectorEquals(array([[11,12]]),data_set.var1)
        self.assertVectorEquals(array([[0,1]]),data_set.var2)


class SimulationTest(BaseTest):

    def setUp(self):
        self.households_data = VerticalVectorReader(
               'test_data/households_data.txt').get_data()
        self.params = ParameterSetReader('test_data/parameters.txt').get_data()
        self.locations_data = HorizontalVectorReader(
               'test_data/locations_data.txt').get_data()

        self.sim = Simulation(
               self.params, self.households_data, None, self.locations_data, None)

    def test_init_steps(self):
       """It initializes all the simulation steps."""

       self.assertEqual(self.params.T_MAX + 2, len(self.sim.steps))
       self.assertIsClass(self.sim.steps[1], SimulationStep)

       print self.sim.steps[-1].b_h
       self.assertVectorEquals(self.households_data.b_h_m1, self.sim.steps[-1].b_h)



    def test_qsim(self):
        pass

        # qsim = Qsim(params, data, model)
        # qsim.run()



if __name__ == '__main__':
    unittest.main()

