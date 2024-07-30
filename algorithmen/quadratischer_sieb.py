import math
import random
import typing

import numpy as np

from algorithmen.primzahltest import ggt


def smoothness_bound(N):
    logN = math.log(N)
    logLogN = math.log(logN)
    B = math.exp(math.sqrt(logN * logLogN / 2))
    return B


def quad_residue(a, n):
    # checks if a is quad residue of n
    q = (n - 1) // 2
    x = q**1
    if x == 0:
        return 1

    a = a % n
    z = 1
    while x != 0:
        if x % 2 == 0:
            a = (a**2) % n
            x //= 2
        else:
            x -= 1
            z = (z * a) % n

    return z


class quadratic_sieve:
    def __init__(self, number: int, n: int = None, b: int = None):
        self.number = number
        self.b = b or int(smoothness_bound(number))
        self.n = n or int(math.sqrt(number) / math.log(number))
        print(self.b, self.n)
        self.x = int(number ** (1 / 2)) + 1
        self.primes, self.ts = self.get_primes(number, self.b, self.x)

    def compute_tonelli(self, prime, x, number):
        response, _ = tonnelli_shanks(number, int(prime))
        t1 = (-x - response) % prime
        t2 = (-x + response) % prime
        print(t1, t2)
        return t1, t2

    def compute_smooth_exponents(
        self, j: int, prime: int, i: int, x: int, number: int, y: int
    ) -> int:
        # print("Smooth_exponent: ", j, prime)
        if not any(i % prime == k for k in self.ts[j]):
            return 0
        exponent = 0
        while True:
            if y % prime != 0:
                break
            y = y // prime
            exponent += 1
        return exponent

    def compute_smooth_primes(self, i: int, y: int, x: int, number: int) -> np.array:
        # print("Smooth_prime: ", y, i)
        return np.vectorize(self.compute_smooth_exponents)(
            np.arange(len(self.primes)), self.primes, i, x, number, y
        )

    def get_primes(self, number: int, b: int, x: int):
        # Calculating relevant primes
        numbers = np.arange(2, b + 1)
        is_prime = np.ones(len(numbers), dtype=bool)
        for i in range(2, int(b**0.5) + 1):
            if is_prime[i - 2]:
                is_prime[i * i - 2 : b + 1 : i] = False
        quad_residues = np.vectorize(quad_residue)(numbers, number).astype(bool)
        primes = numbers[is_prime & quad_residues]
        # Calculating steps to skip
        ts = np.vectorize(self.compute_tonelli)(primes, x, number)
        return primes, np.vstack(ts).transpose()

    def factorise(self):
        # (N**1/2 + x) - N = y_not_works for x in range(1, n)
        # y_not_works factorise this
        # only use those whos are under the smoothness bound (b)
        # calculate a perfect prime with multiplying different y_not_works's
        # do it over a matrix, with only having all exponents % 2 -> y
        # x**2 = y**2 % N
        # gcd(x-y, N)
        # n > b !!

        # Calculating array for sieving
        i_array = np.arange(self.n)
        y_array = (self.x + i_array) ** 2 - self.number
        smooth_primes = []
        print("Start")
        smooth_primes = []

        for idx, y in enumerate(y_array):
            factors = self.compute_smooth_primes(idx, y, self.x, self.number)
            smooth_primes.append(
                factors
                if np.prod(self.primes**factors) == y
                else np.zeros(self.primes.shape[0], dtype=int)
            )

        fast_matrix = np.array(smooth_primes)
        # print(fast_matrix)
        perfect_square = self.fast_gaussian_elimination(fast_matrix)
        indexes = np.any(np.all(fast_matrix[:, None] == perfect_square, axis=2), axis=1)
        a = np.prod(np.nonzero(indexes)[0] + self.x) % self.number
        exponents = np.sum(perfect_square, axis=0) / 2
        b = np.prod(self.primes**exponents) % self.number
        print(a)
        print(b)
        return ggt(a - b, self.number), ggt(a + b, self.number)

    def fast_gaussian_elimination(self, matrix: np.array) -> np.array:
        org_mat = matrix.copy()
        matrix = np.mod(matrix, 2)
        print(matrix)
        rows, columns = matrix.shape
        row_is_marked = np.zeros(rows, dtype=bool)
        for i in range(columns):
            pivot = np.nonzero(matrix[:, i] == 1)[-1]
            if len(pivot) != 0:
                row_is_marked[pivot[0]] = True
                cond = matrix[pivot[0], :] == 1
                cond[i] = False
                matrix[:, cond] ^= matrix[:, [i]]
        marked_rows = matrix[row_is_marked, :]
        unmarked_rows_with_zeros = matrix[~row_is_marked, :]
        unmarked_rows = unmarked_rows_with_zeros[
            ~np.all(unmarked_rows_with_zeros == 0, axis=1)
        ][0]
        dependent_rows = np.any(
            marked_rows[:, np.newaxis, :] & unmarked_rows[np.newaxis], axis=-1
        ).transpose()[0]
        perfect_zero = np.concatenate(
            (unmarked_rows[np.newaxis], (marked_rows[dependent_rows, :]))
        )
        indexes = np.any(np.all(matrix[:, None] == perfect_zero, axis=2), axis=1)
        perfect_square = org_mat[indexes, :]

        self.marked = marked_rows
        self.unmarked = unmarked_rows
        self.dependent = dependent_rows
        self.indexes = indexes
        return perfect_square


# David
def tonnelli_shanks(rhs: int, p: int) -> typing.Optional[tuple[int, int]]:
    # split p_val- 1
    s = (p - 1 & -(p - 1)).bit_length() - 1
    q = (p - 1) // pow(2, s)

    # check for shortcut
    if s == 1:
        print(f"Shortcut possible because {s=}")

        y_pos = pow(rhs, (p + 1) // 4, p)
        y_neg = pow(-rhs, (p + 1) // 4, p)

        return y_pos, y_neg

    else:
        # find a random z with Legendre-Symbol = -1
        z = 0
        while pow(z, (p - 1) // 2, p) != p - 1:
            z = random.randint(0, p)

        # determine common variables
        c = pow(z, q, p)
        y = pow(rhs, (q + 1) // 2)
        t = pow(rhs, q)
        m = s

        while t % p != 1:
            # determine smallest i
            i = 1
            while pow(t, pow(2, i), p) != 1:
                i += 1

                # check for point at 0
                if i > m:
                    return 0, 0

            # if not all values are int, no result is possible
            try:
                d = pow(c, pow(2, m - i - 1), p)

            except TypeError:
                return None, None

            # set common variables
            c = pow(d, 2, p)
            y = (y * d) % p
            t = (t * pow(d, 2)) % p
            m = i

        return y, (-y) % p
        """primes = [
            x
            for x in range(2, b + 1)
            if all(x % i != 0 for i in range(2, int(x**0.5) + 1))
            and quad_residue(x, number)
        ]"""
        """for j in primes:
            response, _ = tonnelli_shanks(number, j)
            t1 = (-x - response) % j
            t2 = (-x + response) % j
            ts.append((t1, t2))"""

        """for i in range(n):
            smooth_exponents = []
            y = (x + i) ** 2 - number
            for j, p in enumerate(primes):
                if not any(i % p == k for k in ts[j]):
                    smooth_exponents.append(0)
                    continue
                exponent = 0
                while True:
                    if y % p != 0:
                        break
                    y = y // p
                    exponent += 1
                smooth_exponents.append(exponent % 2)
            smooth_primes.append(smooth_exponents) if y == 1 else None"""
