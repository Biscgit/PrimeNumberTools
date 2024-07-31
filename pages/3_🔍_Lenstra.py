import math
import random
import typing

import streamlit as st

from algorithmen.primzahltest import millerrabin
from lenstra_lib import *

# set state
state = st.session_state
set_default_session(state)

MAX_PLOT_P = 25_000


def reset_highlighted():
    state.highlighted_points = []


def toggle_highlight(_x: typing.Any, _y: typing.Any):
    pair = (_x, _y)

    if pair in state.highlighted_points:
        state.highlighted_points.remove(pair)
    else:
        state.highlighted_points.append(pair)


def set_random_curve():
    curve_limit = int(factorize) or 100

    while True:
        _a = random.randint(1, int(curve_limit))
        _b = random.randint(1, int(curve_limit))

        if valid_weierstrass(_a, _b, curve_limit):
            break

    state.input_curve_a = str(_a)
    state.input_curve_b = str(_b)

    reset_highlighted()


def set_random_point() -> bool:
    old_pair = state.input_point_x, state.input_point_y
    if old_pair in state.highlighted_points:
        state.highlighted_points.remove(old_pair)

    points = get_weierstrass_points(
        int(state.input_curve_a),
        int(state.input_curve_b),
        int(factorize),
    )
    if points:
        _p = random.choice(points)

        state.input_point_x = str(_p[0])
        state.input_point_y = str(_p[1])

        toggle_highlight(state.input_point_x, state.input_point_y)
        return True

    return False


# main site - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
sidebar_content()


st.title("Lenstra elliptic-curve factorization")

cols = st.columns([23, 2])
with cols[0]:
    factorize: str = st.text_input(
        "Set your Number $n$ to factorize",
        max_chars=20,
        placeholder="Type number here",
        on_change=reset_highlighted,
    )

with cols[1]:
    st.container(height=12, border=False)
    if st.button(
        "🔀",
        key="full_random_select",
        use_container_width=True,
        disabled=not check_num(factorize),
    ):
        fact = int(factorize)
        limit = min([fact, int(1e9)])

        x = random.randint(0, limit) % fact
        y = random.randint(0, limit) % fact
        a = random.randint(0, limit) % fact

        state.input_point_x = x
        state.input_point_y = y
        state.input_curve_a = a
        state.input_curve_b = (pow(y, 2) - pow(x, 3) - a * x) % fact

        reset_highlighted()

call_factorize = False
if factorize:

    def is_prime(product: int) -> bool:
        return millerrabin(product, 20, verbose=False)

    if not check_num(factorize):
        st.error(r"$n\:$ is not a number!", icon="⚠️")

    elif is_prime(int(factorize)):
        st.warning(r"$n\:$ is probably prime!", icon="⚠️")


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
        r"Parameter $\:A$", value=state.input_curve_a, placeholder="Curve parameter A"
    )

with cols[1]:
    state.input_curve_b = st.text_input(
        r"Parameter $\:B$", value=state.input_curve_b, placeholder="Curve parameter B"
    )


def can_plot() -> bool:
    return valid_weierstrass(state.input_curve_a, state.input_curve_b, factorize)


with cols[3]:
    st.container(height=12, border=False)
    if check_num(factorize) and int(factorize) > MAX_PLOT_P:
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
        st.error(
            "Your chosen parameters result in an invalid elliptic curve!", icon="❌"
        )

else:
    st.info("Enter elliptic curve parameters or select random ones", icon="ℹ️")

curve_plot = st.container()

st.header("Point on Curve")
cols = st.columns([8, 8, 2, 4, 1])
place_holder = st.container()
with cols[2]:
    st.container(height=12, border=False)
    if st.button(
        "🔀",
        key="button_point",
        disabled=check_num(factorize) and int(factorize) > MAX_PLOT_P or not can_plot(),
        use_container_width=True,
    ):
        if not set_random_point():
            with place_holder:
                st.warning(r"The curve has no points!", icon="⚠️")

with cols[0]:
    state.input_point_x = st.text_input(
        r"Point $\:X$", value=state.input_point_x, placeholder="Coordinate X"
    )

with cols[1]:
    state.input_point_y = st.text_input(
        r"Point $\:Y$", value=state.input_point_y, placeholder="Coordinate Y"
    )

on_curve = True
if not all([state.input_point_x, state.input_point_y]):
    st.info("Enter a point or select random ones", icon="ℹ️")

