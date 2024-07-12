def set_default_session(state: dict):
    if state.get("is_initialized") is not None:
        return

    state["is_initialized"] = True

    state.input_curve_a = None
    state.input_curve_b = None
    state.plot_curve = False

    state.input_point_x = None
    state.input_point_y = None
    state.point_highlight = False

    state.max_show = 10
    state.calculation_show = False
