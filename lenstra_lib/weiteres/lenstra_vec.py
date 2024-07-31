import copy
import math
import random
import numpy as np
import sympy as sm
import time

# Default Lenstra implementation with vectorized operations


class TwistedEdwardsLenstra:
    # set to multiple of 16 (for efficient ssid and avx operations)
    array_size = 16

    def __init__(self, n: int):
        self.n = n

        # set boundaries
        self.b1 = 10 ** 5
        self.b2 = 50 * self.b1

        # define curves
        curve_pairs = []
        while len(curve_pairs) < TwistedEdwardsLenstra.array_size:
            try:
                x = random.randint(1, n - 1)
                y = random.randint(1, n - 1)
                d = (x ** 2 + y ** 2 - 1) * pow(x ** 2 * y ** 2, -1, n)

                pair = np.array([d, x, y])
                curve_pairs.append(self.to_projective(pair))

            except ValueError:
                continue

        # points are defined as arrays located at [d, x, y, z, t]
        self.points = np.array(curve_pairs).transpose()

    @staticmethod
    def is_quadratic_residue(n: int, p: int) -> bool:
        """use the Legendre symbol to check if d is a quadratic residue mod p"""
        return pow(n, (p - 1) // 2, p) == 1

    @staticmethod
    def to_projective(pair: np.ndarray) -> np.ndarray:
        """Projects (x, y) to (X, Y, Z, T) on a Twisted Edwards curve"""

        d, x, y = pair
        return np.array([d, x, y, 1, x * y])

    def __getitem__(self, item: int) -> np.ndarray:
        return self.points[item]

    def __setitem__(self, key: int, value: np.ndarray) -> None:
        self.points[key] = value

    def add(self, other: np.ndarray) -> None:
        """use point addition with extended projective edwards points"""
        a = (self[2] - self[1]) * (other[2] - other[1]) % self.n
        b = (self[2] + self[1]) * (other[2] + other[1]) % self.n
        c = self[4] * other[4] * self[0] * 2 % self.n
        d = self[3] * other[3] * 2 % self.n
        e = b - a
        f = d - c
        g = d + c
        h = b + a

        self.points[1] = e * f % self.n
        self.points[2] = g * h % self.n
        self.points[3] = f * g % self.n
        self.points[4] = e * h % self.n

    def double(self) -> None:
        """use point doubling with extended projective edwards points"""
        a = self[1] * self[1] % self.n
        b = self[2] * self[2] % self.n
        c = self[3] * self[3] * 2 % self.n
        h = a + b
        e = (h - (self[1] - self[2]) ** 2) % self.n
        g = a - b
        f = c + g

        self.points[1] = e * f % self.n
        self.points[2] = g * h % self.n
        self.points[3] = f * g % self.n
        self.points[4] = e * h % self.n

    def multiply(self, scalar: int):
        default = self.points.copy()

        for position in range(scalar.bit_length() - 2, -1, -1):
            self.double()

            arr_g: np.ndarray = np.gcd(self[3], self.n)
            if np.any((arr_g > 1) & (arr_g < self.n)):
                print(arr_g)
                return

            if scalar >> position & 0b1:
                self.add(default)

                arr_g: np.ndarray = np.gcd(self[3], self.n)
                if np.any((arr_g > 1) & (arr_g < self.n)):
                    print(arr_g)
                    return

    def lenstra(self) -> int | None:
        print(f"Factorizing {self.n} using Lenstra's algorithm")

        k1 = math.lcm(*[x for x in range(2, self.b1 + 1) if sm.isprime(x)])
        k2 = np.array([x for x in range(self.b1, self.b2 + 1) if sm.isprime(x)])
        print(f"Using bounds `B₁: {self.b1:.0e}` and `B₂: {self.b2:.0e}`")

        t = time.perf_counter()

        print(f"Stage 1...")
        self.multiply(k1)

        print(f"Stage 2...")
        # clone = copy.deepcopy(self)

        print(f"Stages took {time.perf_counter() - t}s\n")


if __name__ == '__main__':
    n = sm.nextprime(184_791_471)
    n = n * sm.nextprime(n * 3 + 1)

    curve = TwistedEdwardsLenstra(n)
    curve.lenstra()
