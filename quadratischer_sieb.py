import streamlit as st

from lenstra_lib import check_num

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
        st.button("Factorize!", type="primary")
else:
    st.info("Enter a number to factorize", icon="ℹ️")
