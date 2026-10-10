"""Mechanistic and numerical checks; no wet-lab validation is implied."""
from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from model import DEFAULT_PARAMS, rhs, simulate_batch, simulate_serial_dilution
from ternary_utils import simplex_grid, bary_to_xy


class ModelChecks(unittest.TestCase):
    def test_no_producer_means_no_toxin_and_no_toxin_killing(self):
        sol = simulate_batch((0, 0.005, 0.005), t_max=12)
        np.testing.assert_array_equal(sol.y[0], np.zeros_like(sol.t))
        np.testing.assert_array_equal(sol.y[3], np.zeros_like(sol.t))
        self.assertGreater(sol.y[1, -1], sol.y[1, 0])

    def test_toxin_only_changes_sensitive_derivative(self):
        without = np.array(rhs(0, [0.1, 0.2, 0.3, 0], DEFAULT_PARAMS))
        with_toxin = np.array(rhs(0, [0.1, 0.2, 0.3, 1], DEFAULT_PARAMS))
        self.assertEqual(without[0], with_toxin[0])
        self.assertEqual(without[2], with_toxin[2])
        self.assertAlmostEqual(without[1]-with_toxin[1], DEFAULT_PARAMS['kill']*0.2)

    def test_single_batch_is_finite_and_nonnegative(self):
        sol = simulate_batch((0.01/3, 0.01/3, 0.01/3), t_max=30)
        self.assertTrue(sol.success)
        self.assertTrue(np.isfinite(sol.y).all())
        self.assertGreaterEqual(sol.y.min(), -1e-12)
        fractions = sol.y[:3] / sol.y[:3].sum(axis=0)
        np.testing.assert_allclose(fractions.sum(axis=0), 1)

    def test_serial_passage_fraction_and_detection(self):
        trajectory, ext = simulate_serial_dilution((0, 0.5, 0.5), n_cycles=3)
        np.testing.assert_allclose(trajectory[1:].sum(axis=1), 1)
        self.assertEqual(ext['C'], 1)
        self.assertIsNone(ext['R'])
        self.assertIsNone(ext['S'])

    def test_grid_and_vertex_coordinates(self):
        grid = simplex_grid(28)
        self.assertEqual(len(grid), 435)
        np.testing.assert_allclose(grid.sum(axis=1), 1)
        np.testing.assert_allclose(bary_to_xy(0,1,0), (0,0))
        np.testing.assert_allclose(bary_to_xy(0,0,1), (1,0))


if __name__ == '__main__':
    unittest.main()
