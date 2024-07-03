from inspect import ismethod
import os
from astroid import nodes
from typing import TYPE_CHECKING

from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class HexagonalChecker(BaseChecker):

    name = "hexagonal-checker"
    msgs = {
        "E6601": (
            "Core module must not import from an adapter module",
            "core-imports-adapters",
            "Used when a core module imports from an adapter module",
        ),
        "E6602": (
            "Adapter module must not import from another adapter module",
            "adapter-imports-adapters",
            "Used when an adapter module imports from another adapter module",
        ),
        "W6603": (
            "Adapter module should not import from the core module except for ports",
            "adapter-imports-core",
            "Used when an adapter module imports from the core module other than ports",
        ),
        "R6604": (
            "Ports modules should not include any logic",
            "port-includes-logic",
            "Used when a ports module includes any logic",
        ),
    }

    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        this_module = node.root().name.split(".")
        if node.level and node.level > 0:
            # get module path of ancestors
            relative_module = node.modname.split(".") if node.modname else []
            that_module = this_module[: -node.level] + relative_module
        else:
            that_module = node.modname.split(".") if node.modname else []
        self._check_import(this_module, that_module, node)

    def visit_import(self, node: nodes.Import) -> None:
        this_module = node.root().name.split(".")
        for name, _ in node.names:
            that_module = name.split(".")
            self._check_import(this_module, that_module, node)

    def _check_import(
        self, this_module: list[str], that_module: list[str], node: nodes.NodeNG
    ) -> None:
        if "core" in this_module and "adapters" in that_module:
            self.add_message("core-imports-adapters", node=node)

        if "adapters" in this_module and "adapters" in that_module:
            # get the adapter names (first part after "adapters")
            try:
                this_adapter = this_module[this_module.index("adapters") + 1]
            except ValueError:
                this_adapter = None
            try:
                that_adapter = that_module[that_module.index("adapters") + 1]
            except ValueError:
                that_adapter = None
            if this_adapter and that_adapter and this_adapter != that_adapter:
                self.add_message("adapter-imports-adapters", node=node)

        if (
            "adapters" in this_module
            and "core" in that_module
            and "ports" not in that_module
        ):
            self.add_message("adapter-imports-core", node=node)

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        if "ports" in node.root().name.split("."):
            if any(not isinstance(child, nodes.Pass) for child in node.body):
                self.add_message("port-includes-logic", node=node)


def register(linter: "PyLinter") -> None:
    linter.register_checker(HexagonalChecker(linter))
