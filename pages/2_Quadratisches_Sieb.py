import numpy as np
import streamlit as st

from algorithmen.quadratischer_sieb import quadratic_sieve
from lenstra_lib import check_num


def nice_primes(primes, row):
    factors = []
    for j, column in enumerate(row):
        if column == 0:
            continue
        factors += [rf"{primes[j]}^{{{column}}}"]
    return "*".join(factors)


def sieving(primes, mat, x, number):
    lines = []
    for i, row in enumerate(mat):
        factors = nice_primes(primes, row)
        if factors == "":
            continue
        lines += [rf"${x+i}^2 - {number} \equiv {np.prod(primes**row)} = {factors}$"]
    return lines


def factorise(factorize):
    if not check_num(factorize):
        st.warning("Value is not a number!", icon="⚠️")
        return
    number = int(factorize)
    f = quadratic_sieve(number)
    f.factorise()
    return f


st.header("Quadratischer Sieb")
factorize: str = st.text_input(
    "Set your Number $n$ to factorize",
    placeholder="Type number here",
)

if factorize == "":
    st.info("Enter a number to factorize", icon="ℹ️")
else:
    try:
        f = factorise(factorize)
        sieving_result = sieving(f.primes, f.org_mat, f.x, f.number)
        with st.expander("Sieving", expanded=True):
            for i in sieving_result:
                st.write(i)

        with st.expander("Fast Gaussian Elimination", expanded=True):
            for i in f.org_mat:
                st.write(f"{i}")

        with st.expander("Setting relation", expanded=True):
            exponents = []
            for row in f.perfect_square:
                exponents += [f"({nice_primes(f.primes, row)})"]
            numbers = np.nonzero(f.indexes)[0] + f.x
            st.write(
                rf"$ {"*".join(numbers.astype(str) + "^2")} \equiv {"*".join(exponents)} \% {f.number}$"
            )
            st.write(
                rf"$ ({"*".join(numbers.astype(str))})^2 \equiv {nice_primes(f.primes, f.exponents)} \% {f.number}$"
            )
            st.write(
                rf"$ {np.prod(numbers)}^2 \equiv {nice_primes(f.primes, f.exponents//2)} \% {f.number}$"
            )
            st.write(
                rf"$ {np.prod(numbers) % f.number}^2 \equiv {np.prod(f.primes**(f.exponents//2))}^2 \% {f.number}$"
            )
            st.write(rf"Faktor 1: $gcd({f.base} - {f.exp}, {f.number}) = {f.factor1}$")
            st.write(rf"Faktor 2: $gcd({f.base} + {f.exp}, {f.number}) = {f.factor2}$")
            # st.write(f"Faktor 1 ist: {f.factor1}\nFaktor 2 ist: {f.factor2}")
    except Exception as e:
        print(e)
        st.warning("Can't use your input!", icon="⚠️")
