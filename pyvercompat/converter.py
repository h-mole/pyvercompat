from typing import Any, Union
import ast


def create_length_cmp(seq: ast.expr, expected_length: ast.expr):
    """
    Create the AST of length-comparison expressions such as  `len(x) == 0`
    """
    return ast.Compare(
        left=ast.Call(func=ast.Name(id="len"), args=[seq], keywords=[]),
        ops=[ast.Eq()],
        comparators=[expected_length],
    )


def create_instance_cmp(obj: ast.expr, expected_cls: Union[tuple[ast.expr], ast.expr]):
    """
    Create the AST of type checking such as `isinstance(x, ClassA)`
    """
    return ast.Call(
        func=ast.Name(id="isinstance"),
        args=[obj, expected_cls],
        keywords=[],
    )


def create_getattr_ast(obj: ast.expr, attr: str):
    """
    Create the AST of expressions such as `getattr(a, "abc")`
    """
    return ast.Call(
        func=ast.Name(id="getattr"),
        args=[obj, ast.Constant(attr)],
        keywords=[],
    )


PatternVisitorReturns = tuple[ast.expr, list[ast.Assign]]


class PatternVisitor(ast.NodeVisitor):
    """
    Generates conditional expression from the subject of match node
        and the patterns in one `ast.match_case`

    `PatternVisitor.visit` will return a tuple:
        (`conditional expression`, `list[assignment to created variables]`)
    """

    def __init__(self, subject: ast.expr):
        self.subject = subject

    def visit_MatchSequence(self, node: ast.MatchSequence) -> PatternVisitorReturns:
        conditions: list[ast.expr] = []
        # Collect created variables
        variable_assignments: list[ast.Assign] = []
        for i, pattern_seq_item in enumerate(node.patterns):
            # Assume the subject of match is a list `lst`
            # create a subscript expression `lst[i]``
            current_comparator = ast.Subscript(
                value=self.subject, slice=ast.Constant(i)
            )
            # Visit the sequence item
            #   to create comparison expression
            seq_item_cmp, vars = PatternVisitor(current_comparator).visit(
                pattern_seq_item
            )
            variable_assignments.extend(vars)
            conditions.append(seq_item_cmp)

        length_cmp_ast = create_length_cmp(self.subject, ast.Constant(len(conditions)))
        conditions = [length_cmp_ast] + conditions
        match conditions:
            case [expr]:
                return expr, variable_assignments
            case _:
                return (
                    ast.BoolOp(
                        ast.And(),
                        conditions,
                    ),
                    variable_assignments,
                )

    def visit_MatchOr(self, node: ast.MatchOr) -> PatternVisitorReturns:
        conditions: list[ast.expr] = []
        for i, pattern_item in enumerate(node.patterns):
            # Visit the sequence item
            #   to create comparison expression
            seq_item_cmp, vars = PatternVisitor(self.subject).visit(pattern_item)

            conditions.append(seq_item_cmp)
        return ast.BoolOp(ast.Or(), conditions), []

    def visit_MatchClass(self, node: ast.MatchClass) -> PatternVisitorReturns:
        # Collect valid instances
        instance_cmp = create_instance_cmp(self.subject, node.cls)
        # Collect attribute comparisons
        attribute_comparisons: list[ast.expr] = []
        # Collect created variables
        variable_assignments: list[ast.Assign] = []
        for kwd_attr, kwd_pattern in zip(node.kwd_attrs, node.kwd_patterns):
            match kwd_pattern:
                case ast.MatchAs(name=name):
                    # Create the variable assignments
                    variable_assignments.append(
                        ast.Assign(
                            [ast.Name(id=name)],
                            create_getattr_ast(self.subject, kwd_attr),
                            lineno=None,
                        )
                    )
                case _:
                    # Create the getattr AST of `self.subject`'s attribute `kwd_attr`
                    getattr_ast = create_getattr_ast(self.subject, kwd_attr)
                    # Create the comparison AST of `self.subject`'s attribute `kwd_attr`
                    #   and expected attribute value
                    comparison_ast, vars = PatternVisitor(getattr_ast).visit(
                        kwd_pattern
                    )
                    attribute_comparisons.append(comparison_ast)
        return (
            ast.BoolOp(ast.And(), [instance_cmp] + attribute_comparisons),
            variable_assignments,
        )

    def visit_MatchAs(self, node: ast.MatchAs) -> PatternVisitorReturns:
        match node:
            case ast.MatchAs(pattern=None, name=None):
                return ast.Constant(True), []
            case ast.MatchAs(pattern=None, name=name):
                return ast.Constant(True), [
                    ast.Assign([ast.Name(name, ast.Store())], self.subject, lineno=None)
                ]
            case _:
                raise NotImplementedError(ast.unparse(node))

    def visit_MatchValue(self, node: ast.MatchValue) -> PatternVisitorReturns:
        return ast.Compare(self.subject, [ast.Eq()], [node.value]), []

    def visit_MatchSingleton(self, node: ast.MatchSingleton) -> Any:
        """
        According to https://docs.python.org/3/library/ast.html#ast.MatchSingleton, `ast.MatchSingleton` is used for comparing
        None, True, False using `is` operator.
        """
        return ast.Compare(self.subject, [ast.Is()], [ast.Constant(node.value)]), []
        # return super().visit_MatchSingleton(node)

    def visit_MatchMapping(self, node: ast.MatchMapping) -> PatternVisitorReturns:
        print(ast.dump(node))
        # Conditions generated in the mapping
        conditions: list[ast.expr] = []
        # Collect created variables
        variable_assignments: list[ast.Assign] = []
        for key, pattern in zip(node.keys, node.patterns):
            current_dict_value_ast = ast.Subscript(value=self.subject, slice=key)
            # Visit the mapping value item
            #   to create comparison expression
            seq_item_cmp, vars = PatternVisitor(current_dict_value_ast).visit(pattern)
            variable_assignments.extend(vars)
            conditions.append(
                ast.BoolOp(
                    ast.And(),
                    [ast.Compare(key, [ast.In()], [self.subject]), seq_item_cmp],
                )
            )
        # raise NotImplementedError()
        # length_cmp_ast = create_length_cmp(self.subject, ast.Constant(len(conditions)))
        # conditions = [length_cmp_ast] + conditions
        match conditions:
            case [expr]:
                return expr, variable_assignments
            case _:
                return (
                    ast.BoolOp(
                        ast.And(),
                        conditions,
                    ),
                    variable_assignments,
                )

    def visit(self, node: ast.AST) -> PatternVisitorReturns:
        return super().visit(node)


