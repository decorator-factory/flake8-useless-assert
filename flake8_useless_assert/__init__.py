import ast
from typing import Callable, Iterator, List, NamedTuple, Optional, Union


class FlakeDiagnostic(NamedTuple):
    line: int
    col: int
    message: str

    unused: None = None
    # Why does this tuple need 4 elements? I have no idea.


def _is_call_to_format(call: ast.Call) -> bool:
    """
    Check if a call is a call to `str.format`, like '{0}'.format(1).
    """
    if not isinstance(call.func, ast.Attribute):
        return False

    if not isinstance(call.func.value, (ast.Constant, ast.Str)):
        return False

    return call.func.attr == "format"


ConstT = Union[ast.Constant, ast.Str, ast.Num, ast.Str, ast.Bytes, ast.NameConstant, ast.Ellipsis]


def _extract_value_from_const_expr(const: ConstT) -> object:
    """
    Extract constant value from a constant node
    """
    if isinstance(const, ast.Constant):
        return const.value
    elif isinstance(const, ast.Str):
        return const.s
    elif isinstance(const, ast.Num):
        return const.n
    elif isinstance(const, ast.NameConstant):
        return const.value
    elif isinstance(const, ast.Ellipsis):
        return ...
    else:
        assert False


def _detect_invalid_assert_test(test: ast.expr) -> Optional[str]:
    # Returns a reason if the expresion is an invalid test for an assert,
    # or `None` if it's valid

    if isinstance(test, (ast.Constant, ast.Str, ast.Num, ast.Str, ast.Bytes,
                         ast.NameConstant, ast.Ellipsis)):
        const = _extract_value_from_const_expr(test)
        if const is False:
            return None  # `assert False` is a valid idiom

        if const:
            return "`assert` with a truthy value has no effect"
        else:
            return "`assert` with a falsey value always fails. If you want this, do `assert False`"
    elif isinstance(test, ast.JoinedStr):
        return "`assert` with an f-string has no effect"
    elif isinstance(test, ast.Call):
        if not _is_call_to_format(test):
            return
        return "`assert` with 'string'.format(...) has no effect"
    else:
        return None


class UselessAssertVisitor(ast.NodeVisitor):
    def __init__(self, callback: Callable[[FlakeDiagnostic], None]):
        self._callback = callback

    def visit_Assert(self, node: ast.Assert) -> None:
        message = _detect_invalid_assert_test(node.test)

        if message is None:
            return

        diagnostic = FlakeDiagnostic(
            line=node.lineno,
            col=node.col_offset,
            message="ULA001 {0}".format(message),
        )
        self._callback(diagnostic)


class UselessAssert:
    name = "flake8-useless-assert"
    version = "0.1.1"

    def __init__(self, tree: ast.Module) -> None:
        self._tree = tree

    def __iter__(self) -> Iterator[FlakeDiagnostic]:
        diagnostics: List[FlakeDiagnostic] = []
        UselessAssertVisitor(diagnostics.append).visit(self._tree)

        yield from diagnostics
