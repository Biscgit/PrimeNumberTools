import random
import typing

import numpy as np
import scipy.linalg as sc


def quad_residue(a, n):
    # checks if a is quad residue of n
    l = 1
    q = (n - 1) // 2
    x = q**l
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


def factorise(number: int, n: int, b: int):
    # (N**1/2 + x) - N = y_not_works for x in range(1, n)
    # y_not_works factorise this
    # only use those whos are under the smoothness bound (b)
    # calculate a perfect prime with multiplying different y_not_works's
    # do it over a matrix, with only having all exponents % 2 -> y
    # x**2 = y**2 % N
    # gcd(x-y, N)
    # n > b !!
    primes = [
        x
        for x in range(2, b + 1)
        if all(x % i != 0 for i in range(2, int(x**0.5) + 1))
        and quad_residue(x, number)
    ]
    x = int(number ** (1 / 2)) + 1
    smooth_primes = []
    ts = []
    for j in primes:
        response, _ = tonnelli_shanks(number, j)
        t1 = (-x - response) % j
        t2 = (-x + response) % j
        ts.append((t1, t2))
    for i in range(n):
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
        smooth_primes.append(smooth_exponents) if y == 1 else None
    print(np.array(smooth_primes))
    print(np.transpose(smooth_primes))
    print(sc.null_space(np.transpose(smooth_primes)))


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
