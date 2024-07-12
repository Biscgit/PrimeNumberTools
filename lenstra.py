import typing

import streamlit as st

from lenstra_lib import *

# set state
state = st.session_state
set_default_session(state)


def reset_highlighted():
    state.highlighted_points = []


def toggle_highlight(x: typing.Any, y: typing.Any):
    pair = (x, y)

    if pair in state.highlighted_points:
        state.highlighted_points.remove(pair)
    else:
        state.highlighted_points.append(pair)


def set_random_curve():
    limit = int(factorize) or 100

    while True:
        _a = random.randint(1, int(limit))
        _b = random.randint(1, int(limit))

        if valid_weierstrass(_a, _b, limit):
            break

    state.input_curve_a = str(_a)
    state.input_curve_b = str(_b)

    reset_highlighted()


def set_random_point():
    old_pair = state.input_point_x, state.input_point_y
    if old_pair in state.highlighted_points:
        state.highlighted_points.remove(old_pair)

    points = get_weierstrass_points(
        int(state.input_curve_a),
        int(state.input_curve_b),
        int(factorize),
    )
    _p = random.choice(points)

    state.input_point_x = str(_p[0])
    state.input_point_y = str(_p[1])

    toggle_highlight(state.input_point_x, state.input_point_y)


# main site - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.title("Lenstra elliptic-curve factorization")

factorize: str = st.text_input(
    "Set your Number $n$ to factorize",
    placeholder="Type number here",
    on_change=reset_highlighted,
)

call_factorize = False
if factorize:
    if not check_num(factorize):
        st.error(r'$n\:$ is not a number!', icon="⚠️")

else:
    st.info("Enter a number to factorize", icon="ℹ️")

# set params here so it renders correctly
if call_factorize:
    if not all([state.input_curve_a, state.input_curve_b]):
        set_random_curve()

    if not all([state.input_point_x, state.input_point_y]):
        set_random_point()

st.header("Weierstrass Curve")
st.markdown(r"With $\; y^2 \equiv x^3 + Ax + B \; mod \; n$")

cols = st.columns([8, 8, 2, 4, 1])
with cols[2]:
    st.container(height=12, border=False)
    if st.button(
            "🔀",
            key="button_curve",
            disabled=not check_num(factorize),
            use_container_width=True,
    ):
        set_random_curve()

with cols[0]:
    state.input_curve_a = st.text_input(
        r"Parameter $\:A$",
        value=state.input_curve_a,
        placeholder="Curve parameter A"
    )

with cols[1]:
    state.input_curve_b = st.text_input(
        r"Parameter $\:B$",
        value=state.input_curve_b,
        placeholder="Curve parameter B"
    )


def can_plot() -> bool:
    return valid_weierstrass(state.input_curve_a, state.input_curve_b, factorize)


with cols[3]:
    st.container(height=12, border=False)
    if check_num(factorize) and int(factorize) > 10_000:
        st.button(
            "$n$ too large",
            disabled=True,
            use_container_width=True,
        )

    else:
        if st.button(
                "Plot curve",
                key="button_plot_curve",
                use_container_width=True,
                disabled=not can_plot(),
        ):
            state.plot_curve = not state.plot_curve

with cols[4]:
    st.container(height=18, border=False)
    if state.plot_curve:
        st.write("🟥")
    else:
        st.write("⬛️")

if state.input_curve_a is not None and state.input_curve_b is not None:
    if not can_plot() and factorize not in [None, ""]:
        st.error('Your chosen parameters result in an invalid elliptic curve!', icon="❌")

else:
    st.info("Enter elliptic curve parameters or select random ones", icon="ℹ️")

curve_plot = st.container()

st.header("Point on Curve")
cols = st.columns([8, 8, 2, 4, 1])
with cols[2]:
    st.container(height=12, border=False)
    if st.button(
            "🔀",
            key="button_point",
            disabled=check_num(factorize) and int(factorize) > 10_000 or not can_plot(),
            use_container_width=True,
    ):
        set_random_point()

with cols[0]:
    state.input_point_x = st.text_input(
        r"Point $\:X$",
        value=state.input_point_x,
        placeholder="Coordinate X"
    )

with cols[1]:
    state.input_point_y = st.text_input(
        r"Point $\:Y$",
        value=state.input_point_y,
        placeholder="Coordinate Y"
    )

on_curve = True
if not all([state.input_point_x, state.input_point_y]):
    st.info("Enter a point or select random ones", icon="ℹ️")

