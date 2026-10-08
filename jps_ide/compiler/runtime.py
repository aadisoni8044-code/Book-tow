"""
JPS Script Runtime Engine
Executes AST nodes and manages environment state.
"""

from jps_ide.compiler.ast import ProgramNode, ImportNode, AssignNode, CallNode, IdentifierNode, LiteralNode
from jps_ide.compiler.errors import JPSNameError, JPSRuntimeError, JPSTypeError, JPSImportError
from jps_ide.runtime.box_runtime import BoxRuntimeManager
from jps_ide.runtime.game_runtime import GameRuntimeManager
from jps_ide.runtime.functions import jps_print

class Interpreter:
    def __init__(self, output_callback=print):
        self.output_callback = output_callback
        self.variables = {}
        self.imported_modules = set()
        self.box_manager = BoxRuntimeManager()
        self.game_manager = GameRuntimeManager()

    def reset(self):
        self.variables.clear()
        self.imported_modules.clear()
        self.box_manager.reset()
        self.game_manager.reset()

    def execute(self, ast):
        if not isinstance(ast, ProgramNode):
            raise JPSRuntimeError("Invalid AST program root")

        last_val = None
        for stmt in ast.statements:
            last_val = self.visit(stmt)
        return last_val

    def visit(self, node):
        if isinstance(node, ImportNode):
            return self.visit_import(node)
        elif isinstance(node, AssignNode):
            return self.visit_assign(node)
        elif isinstance(node, CallNode):
            return self.visit_call(node)
        elif isinstance(node, IdentifierNode):
            return self.visit_identifier(node)
        elif isinstance(node, LiteralNode):
            return node.value
        else:
            raise JPSRuntimeError(f"Unknown AST node {type(node).__name__}", line=getattr(node, 'line', None))

    def visit_import(self, node):
        mod_name = node.module_name
        self.imported_modules.add(mod_name)

        if mod_name == "box":
            msg = "[Module 'box' imported]"
        elif mod_name == "game":
            msg = self.game_manager.import_game()
        else:
            raise JPSImportError(f"Unknown library '{mod_name}'", line=node.line, column=node.column)
        return msg

    def visit_assign(self, node):
        val = self.visit(node.expr)
        self.variables[node.target] = val
        return val

    def visit_call(self, node):
        callee = node.callee
        evaluated_args = [self.visit(arg) for arg in node.args]

        if callee == "print":
            return jps_print(evaluated_args, output_callback=self.output_callback)

        # Box functions
        if callee == "body_2D.box":
            if "box" not in self.imported_modules:
                raise JPSImportError("Module 'box' is not imported. Call 'import.box' first.", line=node.line)
            return self.box_manager.body_2D_box()

        elif callee == "size.box":
            if "box" not in self.imported_modules:
                raise JPSImportError("Module 'box' is not imported. Call 'import.box' first.", line=node.line)
            if len(evaluated_args) != 2:
                raise JPSTypeError(f"size.box expects 2 arguments (width, height), got {len(evaluated_args)}", line=node.line)
            return self.box_manager.size_box(evaluated_args[0], evaluated_args[1])

        elif callee == "run.box":
            if "box" not in self.imported_modules:
                raise JPSImportError("Module 'box' is not imported. Call 'import.box' first.", line=node.line)
            return self.box_manager.run_box()

        elif callee == "switch.box":
            if "box" not in self.imported_modules:
                raise JPSImportError("Module 'box' is not imported. Call 'import.box' first.", line=node.line)
            return self.box_manager.switch_box()

        # Game functions
        elif callee == "size.game":
            if "game" not in self.imported_modules:
                raise JPSImportError("Module 'game' is not imported. Call 'import.game' first.", line=node.line)
            if len(evaluated_args) != 2:
                raise JPSTypeError(f"size.game expects 2 arguments (width, height), got {len(evaluated_args)}", line=node.line)
            return self.game_manager.size_game(evaluated_args[0], evaluated_args[1])

        elif callee == "run.game":
            if "game" not in self.imported_modules:
                raise JPSImportError("Module 'game' is not imported. Call 'import.game' first.", line=node.line)
            return self.game_manager.run_game()

        raise JPSNameError(f"Unknown function or method '{callee}'", line=node.line)

    def visit_identifier(self, node):
        if node.name in self.variables:
            return self.variables[node.name]
        raise JPSNameError(f"Variable '{node.name}' is not defined", line=node.line)
