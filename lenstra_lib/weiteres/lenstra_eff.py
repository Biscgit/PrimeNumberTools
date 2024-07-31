import math
import random
import time

from sympy import isprime, nextprime, factorint

import sys

sys.set_int_max_str_digits(0)


# efficient lenstra implementation on twisted edwards curves


def get_bounds(factor: int) -> (int, int):
    """Get the bounds for the Lenstra algorithm. Target is factoring p * q = n"""
    smallest_factor = len(str(factor)) / 2

    if smallest_factor <= 15:
        b_1 = 10 ** 5
        b_2 = 20 * b_1

    elif smallest_factor <= 25:
        b_1 = 10 ** 6
        b_2 = 50 * b_1

    else:
        b_1 = 10 ** 7
        b_2 = 100 * b_1

    return b_1, b_2


class EdwardsCurve:
    def __init__(self, d: int, k: int):
        self.d = d
        self.k = k

        # assert not (0 <= d <= 1), "d must not be 0"
        # assert not self.is_quadratic_residue(), "d must not be a quadratic residue mod k"

    def point(self, x: int, y: int) -> "EPEdwardsPoint":
        """Create a point on the Edwards Curve"""
        return EdwardsPoint(self, x, y).to_extended()

    @staticmethod
    def with_random(n: int) -> "EPEdwardsPoint":
        """Create a random point on the Edwards Curve"""

        while True:
            try:
                # x = random.randint(2, n - 1)
                # y = random.randint(2, n - 1)
                # d = (x ** 2 + y ** 2 - 1) * pow(x ** 2 * y ** 2, -1, n)

                u = random.randint(2, n - 1)
                x = (u ** 2 - 1) * pow(u ** 2 + 1, -1, n) % n
                y = - (u - 1) ** 2 * pow(u ** 2 + 1, -1, n) % n
                d = ((u ** 2 + 1) ** 3 * (u ** 2 - 4 * u + 1)) * pow((u - 1) ** 6 * (u + 1) ** 2, -1, n) % n

                curve = EdwardsCurve(d, n)
                point = curve.point(x, y)

                # if not curve.is_quadratic_residue():
                return point

            except ValueError:
                continue

    def is_quadratic_residue(self) -> bool:
        """use the Legendre symbol to check if d is a quadratic residue mod p"""
        return pow(self.d, (self.k - 1) // 2, self.k) == 1

    def __str__(self):
        return f"-1 * (x² + y²) = 1 + {self.d}x²y² mod {self.k}"

    def __repr__(self):
        return f"Twisted Edwards Curve with {self}"


class EdwardsPoint:
    """Regular Edwards Point"""

    def __init__(self, curve: EdwardsCurve, x: int, y: int):
        self.curve = curve
        k = curve.k
        self.x = x % k
        self.y = y % k

    def to_extended(self) -> "EPEdwardsPoint":
        return EPEdwardsPoint(self.curve, self.x, self.y, 1, self.x * self.y)


class EPEdwardsPoint:
    """ExtendedextendedEdwardsPoint"""

    def __init__(self, curve: EdwardsCurve, x: int, y: int, z: int, t: int):
        self.curve = curve
        k = curve.k
        self.x = x % k
        self.y = y % k
        self.z = z % k
        self.t = t % k

    def to_coordinates(self) -> "EdwardsPoint":
        return EdwardsPoint(
            self.curve,
            self.x * pow(self.z, -1, self.curve.k),
            self.y * pow(self.z, -1, self.curve.k),
        )

    def __add__(self, other: "EPEdwardsPoint") -> "EPEdwardsPoint":
        """Use extended coordinate on Edwards Curve for addition"""
        k = self.curve.k
        a = (self.y - self.x) * (other.y - other.x) % k
        b = (self.y + self.x) * (other.y + other.x) % k
        c = 2 * self.t * other.t * self.curve.d % k
        d = 2 * self.z * other.z % k
        e = b - a
        f = d - c
        g = d + c
        h = b + a

        z = f * g
        g = math.gcd(z, k)
        if 1 < g < k:
            print(g)
            exit(0)

        return EPEdwardsPoint(
            self.curve,
            e * f,
            g * h,
            z,
            e * h,
        )

    def double(self) -> None:
        """Use extended coordinate on Edwards Curve for doubling"""
        k = self.curve.k
        a = pow(self.x, 2, k)
        b = pow(self.y, 2, k)
        c = pow(self.z * 2, 2, k)
        h = a + b
        e = h - pow(self.x - self.y, 2, k)
        g = a - b
        f = c + g

        self.x = e * f % k
        self.y = g * h % k
        self.z = f * g % k
        self.t = e * h % k

        g = math.gcd(self.z, k)
        if 1 < g < k:
            print(g)
            exit(0)

    def __mul__(self, scalar: int) -> "EPEdwardsPoint":
        """Use double-and-add method for scalar multiplication"""
        result = self

        for position in range(scalar.bit_length() - 2, -1, -1):
            result.double()

            if scalar >> position & 0b1:
                result = result + self

        return result

    def is_infinite(self) -> bool:
        return self.x == self.t == 0 and self.y == self.z == 1

    def __repr__(self):
        print(f"Projected on P({self.x}, {self.y}, {self.z}, {self.t})")
        point = self.to_coordinates()
        return f"Twisted Edwards Point({point.x}, {point.y}) on Curve `{self.curve}`"


class BNode:
    def __init__(self, p: EPEdwardsPoint):
        self.zero: BNode | None = None
        self.one: BNode | None = None
        self.point = p

    def calculate(self, number: str, root_point: EPEdwardsPoint):
        try:
            bit, number = int(number[0]), number[1:]

            if bit == 0:
                try:
                    self.zero.calculate(number, root_point)
                except AttributeError:
                    self.zero = BNode(self.point * 2)
                    self.zero.calculate(number, root_point)

            else:
                try:
                    self.one.calculate(number, root_point)
                except AttributeError:
                    self.one = BNode(self.point * 2 + root_point)
                    self.one.calculate(number, root_point)

        except IndexError:
            return


if __name__ == '__main__':
    n = nextprime(184_791_471)
    n = n * nextprime(n * 3 + 1)
    print(f"Factorizing {n} ({len(str(n))} digits) using Lenstra's algorithm")

    b1, b2 = get_bounds(n)
    k1 = math.lcm(*[x for x in range(2, b1 + 1) if isprime(x)])
    k2 = [x for x in range(b1, b2 + 1) if isprime(x)]
    print(f"Using bounds `B₁: {b1:.0e}` and `B₂: {b2:.0e}`")

    try:
        for x in range(100):
            t = time.perf_counter()
            point = EdwardsCurve.with_random(n)

            print(f"Round {x + 1} Stage 1...")
            q = point * k1

            print(f"Round {x + 1} Stage 2...")
            node = BNode(q)
            for b2_prime in k2:
                number = f"{b2_prime:b}"[1:]
                node.calculate(number, q)

            print(f"Round {x + 1} Stage took {time.perf_counter() - t}s\n")

        print("No factors found")

    except ValueError:
        pass