elif not check_num(state.input_point_x) or not check_num(state.input_point_y):
    st.error("One of the coordinates is not a number!", icon="❌")

elif check_num(factorize) and not (on_curve := is_on_curve(
        int(state.input_curve_a),
        int(state.input_curve_b),
        int(factorize),
        int(state.input_point_x),
        int(state.input_point_y),
)):
    st.error("Your point is not on the curve!", icon="❌")

with cols[3]:
    st.container(height=12, border=False)
    if st.button(
            "Highlight",
            use_container_width=True,
            disabled=not can_plot() or not check_num(state.input_point_x) or not check_num(
                state.input_point_y) or check_num(factorize) and int(factorize) > 10_000,
    ):
        toggle_highlight(state.input_point_x, state.input_point_y)

with cols[4]:
    st.container(height=18, border=False)
    if (state.input_point_x, state.input_point_y) in state.highlighted_points:
        st.write("🔴")
    else:
        st.write("⚫")

# execute factorization
st.header("Factorization")
# call_try_factorize = st.button("Try until found", type="secondary", use_container_width=True)

if not all([check_num(x) for x in [
    factorize,
    state.input_curve_a,
    state.input_curve_b,
    state.input_point_x,
    state.input_point_y
]]) or not on_curve:
    st.info("Enter missing or change incorrect values to start algorithm", icon="ℹ️")

else:
    number = int(factorize)
    if number % 2 == 0:
        st.warning(r"Number is even $\,→\,$ divisible by 2", icon="⚠️")

    else:
        max_show = 10

        with st.spinner("calculating..."):
            n = int(factorize)
            a = int(state.input_curve_a) % n
            b = int(state.input_curve_b) % n
            x = int(state.input_point_x) % n
            y = int(state.input_point_y) % n

            items = []
            iterator = streamlit_lenstra((a, b, n), (x, y))

            while True:
                try:
                    items.insert(0, next(iterator))

                except StopIteration as result:
                    if result.value:
                        result = int(result.value)
                        st.success(
                            fr"Found factor $\, {result} \,$ with $\, {n}\, \vert \, {result} = {n // result}$",
                            icon="✅"
                        )

                    else:
                        # with result_widget:
                        st.error(fr"Found no valid factor", icon="❌")

                    break

            st.header("Last points")
            size = len(items)

            calculation_container = st.container()

            if st.button("Load more", disabled=max_show < size):
                max_show += 10

            with calculation_container:
                last = items.pop(-1)

                for i, item in enumerate(items):
                    if i > max_show:
                        break

                    col_outer = st.columns([1, 15])
                    with col_outer[0]:
                        s = {
                            True: "➕",
                            False: "✖️",
                            None: "◾️"
                        }.get(item[1])
                        st.markdown(f"""<div style="font-size: 40px;">{s}</div>""", unsafe_allow_html=True)

                    with col_outer[1]:
                        with st.container(border=True):
                            cols = st.columns([4, 6, 8, 4, 1])

                            with cols[0]:
                                if i < size - 1:
                                    if item[1]:
                                        st.markdown(fr"$P_0 + P_{{{size - i - 2}}} = $")
                                    else:
                                        st.markdown(fr"$2 \cdot P_{{{size - i - 2}}} = $")

                            with cols[1]:
                                st.markdown(f"$P_{{{size - i - 1}}}({item[0].x}|{item[0].y})$")

                            with cols[2]:
                                st.markdown(item[2])
                            #     before = items[i + 1][0]
                            #     if item[1]:
                            #         st.markdown(fr"$s \equiv \frac{{{before.y} - {current.y}}}$")

                            with cols[3]:
                                if st.button(
                                        "Highlight",
                                        use_container_width=True,
                                        key=f"res_select_{i}",
                                        disabled=not can_plot(),
                                ):
                                    toggle_highlight(item[0].x, item[0].y)

                            with cols[4]:
                                if (item[0].x, item[0].y) in state.highlighted_points:
                                    st.write("🔴")
                                else:
                                    st.write("⚫")

# plot curve: here because of updates
if state.plot_curve and check_num(factorize):
    a = int(state.input_curve_a)
    b = int(state.input_curve_b)
    p = int(factorize)

    # point = (int(state.input_point_x), int(state.input_point_y)) if state.point_highlight else None
    draw_curve(a, b, p, curve_plot, state.highlighted_points)
