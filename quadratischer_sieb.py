import streamlit as st

from algorithmen.quadratischer_sieb import quadratic_sieve
from lenstra_lib import check_num


def factorise():
    number = int(factorize)
    f = quadratic_sieve(number)
    st.write(f.factorise())


st.header("Quadratischer Sieb")
factorize: str = st.text_input(
    "Set your Number $n$ to factorize",
    placeholder="Type number here",
    on_change=lambda: check_num(factorize),
)

if factorize:
    if not check_num(factorize):
        st.warning("Value is not a number!", icon="⚠️")
    else:
        st.button("Factorize!", type="primary", on_click=factorise)
else:
    st.info("Enter a number to factorize", icon="ℹ️")
