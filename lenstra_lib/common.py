def check_num(value) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False
