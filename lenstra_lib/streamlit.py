import streamlit as st


def set_default_session(state: dict):
    if state.get("is_initialized") is not None:
        return

    state["is_initialized"] = True

    state.input_curve_a = None
    state.input_curve_b = None
    state.plot_curve = False

    state.input_point_x = None
    state.input_point_y = None
    state.highlighted_points = []

    state.max_show = 10
    state.plot_factor_curves = False


def sidebar_content():
    st.sidebar.success("Lenstra's Faktorisierung ausgewählt!")
    st.sidebar.container(height=25, border=False)
    st.sidebar.markdown("Klicke einen der Buttons um mehr über Lenstra zu erfahren!")

    sb_cols = st.sidebar.columns(3)

    with sb_cols[0]:

        st.link_button(
            "Wiki",
            "https://en.wikipedia.org/wiki/Lenstra_elliptic-curve_factorization",
            use_container_width=True
        )

    with sb_cols[1]:
        st.link_button(
            "Paper",
            "https://wstein.org/edu/124/lenstra/lenstra.pdf",
            use_container_width=True
        )

    with sb_cols[2]:
        st.link_button(
            "Code",
            "https://github.com/Biscgit/ecc_collection/blob/main/lenstra.rs",
            use_container_width=True
        )
