import typing
import random

import streamlit as st
import plotly.express as px


def get_weierstrass_points(a: int, b: int, p: int) -> list[tuple[int, int]]:
    points = []
    for x in range(p):
        rhs = (pow(x, 3, p) + a * x + b) % p
        for y in range(p // 2 + 1):
            if pow(y, 2, p) == rhs:
                points.extend([(x, y), (x, -y % p)])
    return points


def draw_curve(a: int, b: int, p: int):
    with st.spinner("plotting..."):
        points = get_weierstrass_points(a, b, p)
        _x = [x[0] for x in points]
        _y = [y[1] for y in points]

        fig = px.scatter(
            x=_x,
            y=_y,
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.markdown(fr"Plotted Weiterstrass Curve $\; y^2 = x^3 + {a}x + {b} \; mod \; {p}$")
