# Lenstra elliptic-curve factorization in Python
# by David Horvát, 2024

from __future__ import annotations

import dataclasses

import typing

import math
import sympy


@dataclasses.dataclass
class OperationData:
    current_point: WeierstrassPoint
    last_point: typing.Optional[WeierstrassPoint]
    base_point: typing.Optional[WeierstrassPoint]
    is_operation_add: typing.Optional[bool]
    slope: int | math.inf
    scalar: int


class InvalidCurve(Exception):
    pass


class WeierStrassEC:
    """Creates a Weierstrass elliptic curve from a, b and p"""

    def __init__(self, a: int, b: int, p: int):
        if (4 * pow(a, 3) + 27 * pow(b, 2)) % p == 0:
            raise InvalidCurve("Invalid curve parameters `a` and `b`")

        self.a = a
        self.b = b
        self.p = p

    def __eq__(self, other: WeierStrassEC) -> bool:
        return self.a == other.a and self.b == other.b and self.p == other.p

    def point(self, x: int, y: int | math.inf) -> WeierstrassPoint:
        """get point directly from the curve"""
        return WeierstrassPoint(x, y, self)


class WeierstrassPoint:
    """Defines a Point on an elliptic curve"""

    def __init__(self, x: int, y: int | math.inf, ecc: WeierStrassEC):
        self.curve = ecc
        self.x = x % ecc.p
        self.y = int(y % ecc.p) if math.isfinite(y) else y

    def is_infinite(self) -> bool:
        return math.isinf(self.y)

    def is_on_curve(self) -> bool:
        p = self.curve.p
        return pow(self.y, 2, p) % p == (pow(self.x, 3, p) + self.curve.a * self.x + self.curve.b) % p

    def __repr__(self) -> str:
        curve = self.curve

        if self.is_infinite():
            return f"on `EC[a={curve.a}, b={curve.b}, p={curve.p}]` with `Point[x={self.x}, y=∞]`"

        return f"on `EC[a={curve.a}, b={curve.b}, p={curve.p}]` with `Point[x={self.x}, y={self.y}]`"

    def __eq__(self, other: WeierstrassPoint) -> bool:
        return self.x == other.x and self.y == other.y

    def add(self, other: WeierstrassPoint) -> tuple[WeierstrassPoint, int | math.inf]:
        """Adds two points on the same elliptic curve
        Add the same point for point-doubling"""

        curve = self.curve

        # points must be on the same curve
        if curve != other.curve:
            raise Exception("Adding points from different curves")

        # match for infinite point
        if self.is_infinite():
            return WeierstrassPoint(self.x, math.inf, curve), math.inf
        if other.is_infinite():
            return WeierstrassPoint(other.x, math.inf, curve), math.inf

        # calculate slope s
        try:
            s = self.get_slope(other)

        except (ValueError, ZeroDivisionError):
            return WeierstrassPoint(other.x, math.inf, curve), math.inf

        # calculate new coordinates x and y
        x = (pow(s, 2) - self.x - other.x) % curve.p
        y = (s * (self.x - x) - self.y) % curve.p

        return WeierstrassPoint(x, y, curve), s

    def double(self) -> tuple[WeierstrassPoint, int]:
        return self.add(self)

    def get_slope(self, other: WeierstrassPoint) -> int:
        """Calculates the slope of adding two points/doubling.
        Raises ValueError or ZeroDivisionError for an infinite slope"""

        p = self.curve.p

        # point doubling
        if self == other:
            denominator = (2 * self.y)
            numerator = (3 * pow(self.x, 2) + self.curve.a) % p

        # point addition
        else:
            denominator = (other.x - self.x)
            numerator = (other.y - self.y) % p

        return numerator * pow(denominator, -1, p) % p

    def lenstra_streamlit(self, max_mul: int, mode: int) -> typing.Generator[OperationData, None, typing.Optional[int]]:
        point: WeierstrassPoint = self
        n: int = self.curve.p

        # @functools.lru_cache(maxsize=1024)
        def lenstra_mul(scalar: int) -> typing.Generator[OperationData, None, int]:
            """Multiplies point by a scalar.
            On finding a point in infinity return true
            yields OperationData
            returns is_finished"""

            nonlocal point
            base_point = point

            for position in range(scalar.bit_length() - 1, 0, -1):
                bit = scalar >> (position - 1) & 0b1

                # double
                next_point, slope = point.double()

                # yield next_point, False, scalar, slope
                yield OperationData(
                    current_point=next_point,
                    last_point=point,
                    base_point=point,
                    is_operation_add=False,
                    slope=slope,
                    scalar=scalar,
                )
                if next_point.is_infinite():
                    return math.gcd((point.x - next_point.x) % n, n)

                assert next_point.is_on_curve()
                point = next_point

                # add
                if bit:
                    next_point, slope = point.add(base_point)

                    yield OperationData(
                        current_point=next_point,
                        last_point=point,
                        base_point=base_point,
                        is_operation_add=True,
                        slope=slope,
                        scalar=scalar,
                    )
                    if next_point.is_infinite():
                        return math.gcd((point.x - next_point.x) % n, n)

                    assert next_point.is_on_curve()
                    point = next_point

        if mode == 0:
            primes = sympy.primerange(sympy.prime(max_mul) + 1)
        elif mode == 1:
            primes = range(2, max_mul + 2).__iter__()
        else:
            raise NotImplementedError(f"Mode with index {mode} not implemented")

        while True:
            try:
                factor = next(primes)
            except StopIteration:
                return None

            res = yield from lenstra_mul(factor)

            if res:
                return res if n > res > 1 else None

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.curve.p, self.curve.a, self.curve.b))


def streamlit_lenstra(curve: tuple, point: tuple, mode: int, max_factor: int = 3_000) -> typing.Generator \
        [OperationData, None, typing.Optional[int]]:
    """Yields points while calculating"""

    x, y = point
    a, b, n = curve

    # div by two
    if (n - 1) & 0b1:
        return

    elliptic_curve = WeierStrassEC(a, b, n)
    start_point = WeierstrassPoint(x, y, elliptic_curve)
    yield OperationData(
        current_point=start_point,
        last_point=None,
        base_point=None,
        is_operation_add=None,
        scalar=1,
        slope=0,
    )

    factor = yield from start_point.lenstra_streamlit(max_factor, mode)
    return factor
