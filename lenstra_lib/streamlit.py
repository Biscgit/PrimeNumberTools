def set_default_session(state: dict):
    if state.get("is_initialized") is not None:
        return

    state["is_initialized"] = True

    state.input_curve_a = None
    state.input_curve_b = None
