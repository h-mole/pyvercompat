from typing import Literal


def get_symbol_priority(kind: Literal["binary", "unary"], symbol):
    """
    Get the priority of symbols.
    """
    if kind == "binary":
        return {
            "&&": 6,
            "||": 6,
            "^": 6,
            ">=": 5,
            "<=": 5,
            ">": 5,
            "<": 5,
            "==": 5,
            "!=": 5,
            "+": 4,
            "-": 4,
            "<<": 4,
            ">>": 4,
            "*": 3,
            "/": 3,
            "%": 3,
        }[symbol]
    else:
        return {
            "A<>": 10
        }[symbol]


def get_expr_priority(expr: "Expr"):
    match expr:
        case BinaryOperator():
            return get_symbol_priority("binary", expr.operator)
        case UnaryOperator():
            return get_symbol_priority("unary", expr.operator)
        case Identifier() | Const():
            return -1  # Highest priority
        case _:
            raise NotImplementedError(expr)


class Expr:
    def to_dict(self):
        new_dict = {}
        for k, v in self.__dict__.items():
            if isinstance(v, Expr):
                new_dict[k] = v.to_dict()
            else:
                new_dict[k] = v
        return new_dict

    def unparse(self):
        """
        Unparse and print the LTL formula.
        """
        raise NotImplementedError


class Identifier(Expr):
    def __init__(self, name: str) -> None:
        self.name = name

    # def __str__(self) -> str:
    #     return self.name

    def unparse(self):
        return self.name


class Const(Expr):
    def __init__(self, value: str, type: str) -> None:
        self.value = value
        self.type = type

    # def __str__(self) -> str:
    #     return self.value

    def unparse(self):
        return str(self.value)


class UnaryOperator(Expr):
    def __init__(self, operator, operand) -> None:
        self.operator = operator
        self.operand = operand

    # def __str__(self) -> str:
    #     return f"({self.operator} {self.operand})"

    def unparse(self):
        priority_this = get_expr_priority(self)
        priority_operator = get_expr_priority(self.operand)
        operand_parsed = self.operand.unparse()
        if priority_operator>=priority_this:
            return f"{self.operator} ({operand_parsed})"
        else:
            return f"{self.operator} {operand_parsed}"


class BinaryOperator(Expr):
    def __init__(self, left, operator, right) -> None:
        self.left: Expr = left
        self.operator = operator
        self.right: Expr = right

    # def __str__(self) -> str:
    #     return f"({self.left} {self.operator} {self.right})"

    def unparse(self):
        """
        Compare the priority on this level (priority_this) and
            the sub-expressions (priority_left, priority_right).
        """

        priority_this = get_expr_priority(self)
        priority_left = get_expr_priority(self.left)
        priority_right = get_expr_priority(self.right)
        left_unparsed = self.left.unparse()
        right_unparsed = self.right.unparse()
        print("unparsed", left_unparsed, right_unparsed)
        # If left operand does not have priority
        # then add brackets
        if priority_left >= priority_this:
            left_unparsed = f"({left_unparsed})"
        # If right operand does not have priority
        # then add brackets
        if priority_right >= priority_this:
            right_unparsed = f"({right_unparsed})"
        return f"{left_unparsed}{self.operator}{right_unparsed}"
