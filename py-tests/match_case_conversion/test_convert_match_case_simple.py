from typing import Any
from pyvercompat.utils import ensure_same_functionality


def match_single_values(p):
    match p:
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case _:
            return 600


def match_single_value_with_alias(p):
    match p:
        case 1:
            return 0
        case x:
            return x + 1


def match_sequence(p: list[int]):
    match p:
        case [0, 1]:
            return 0
        case [1]:
            return 1
        case []:
            return -1
        case _:
            return -2


def match_sequence_with_alias(p: list[int]):
    match p:
        case [0, y]:
            return y
        case [x]:
            return 1 + x
        case []:
            return -1
        case _:
            return -2


def match_object_with_alias(x: int, y: int):
    class A:
        def __init__(self, x, y) -> None:
            self.x = x
            self.y = y

    p = A(x, y)
    match p:
        case A(x=0, y=y):
            return f"y axis, position {x}"
        case A(x=x, y=0):
            return f"x axis, position {y}"
        case A(x=x, y=y):
            return f"{(x, y)} is on canvas"
        case _:
            raise NotImplementedError


def match_list_of_objects(p: list[tuple[int, int]]):
    class A:
        def __init__(self, x, y) -> None:
            self.x = x
            self.y = y

    p = [A(x, y) for x, y in p]

    match p:
        case [A(x=0, y=y)]:
            return f"y axis, position {y}"
        case [A(x=0, y=y), A(x=x, y=0)]:
            return f"length is 2, first altitude is {y}, second x pos is {x}"
        case []:
            return f"no point"
        case _:
            return len(p)


def match_sequence_with_mapping():
    sumx = 0
    for item in [
        {"x": 2},
        {"x": 0, "y": 1},
        {"x": 0, "y": 2},
        {"x": 1, "y": 0},
        {"x": 2, "y": 0},
        
    ]:
        match item:
            case {"x": x}:
                sumx += 1 + 6 + x+8
            case {"x": 0, "y": y}:
                sumx += y + 1
            case {"x": x, "y": 0}:
                sumx += x + 2
            case {"x": x, "y": y}:
                sumx += 9 + y + x

            case _:
                raise NotImplementedError
    return sumx


def match_with_evaluators():

    it = iter([1, 2, 3])
    # for _ in range(3):
    next(it)
    match next(it):
        case 1:
            return 1
        case 2:
            return 2


def test_match_single_values():
    ensure_same_functionality(
        match_single_values,
        [(1,), (2,), (3,), (4,)],
    )
    ensure_same_functionality(match_single_value_with_alias, [(1,), (2,), (3,), (4,)])
    ensure_same_functionality(
        match_sequence, [([0, 1],), ([0, 1, 2],), ([1],), ([],), ([0, 1, 2, 3],)], True
    )
    ensure_same_functionality(
        match_sequence_with_alias,
        [([0, 1],), ([0, 1, 2],), ([1],), ([],), ([0, 1, 2, 3],)],
    )
    ensure_same_functionality(
        match_object_with_alias,
        [(0, 1), (1, 0), (1, 1), (-1, -1)],
    )
    ensure_same_functionality(
        match_list_of_objects,
        [
            ([(0, 1)],),
            ([(0, 1), (1, 0)],),
            ([(1, 0), (1, 1), (0, 2)],),
        ],
    )
    ensure_same_functionality(
        match_with_evaluators,
        [tuple([])],
        True,
    )
    ensure_same_functionality(
        match_sequence_with_mapping,
        [tuple([])],
        True,
    )