elif not check_num(state.input_point_x) or not check_num(state.input_point_y):
    st.error("One of the coordinates is not a number!", icon="❌")

elif check_num(factorize) and not (
    on_curve := is_on_curve(
        int(state.input_curve_a),
        int(state.input_curve_b),
        int(factorize),
        int(state.input_point_x),
        int(state.input_point_y),
    )
):
    st.error("Your point is not on the curve!", icon="❌")

with cols[3]:
    st.container(height=12, border=False)
    if st.button(
        "Highlight",
        use_container_width=True,
        disabled=not can_plot()
        or not check_num(state.input_point_x)
        or not check_num(state.input_point_y)
        or check_num(factorize)
        and int(factorize) > MAX_PLOT_P,
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

if (
    not all(
        [
            check_num(x)
            for x in [
                factorize,
                state.input_curve_a,
                state.input_curve_b,
                state.input_point_x,
                state.input_point_y,
            ]
        ]
    )
    or not on_curve
):
    st.info("Enter missing or change incorrect values to start algorithm", icon="ℹ️")

else:
    number = int(factorize)
    if number % 2 == 0:
        st.warning(r"Number is even $\,→\,$ divisible by 2", icon="⚠️")

    else:
        with st.spinner("calculating..."):
            n = int(factorize)
            a = int(state.input_curve_a) % n
            b = int(state.input_curve_b) % n
            x = int(state.input_point_x) % n
            y = int(state.input_point_y) % n

            mode_options = ["Prime factors", "Factorial n!"]
            mode_index = mode_options.index(
                st.selectbox(
                    "Calculation Mode", mode_options, key="select_factorization_mode"
                )
            )

            items = []
            iterator = streamlit_lenstra(
                (a, b, n), (x, y), mode_index, max_factor=10_000
            )

            while True:
                try:
                    items.insert(0, next(iterator))

                except InvalidCurve:
                    st.stop()

                except StopIteration as result:
                    if result.value:
                        result = int(result.value)
                        divider = n // result

                        cols = st.columns([18, 4, 1])
                        with cols[0]:
                            st.container(height=1, border=False)
                            st.success(
                                rf"Found factor $\, {result} \,$ with $\, {n} = {result} \cdot {divider}$",
                                icon="✅",
                            )

                        with cols[1]:
                            st.container(height=9, border=False)
                            limit_size = max([result, divider]) > int(MAX_PLOT_P * 0.2)

                            if limit_size:
                                st.button(
                                    "$n$ too large",
                                    key="button_plot_factor_curves",
                                    disabled=True,
                                    use_container_width=True,
                                )

                            else:
                                if st.button(
                                    "Plot curves",
                                    key="button_plot_factor_curves",
                                    use_container_width=True,
                                    disabled=not can_plot(),
                                ):
                                    state.plot_factor_curves = (
                                        not state.plot_factor_curves
                                    )

                        with cols[2]:
                            st.container(height=15, border=False)
                            if state.plot_factor_curves:
                                st.write("🟥")
                            else:
                                st.write("⬛️")

                        if (
                            state.plot_factor_curves
                            and check_num(factorize)
                            and not limit_size
                        ):
                            container = st.container()

                            a = int(state.input_curve_a)
                            b = int(state.input_curve_b)

                            draw_multi_curve(
                                container, a, b, int(factorize), [result, divider]
                            )

                            for i, num in enumerate([result, divider], 1):
                                st.markdown(
                                    rf"**Curve {i}:** $\; y^2 \equiv x^3 + {a % num}x + {b % num} \; mod \; {num}\,$"
                                )

                    else:
                        # with result_widget:
                        if items[0].current_point.y < math.inf:
                            st.error(
                                r"Found no valid factor: Exceeded operations limit",
                                icon="❌",
                            )
                        else:
                            st.error(
                                r"Found no valid factor: $\, gcd \,$ resulted in $1$ or $n$",
                                icon="❌",
                            )

                    break

            st.header("Last points")
            size = len(items)

            calculation_container = st.container()

            if st.button("Load more", disabled=state.max_show > size):
                state.max_show += 10

            with calculation_container:
                last_item = items.pop(-1)
                last_operation = -1
                base_index = -1

                containers: dict[int, st.container] = {}
                cont_titles: dict[int, st.container] = {}

                for i, item in enumerate(items):
                    if i > state.max_show:
                        break

                    if item.scalar != last_operation:
                        # this is very magic, do not touch
                        if last_operation > 0:
                            containers[last_operation].__exit__(None, None, None)

                        last_operation = item.scalar
                        containers[last_operation] = st.container(border=True)
                        containers[last_operation].__enter__()

                        calc_index = (
                            size
                            - i
                            - last_operation.bit_length()
                            - last_operation.bit_count()
                            + 1
                        )

                        # special case with breaking while calculating a scalar
                        modifier = 0
                        if i == 0 and last_operation > 2:
                            operations = (
                                last_operation.bit_length()
                                + last_operation.bit_count()
                                - 2
                            )
                            actual = len(
                                [x for x in items if x.scalar == last_operation]
                            )
                            modifier = max(operations - actual, 0)

                        base_index = calc_index + modifier
                        st.markdown(
                            rf"Calculating $\,{last_operation} \cdot P_{{{base_index}}} = "
                            rf"P_{{{size - i - 1 + modifier}}}$"
                        )

                    col_outer = st.columns([1, 15])
                    with col_outer[0]:
                        s = {True: "➕", False: "✖️", None: "◾️"}.get(
                            item.is_operation_add
                        )
                        st.markdown(
                            f"""<div style="font-size: 40px;">{s}</div>""",
                            unsafe_allow_html=True,
                        )

                    with col_outer[1]:
                        with st.container(border=True):
                            cols = st.columns([9, 21, 3])

                            with cols[0]:
                                if i < size - 1:
                                    if item.is_operation_add:
                                        st.markdown(
                                            rf"$P_{{{size - i - 1}}}({item.current_point.x}|{item.current_point.y})\\"
                                            rf"= P_{{{base_index}}} + P_{{{size - i - 2}}}$"
                                        )

                                    else:
                                        st.markdown(
                                            rf"$P_{{{size - i - 1}}}({item.current_point.x}|{item.current_point.y})\\"
                                            rf"= 2 \cdot P_{{{size - i - 2}}}$"
                                        )

                            with cols[1]:
                                calculation = ""

                                if item.is_operation_add:
                                    calculation += (
                                        rf"s \equiv {item.slope} \equiv \frac{{{item.base_point.y} - "
                                        rf"{item.last_point.y}}}{{{item.base_point.x} - {item.last_point.x}}} "
                                        rf"\; mod \; {item.current_point.curve.p}"
                                    )

                                else:
                                    calculation += (
                                        rf"s \equiv {item.slope} \equiv \frac{{3 \cdot {item.last_point.x}^2 + "
                                        rf"{item.current_point.curve.a}}}{{2 \cdot {item.last_point.y}}} "
                                        rf"\; mod \; {item.current_point.curve.p}"
                                    )

                                if math.inf > item.slope > 0:
                                    calculation += (
                                        rf"\\ x \equiv {item.slope}^2 - {item.last_point.x} - {item.base_point.x} "
                                        rf"\; mod \; {item.current_point.curve.p}"
                                        rf"\\ y \equiv {item.slope} \cdot ({item.last_point.x} - "
                                        rf"{item.current_point.x}) - {item.last_point.y} "
                                        rf"\; mod \; {item.current_point.curve.p}"
                                    )

                                else:
                                    calculation += rf"\\ q = gcd({item.last_point.x} - {item.current_point.x}, {n})"

                                st.markdown(f"${calculation}$")

                        with cols[2]:
                            if st.button(
                                "💡",
                                key=f"res_select_{i}",
                                disabled=i == 0 or not can_plot(),
                            ):
                                toggle_highlight(
                                    item.current_point.x, item.current_point.y
                                )

                            if (
                                item.current_point.x,
                                item.current_point.y,
                            ) in state.highlighted_points:
                                st.markdown(
                                    '<p style="text-align: center;">🔴</p>',
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.markdown(
                                    '<p style="text-align: center;">⚫</p>',
                                    unsafe_allow_html=True,
                                )

# plot curve: here because of updates
if state.plot_curve and check_num(factorize) and int(factorize) < MAX_PLOT_P:
    a = int(state.input_curve_a)
    b = int(state.input_curve_b)
    p = int(factorize)

    draw_curve(a, b, p, curve_plot, state.highlighted_points)

# long calc: 4567, 884, 1479, 423, 3129
# long calc: 5767, 3494, 4821, 1623, 1169

st.container(height=30, border=False)
st.html('<p style="color: #ffffff40;">David Horvát, 2024 ❤️</p>')
