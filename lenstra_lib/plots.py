import functools

import typing
import random

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from .common import check_num
from .lenstra import WeierstrassPoint, WeierStrassEC


@functools.lru_cache()
def valid_weierstrass(a: typing.Any, b: typing.Any, p: typing.Any) -> bool:
    if check_num(a) and check_num(b) and check_num(p):
        return only_check_weierstrass(int(a), int(b), int(p))

    return False


@functools.lru_cache()
def only_check_weierstrass(a: int, b: int, p: int) -> bool:
    return (4 * pow(a, 3) + 27 * pow(b, 2)) % p != 0


@functools.lru_cache()
def get_weierstrass_points(a: int, b: int, p: int) -> list[tuple[int, int]]:
    points = []

    for x in range(p):
        rhs = (pow(x, 3, p) + a * x + b) % p

        for y in range(p // 2 + 1):
            if pow(y, 2, p) == rhs:
                points.extend([(x, y), (x, -y % p)])

    return points


@functools.lru_cache()
def is_on_curve(a: int, b: int, p: int, x: int, y: int) -> bool:
    return (x, y) in get_weierstrass_points(a, b, p)


def draw_curve(a: int, b: int, p: int, cont: st.container, point: typing.Optional[tuple[int, int]] = None):
    with cont:
        with st.spinner("plotting..."):
            points = get_weierstrass_points(a, b, p)
            _x = [i[0] for i in points]
            _y = [i[1] for i in points]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=_x,
                y=_y,
                mode='markers',
                hovertemplate='x=%{x}<br>y=%{y}<extra></extra>',
                showlegend=False,
            ))

            # get all points with order 2 -> double for infinity
            # point_x = [_x[i] for i, y in enumerate(_y) if y == 0]

            # point in infinity
            fig.add_trace(go.Scatter(
                x=[p + p // 100],
                y=[p + p // 100],
                mode='markers',
                marker=dict(
                    size=7,
                    color=px.colors.qualitative.Plotly[0],
                ),
                hovertext=f"Point 𝓞",
                hoverinfo=["text"],
                showlegend=False,
            ))

            # highlight
            if point:
                fig.add_trace(go.Scatter(
                    x=[point[0]],
                    y=[point[1]],
                    mode='markers',
                    marker=dict(
                        size=12,
                        color=px.colors.qualitative.Plotly[1],
                    ),
                    hovertext=f"Selected<br>x={point[0]}<br>y={point[1]}",
                    hoverinfo=["text"],
                    showlegend=False,
                ))

            selected = st.plotly_chart(
                fig,
                theme="streamlit",
                use_container_width=True,
                selection_mode="points",
                on_select="rerun"
            )

            if len(selected["selection"]["points"]):
                s_point = selected["selection"]["points"][0]
                state = st.session_state
                state.input_point_x = s_point["x"]
                state.input_point_y = s_point["y"]
                state.point_highlight = True

                # ToDo: solve that it works without rerun
                st.rerun()

        st.markdown(fr"Plotted Weiterstrass Curve $\; y^2 \equiv x^3 + {a}x + {b} \; mod \; {p}$")
