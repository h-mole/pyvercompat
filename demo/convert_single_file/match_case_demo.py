def f(a):
    match a:
        case 1:
            return
        case [1, x]:
            return x
        case {"a": 1}:
            return a
        case _:
            pass