import unittest
import sympy as sy
from graph_plotter import PlotWidget


class TestPlotWidged(unittest.TestCase):
    def test_limit(self):
        """
        Test for checking function limits
        """
        x = sy.Symbol('x')
        func = sy.sin(x) / x
        result = sy.limit(func, x, 0)
        self.assertEqual(result, 1)

    def test_derivative(self):
        """
        Test for checking function derivative
        """
        x = sy.Symbol('x')
        func = sy.sin(x)
        result = sy.diff(func, x)
        self.assertEqual(result, sy.cos(x))

    def test_double_derivative(self):
        """
        Test for checking function double derivative
        """
        x = sy.Symbol('x')
        func = sy.sin(x)
        result = sy.diff(func, x, 2)
        self.assertEqual(result, -sy.sin(x))


if __name__ == '__main__':
    unittest.main()
