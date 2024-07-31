import numpy as np
import streamlit as st

from algorithmen.primzahltest import millerrabin
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
    if millerrabin(int(factorize), 20, False):
        st.warning(r"$n\:$ is probably prime!", icon="⚠️")
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
        if f is not None:
            sieving_result = sieving(f.primes, f.org_mat, f.x, f.number)
            with st.expander("Explaination"):
                st.write(
                    r"Fermat's factorization is very simple its based on the equation of the differnce of two squares ($x^2 - y^2 = (x-y)(x+y)$). Thats also corresponds to this: $x^2 - y^2 = N$, that we are able to rewrite to $x^2 - N = y^2$. For the algo x is predefind ($x = \left \lceil{\sqrt{N}}\right \rceil $), will be increased everytime until a y is found that is a perfect square. As this only works for little numbers, as there a not so much perfect squares, the quadratic sieve was implemented, which is based on the Fermat's factorization, but a lot faster. It has slightly modified the formula: $x^2 - y^2 = kN, k>1$, otherwise it would just be Fermat. So if this applies, the greatest common divisor from $x-y$ and $N$ ($gcd(x-y,N)$ is a factor of N, as $gcd(x+y, n)$ is the other factor."
                )
            with st.expander("Sieving", expanded=True):
                st.write(
                    "So first we need to calculate $x$. And calculate $(x+i)^2-N for i in n, but now we don't look for a perfect sqaure, but factorize our results we got."
                )
                st.write(
                    rf"$x = {f.x} = \left \lceil{{\sqrt{{{f.number}}}}} \right \rceil$"
                )
                st.write(
                    rf"$b = {f.b} = \exp\left( \sqrt{{\frac{{\log {f.number} \log \log {f.number}}}{{2}}}} \right)$"
                )
                st.write(
                    rf"$n = {f.n} =  \left \lfloor{{\frac{{\sqrt{{{f.number}}}}}{{\log{{{f.number}}}}}}} \right \rfloor$"
                )
                st.write(
                    f"For simple reason only numbers, that have primefactors under {f.b} will be printed."
                )
                for i in sieving_result:
                    st.write(i)

            with st.expander("Fast Gaussian Elimination"):
                st.markdown(
                    "Next we want to combine some of the previous results to get a perfect square. That is easily done over matrix of the $exponents \% 2$. This is best done with matrices. You just need to calculate the left null space. The [Fast Gaussian Elimination](https://www.cs.umd.edu/~gasarch/TOPICS/factoring/fastgauss.pdf) is a fast way of doing that"
                )

                for i in f.org_mat:
                    st.write(f"{i}")
                st.write("Out of this, we will get this:")
                st.write("")
                for i in f.perfect_square:
                    st.write(f"{i}")
                st.write("and this adds up to:")
                st.write(f"{np.zeros(f.org_mat.shape[1], dtype=int)}")

            with st.expander("Calculating factors", expanded=True):
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
                st.write(
                    rf"Faktor 1: $gcd({f.base} - {f.exp}, {f.number}) = {f.factor1}$"
                )
                st.write(
                    rf"Faktor 2: $gcd({f.base} + {f.exp}, {f.number}) = {f.factor2}$"
                )
                # st.write(f"Faktor 1 ist: {f.factor1}\nFaktor 2 ist: {f.factor2}")
    except Exception as e:
        print(e)
        st.warning("Can't use your input!", icon="⚠️")
