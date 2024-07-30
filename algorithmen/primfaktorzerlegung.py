import math
import random

import streamlit as st

# ----------------------------------------PRIMFAKTORZERLEGUNG----------------------------------------


def ggt(a, b):
    while b:
        a, b = b, a % b
    return a


def pollard_rho(n, verbose):
    if n % 2 == 0:
        if verbose is True:
            st.write(f"Da {n} eine gerade Zahl ist ist 2 ein Primfaktor")
        return 2

    x = random.randint(1, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    if verbose is True:
        st.write(
            f"Es werden für x, y, c zufällige Werte zwischen definiert: x = {x}, y = {y} und c = {c} "
        )
    while d == 1:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = ggt(abs(x - y), n)
        if verbose is True:
            st.write(
                f" die Wert x und y  werden quadriert und c addiert. Für y ein weiteres Mal. d wird der ggT von (|(x - y)|, n).  x = {x}, y = {y} und d = {d}"
            )
        if d == n:
            return pollard_rho(n, verbose)
    if verbose is True:
        st.write(f"Da der ggT {d} ungleich 1 ist muss {d} ein Primfaktor sein")
    return d


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def factors_pollard(n, verbose):
    if n <= 1:
        return []
    if is_prime(n):
        if verbose is True:
            st.write(f"{n} ist ein Primfaktor")
        return [n]
    factor = pollard_rho(n, verbose)
    return factors_pollard(factor, verbose) + factors_pollard(n // factor, verbose)


def williams_p_plus_1(n, verbose):
    if n % 2 == 0:
        return 2
    if verbose is True:
        st.write(f"Da {n} eine gerade Zahl ist ist 2 ein weiterer Primfaktor")

    b = 100
    a = random.randint(2, n - 2)

    for j in range(2, b + 1):
        if verbose is True:
            st.write(
                f"Es wird der Rest der Potent von {a} hoch {j} modulo {n} brechnet"
            )
            st.write(f"Zudem wird der ggT von {a - 1} und {n} bestimmt. ")
        a = pow(a, j, n)
        d = ggt(a - 1, n)
        if 1 < d < n:
            if verbose is True:
                st.write(
                    f"Da der ggT ({d}) größer 1, aber kleiner {n} ist es ein Teiler."
                )
            return d

    return None


def factors_williams(n, verbose):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
        if verbose is True:
            st.write(f"Da {n} eine gerade Zahl ist ist 2 ein weiterer Primfaktor")

    while n > 1:
        factor = williams_p_plus_1(n, verbose)
        if not factor:
            factors.append(n)
            if verbose is True:
                st.write(f"{n} ist ein weiterere Primfaktor. ")
            break
        while n % factor == 0:
            if verbose is True:
                st.write(f"{factor} ist ein weiterere Primfaktor.")
            factors.append(factor)
            n //= factor

    return factors


# ----------------------------------------STREAMLIT----------------------------------------

"""st.header('Primzahlzerlegung')

option = st.selectbox("Welche Primzahlzerlegungs-Methode soll gemacht werden?", ["Pollard-Rho", "Williams", "Lenstra", "Quadratischer Sieb"], index=0)

verbose = st.checkbox("Ist eine detailierte Beschreibung gewünscht?")

number = st.number_input("Welche Zahl soll zerlegt werden?", value=1, min_value=1)

if option == "Pollard-Rho":
    factors = factors_pollard(number, verbose)
    st.write(f"Die Primfaktoren von {number} sind: ")
    st.write(factors)

if option == "Williams":
    factors = factors_williams(number, verbose)
    st.write(f"Die Primfaktoren von {number} sind: ")
    st.write(factors)"""