class CaseVisitor(ast.NodeVisitor):
    """
    The method `.visit()` returns a tuple, (if-else predicate, if-else body)
    """

    def __init__(self, subject: ast.expr):
        self.subject = subject

    def visit_match_case(self, node: ast.match_case) -> tuple[ast.AST, list[ast.stmt]]:
        ret = PatternVisitor(self.subject).visit(node.pattern)
        assert ret is not None, node.pattern
        pattern_expr, vars = ret
        return pattern_expr, vars + node.body


class MainConverter(ast.NodeVisitor):
    """
    `.visit()` method returns a tuple `(extra_stmts_before_if, converted_if_else_structure)`

    `extra_stmts_before_if` are the created statements to be placed before if-else structure.

    For example, if we have stmt like:

    ```python
    match call(y):
        case [1, 2, 3]:
            ...
        case []:
            ...
    ```
    the expression `call(y)` will be evaluated every time in the generated if-else branches.
    So we create a new value `subject_value` to store `call(y)`'s value.
    """

    def visit_Match(self, node: ast.Match) -> tuple[list[ast.Assign], ast.If]:
        # If subject is not a Name or Constant, we need to create a new value to store the result.
        extra_stmts_before_if: list[ast.Assign] = []
        match node.subject:
            case ast.Name() | ast.Constant():
                subject = node.subject
            case _:
                var_to_store_subject = ast.Name(
                    id=f"_match_subject_value__line_{node.lineno}"
                )
                extra_stmts_before_if.append(
                    ast.Assign(
                        targets=[var_to_store_subject],
                        value=node.subject,
                        lineno=None,
                    )
                )
                subject = var_to_store_subject
        # Collect all cases from the match statement.
        cases: list[tuple[ast.expr, list[ast.stmt]]] = []
        for case in node.cases:
            condition, body = CaseVisitor(subject).visit(case)
            cases.append((condition, body))

        # The following code in this function
        # will create a series of if-elif-else statements
        created_stmt: Union[ast.If, None, list[ast.stmt]] = None

        # If the last case was patterned "case _", then convert it to an "else" statement.
        match cases[-1][0]:
            case ast.Constant(True):
                created_stmt = cases[-1][1]
                cases.pop(-1)
            case _:
                pass
        for cond_expr, body_stmts in reversed(cases):
            match created_stmt:
                # Create `if`
                case None:
                    created_stmt = ast.If(cond_expr, body_stmts, [])
                # Create elif
                case ast.If():
                    created_stmt = ast.If(
                        cond_expr,
                        body_stmts,
                        [created_stmt],
                    )
                # Create else
                case list():
                    created_stmt = ast.If(
                        cond_expr,
                        body_stmts,
                        created_stmt,
                    )
                case _:
                    raise NotImplementedError
        assert created_stmt is not None
        assert not isinstance(created_stmt, list)
        return extra_stmts_before_if, created_stmt


class TransformerToLegacy(ast.NodeTransformer):
    """
    The transformer to transform `Python>=3.10` AST to Lower versions.
    """

    def visit_Match(self, node: ast.Match) -> list[ast.stmt]:
        return MainConverter().visit(node)


def convert_file(file_path: str, output_path: str, file_encoding="utf8"):
    """
    Convert a python source file to a python source file compatible with python 3.9 or lower.

    :file_path: The path of the python source file.
    :output_path: The path of the output file.
    """
    with open(file_path, "r", encoding=file_encoding) as f:
        src = f.read()
    tree = ast.parse(src)
    tree = TransformerToLegacy().visit(tree)
    with open(output_path, "w") as f:
        f.write(ast.unparse(tree))
    return tree
