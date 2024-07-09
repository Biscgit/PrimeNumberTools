import streamlit as st
from lenstra_lib import *


st.header("Lenstra factorization")
value = st.text_input(
    "Set your Number to factorize",
    placeholder="Type number here",
    on_change=check_num
)

if value:
    if not check_num():
        st.warning('Value is not a number!', icon="⚠️")
    else:
        st.button("Factorize!")

