import functools

# from multiprocessing import Process, Queue


@functools.lru_cache()
def check_num(value) -> bool:
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


"""def get_points_compute(a: int, b: int, p: int, queue: Queue):
    from sage.all import EllipticCurve, GF

    field = GF(p)
    curve = EllipticCurve(field, [a, b])
    points = curve.points()

    result = [(p, p.order()) for p in points]
    queue.put(result)


@functools.lru_cache()
def old_get_points(a: int, b: int, p: int) -> list[tuple[int, int], int]:
    queue = Queue()
    process = Process(target=get_points_compute, args=(a, b, p, queue))
    print("here")
    process.start()
    print("here")
    process.join()

    result = queue.get()
    return result"""

# This does not work
# print(get_points(3, 11, 17))
