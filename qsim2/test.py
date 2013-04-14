import unittest

from qsim import SimulationStep, Simulation, MatrixReader, \
        ParameterSetReader, VerticalVectorReader, HorizontalVectorReader
from qsim.models.GqsR import Model as TestModel
from numpy import array, zeros, around


class BaseTest(unittest.TestCase):

    def assertVectorEquals(self, v1, v2):
        msg = "Vectors are not equal: \n %s \n\n vs \n\n %s " % (v1, v2)
        self.assertTrue((v1 == v2).all(), msg)

    def assertVectorAlmostEqual(self,v1,v2,places=5):
        msg = "Vectors are not almost equal: \n %s \n\n vs \n\n %s " % (v1, v2)
        self.assertVectorEquals(around(v1,places),around(v2,places))

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
        self.assertEquals(2, parameterSet.T_MAX)
        self.assertEquals(0.5, parameterSet.mu)
        self.assertEquals(0.5, parameterSet.lambd)
        self.assertEquals(100, parameterSet.iter_max)
        self.assertEquals(1e-10, parameterSet.tol)
        self.assertEquals(0.99, parameterSet.nu)
        self.assertEquals(0.1, parameterSet.pop_growth_rate)

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

    def test_read_matrix(self):
        """A matrix file can be read and loaded into a
        DataSet

        """

        reader = MatrixReader('test_data/matrix.txt')
        data_set = reader.get_data()

        self.assertVectorEquals(array([[10,20],[30,40]]),data_set.var1)

class SimulationTest(BaseTest):

    def setUp(self):
        self.households_data = VerticalVectorReader(
               'test_data/households_data.txt').get_data()
        self.params = ParameterSetReader('test_data/parameters.txt').get_data()
        self.locations_data = HorizontalVectorReader(
               'test_data/locations_data.txt').get_data()
        self.probs_init = MatrixReader('test_data/data_P_h_vi_m1.txt').get_data()

        self.model = TestModel(self.params)
        self.sim = Simulation(
               self.params, self.households_data, self.probs_init, self.locations_data, self.model)

    def test_data_validate(self):
        aux=self.locations_data.R_vi
        self.locations_data.R_vi=zeros((1,len(self.locations_data.S_vi_0)))
        self.assertRaises(ValueError,self.sim.data_validate)
        self.locations_data.R_vi=aux

    def test_init_steps(self):
        """It initializes all the simulation steps."""

        self.assertEqual(self.params.T_MAX + 2, len(self.sim.steps))
        self.assertIsClass(self.sim.steps[1], SimulationStep)

        self.assertVectorEquals(self.households_data.b_h_m1, self.sim.steps[-1].b_h)
        self.assertVectorEquals(self.probs_init.P_h_vi_m1,self.sim.steps[-1].P_h_vi)
        self.assertVectorEquals(self.locations_data.gamma_vi_0,self.sim.steps[0].gamma_vi)
        self.assertVectorEquals(self.locations_data.S_vi_0,self.sim.steps[0].S_vi)

        for t in range(-2,self.params.T_MAX):
            self.assertVectorEquals(self.sim.steps[t].H_h,self.households_data.H_h_0*(1.1**t))


    def test_run(self):
        self.sim.run()

        self.assertVectorAlmostEqual(array([1,2]),array([1.01,2.01]),places=1)
        self.assertVectorAlmostEqual(array([[110],[330],[1100]]), self.sim.steps[1].H_h)
        self.assertVectorAlmostEqual(array([[-0.71327954],[-0.2596002 ],[ 0.64432307]]), self.sim.steps[1].b_h)
        self.assertVectorAlmostEqual(array([[ 311.63426866, 307.82930307, 307.82930307, 307.82930307, 304.87782213]]), self.sim.steps[1].S_vi)

        self.assertVectorAlmostEqual(array([[ 0.07438614, 0.07116111, 0.07116111, 0.07116111, 0.06864085],[ 0.21935201, 0.21384719, 0.21384719, 0.21384719, 0.20944571],[ 0.70626185, 0.7149917,  0.7149917,  0.7149917,  0.72191344]]), self.sim.steps[1].P_h_vi)


        # qsim = Qsim(params, data, model)
        # qsim.run()



if __name__ == '__main__':
    unittest.main()

