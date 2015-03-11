import unittest
import numpy as np
from sejits_caffe.types.array import Array, smap, smap2


class TestMap(unittest.TestCase):
    def _check(self, actual, expected):
        np.testing.assert_allclose(actual, expected)

    def test_simple(self):
        a = Array.rand(256, 256).astype(np.float32)

        @smap
        def fn(x):
            if x > 0:
                return x
            else:
                return 0

        actual = Array.zeros(a.shape, np.float32)
        fn(a, actual)
        expected = np.copy(a)
        expected[expected < 0] = 0
        self._check(actual, expected)


    def test_two_inputs(self):
        a = Array.rand(256, 256).astype(np.float32) * 255 - 128
        b = Array.rand(256, 256).astype(np.float32) * 255 - 128
        negative_slope = 0

        @smap
        def fn(x, y):
            if x > 0:
                return y
            else:
                return negative_slope * y

        actual = Array.zeros(a.shape, np.float32)
        fn(a, b, actual)
        expected = b
        expected[a <= 0] *= negative_slope
        self._check(actual, expected)


if __name__ == '__main__':
    unittest.main()
