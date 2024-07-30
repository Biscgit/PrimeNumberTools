import math
import random
import typing

import numpy as np


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

    a = pow(int(a), 1, int(n))
    z = 1
    while x != 0:
        if x % 2 == 0:
            a = pow(a, 2, int(n))
            x //= 2
        else:
            x -= 1
            z = pow((z * a), 1, int(n))

    return z


class quadratic_sieve:
    def __init__(self, number: int, n: int = None, b: int = None):
        self.number = number
        self.b = b or int(smoothness_bound(number))
        self.n = n or int(math.sqrt(number) / math.log(number))
        self.x = int(number ** (1 / 2)) + 1
        self.primes, self.ts = self.get_primes(number, self.b, self.x)
        self.org_mat = []
        self.unmarked = []
        self.unmarked_rows = []
        self.dependent_rows = []
        self.indexes = []
        self.perfect_square = []

    def compute_tonelli(self, prime, x, number):
        response, _ = tonnelli_shanks(int(number), int(prime))
        t1 = (
            (pow(int(-x), 1, int(prime)) - pow(int(response), 1, int(prime))) % prime
            if response is not None
            else -1
        )
        t2 = (
            (pow(int(-x), 1, int(prime)) + pow(int(response), 1, int(prime))) % prime
            if response is not None
            else -1
        )
        return t1, t2

    def compute_smooth_exponents(
        self, j: int, prime: int, i: int, x: int, number: int, y: int
    ) -> int:
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
        # Calculating array for sieving
        i_array = np.arange(self.n)
        y_array = (self.x + i_array) ** 2 - self.number
        smooth_primes = []

        for idx, y in enumerate(y_array):
            factors = self.compute_smooth_primes(idx, y, self.x, self.number)
            smooth_primes.append(
                factors
                if np.prod(self.primes**factors) == y
                else np.zeros(self.primes.shape[0], dtype=int)
            )

        fast_matrix = np.array(smooth_primes)
        perfect_square = self.fast_gaussian_elimination(fast_matrix)
        indexes = np.any(np.all(fast_matrix[:, None] == perfect_square, axis=2), axis=1)
        self.base = np.prod(np.nonzero(indexes)[0] + self.x) % self.number
        exponents = np.sum(perfect_square, axis=0)
        self.exponents = exponents
        self.exp = int(np.prod(self.primes ** (exponents / 2)) % self.number)
        self.factor1, self.factor2 = (
            math.gcd(int(self.base - self.exp), self.number),
            math.gcd(int(self.base + self.exp), self.number),
        )

    def fast_gaussian_elimination(self, matrix: np.array) -> np.array:
        org_mat = matrix.copy()
        self.org_mat = matrix.copy()
        matrix = np.mod(matrix, 2)
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
        unmarked_row = unmarked_rows_with_zeros[
            ~np.all(unmarked_rows_with_zeros == 0, axis=1)
        ][0]
        dependent_rows = np.any(
            marked_rows[:, np.newaxis, :] & unmarked_row[np.newaxis], axis=-1
        ).transpose()[0]
        perfect_zero = np.concatenate(
            (unmarked_row[np.newaxis], (marked_rows[dependent_rows, :]))
        )
        indexes = np.any(np.all(matrix[:, None] == perfect_zero, axis=2), axis=1)
        perfect_square = org_mat[indexes, :]

        self.unmarked = marked_rows
        self.unmarked_row = unmarked_row
        self.dependent_rows = dependent_rows
        self.indexes = indexes
        self.perfect_square = perfect_square
        return perfect_square


# David
def tonnelli_shanks(rhs: int, p: int) -> typing.Optional[tuple[int, int]]:
    # split p_val- 1
    s = (p - 1 & -(p - 1)).bit_length() - 1
    q = (p - 1) // pow(2, s)

    # check for shortcut
    if s == 1:
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

            except TypeError as e:
                print(e)
                return None, None

            # set common variables
            c = pow(d, 2, p)
            y = pow(y * d, 1, p)
            t = (t * pow(d, 2)) % p
            m = i

        return y, (-y) % p
