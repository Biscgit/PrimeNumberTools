import random

import streamlit as st

from lenstra_lib import *

# set state
state = st.session_state
set_default_session(state)

# main site - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Lenstra factorization")
factorize: str = st.text_input(
    "Set your Number $n$ to factorize",
    placeholder="Type number here",
    on_change=lambda: check_num(factorize)
)

if factorize:
    if not check_num(factorize):
        st.warning('Value is not a number!', icon="⚠️")
    else:
        st.button("Factorize!", type="primary")
else:
    st.info("Enter a number to factorize", icon="ℹ️")

st.header("Weierstrass Curve")
st.markdown(r"With $\; y^2 = x^3 + Ax + B \; mod \; n$")

cols = st.columns([8, 8, 2, 4])
with cols[2]:
    st.container(height=12, border=False)
    if st.button(
            "🔀",
            disabled=not check_num(factorize),
            use_container_width=True,
    ):
        limit = int(factorize) or 100

        while True:
            a = random.randint(1, int(limit))
            b = random.randint(1, int(limit))

            if (4 * pow(a, 3) + 27 * pow(b, 2)) % limit != 0:
                break

        state.input_curve_a = str(a)
        state.input_curve_b = str(b)

with cols[0]:
    state["input_curve_a"] = st.text_input(
        "Parameter A",
        value=state.input_curve_a,
        placeholder="Curve parameter A"
    )

with cols[1]:
    state["input_curve_b"] = st.text_input(
        "Parameter B",
        value=state.input_curve_b,
        placeholder="Curve parameter B"
    )

with cols[3]:
    st.container(height=12, border=False)
    if int(factorize) > 10_000:
        st.button(
            "$n$ too large",
            disabled=True,
            use_container_width=True,
        )

    else:
        plot_curve = st.button(
            "Plot curve",
            use_container_width=True
        )

if plot_curve:
    a = int(state.input_curve_a)
    b = int(state.input_curve_b)
    p = int(factorize)

    draw_curve(a, b, p)
