import ast
from typing import Iterator, List

from .flake_diagnostic import FlakeDiagnostic
from .visitors import AssertWithConstantVisitor, AssertWithFormattedStrVisitor

from .patch_const import LegacyConstantRewriter


class UselessAssert:
    name = "flake8-useless-assert"
    version = "0.2.0"

    def __init__(self, tree: ast.Module) -> None:
        self._tree = tree

    def __iter__(self) -> Iterator[FlakeDiagnostic]:
        LegacyConstantRewriter().visit(self._tree)

        diagnostics: List[FlakeDiagnostic] = []
        AssertWithConstantVisitor(diagnostics.append).visit(self._tree)
        AssertWithFormattedStrVisitor(diagnostics.append).visit(self._tree)

        yield from diagnostics
