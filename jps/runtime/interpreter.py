import sys
from typing import TextIO, Any, Optional
from .environment import Environment, BoxObject
from ..ast.nodes import (
    ASTNode, ProgramNode, ImportNode, AssignNode, CallNode,
    MemberAccessNode, LiteralNode, VariableNode, BinaryOpNode
)
from ..errors.exceptions import (
    JPSRuntimeError, JPSNameError, JPSImportError, JPSSyntaxError
)


class Interpreter:
    """Interpreter executing JPS Script AST nodes."""

    def __init__(self, output_stream: TextIO = sys.stdout):
        self.env = Environment()
        self.output_stream = output_stream

    def interpret(self, program: ProgramNode):
        for stmt in program.statements:
            self._eval(stmt)

    def _eval(self, node: ASTNode) -> Any:
        if isinstance(node, ImportNode):
            return self._eval_import(node)
        elif isinstance(node, AssignNode):
            return self._eval_assign(node)
        elif isinstance(node, CallNode):
            return self._eval_call(node)
        elif isinstance(node, MemberAccessNode):
            return self._eval_member_access(node)
        elif isinstance(node, LiteralNode):
            return node.value
        elif isinstance(node, VariableNode):
            return self._eval_variable(node)
        elif isinstance(node, BinaryOpNode):
            return self._eval_binary_op(node)
        else:
            raise JPSRuntimeError(f"Unknown AST node type '{type(node).__name__}'", line=getattr(node, "line", 1))

    def _eval_import(self, node: ImportNode):
        if node.module_name == "box":
            self.env.box_module_imported = True
            return "<Module 'box'>"
        elif node.module_name == "game":
            self.env.game_module_imported = True
            return "<Module 'game'>"
        else:
            raise JPSImportError(f"Unknown module '{node.module_name}'", line=node.line)

    def _eval_assign(self, node: AssignNode):
        val = self._eval(node.value)
        self.env.set_var(node.var_name, val)
        return val

    def _eval_call(self, node: CallNode):
        func_name = node.func_name
        args = [self._eval(arg) for arg in node.args]

        if func_name == "print":
            str_args = [str(a) for a in args]
            out = " ".join(str_args)
            print(out, file=self.output_stream)
            self.output_stream.flush()
            return out

        elif func_name == "body_2D.box":
            if not self.env.box_module_imported:
                raise JPSRuntimeError("Module 'box' not imported. Call 'import.box' first.", line=node.line)
            box = self.env.create_box()
            return box

        elif func_name == "size.box":
            if not self.env.box_module_imported:
                raise JPSRuntimeError("Module 'box' not imported. Call 'import.box' first.", line=node.line)
            if len(args) == 2:
                w, h = int(args[0]), int(args[1])
                self.env.set_last_box_size(w, h)
                return f"<SizeBox w={w}, h={h}>"
            elif len(args) == 0:
                return f"<SizeBox w=500, h=500>"
            else:
                raise JPSRuntimeError(f"'size.box()' expects 2 arguments (width, height), got {len(args)}", line=node.line)

        elif func_name == "run.box":
            if not self.env.box_module_imported:
                raise JPSRuntimeError("Module 'box' not imported. Call 'import.box' first.", line=node.line)
            self.env.enable_box_run()
            return "<RunBox state=Active>"

        elif func_name == "switch.box":
            if not self.env.box_module_imported:
                raise JPSRuntimeError("Module 'box' not imported. Call 'import.box' first.", line=node.line)
            self.env.enable_box_switch()
            return "<SwitchBox state=Enabled>"

        elif func_name == "size.game":
            if not self.env.game_module_imported:
                raise JPSRuntimeError("Module 'game' not imported. Call 'import.game' first.", line=node.line)
            if len(args) == 2:
                w, h = int(args[0]), int(args[1])
                self.env.game_size = (w, h)
                return f"<GameSize w={w}, h={h}>"
            else:
                raise JPSRuntimeError(f"'size.game()' expects 2 arguments (width, height), got {len(args)}", line=node.line)

        elif func_name == "run.game":
            if not self.env.game_module_imported:
                raise JPSRuntimeError("Module 'game' not imported. Call 'import.game' first.", line=node.line)
            self.env.game_running = True
            return "<GameRuntime state=Running>"

        else:
            raise JPSRuntimeError(f"Unknown function '{func_name}()'", line=node.line)

    def _eval_member_access(self, node: MemberAccessNode):
        full_name = node.full_name
        if full_name == "run.box":
            if not self.env.box_module_imported:
                raise JPSRuntimeError("Module 'box' not imported. Call 'import.box' first.", line=node.line)
            self.env.enable_box_run()
            return "<RunBox state=Active>"
        elif full_name == "switch.box":
            if not self.env.box_module_imported:
                raise JPSRuntimeError("Module 'box' not imported. Call 'import.box' first.", line=node.line)
            self.env.enable_box_switch()
            return "<SwitchBox state=Enabled>"
        elif full_name == "run.game":
            if not self.env.game_module_imported:
                raise JPSRuntimeError("Module 'game' not imported. Call 'import.game' first.", line=node.line)
            self.env.game_running = True
            return "<GameRuntime state=Running>"
        else:
            raise JPSRuntimeError(f"Unknown property/function '{full_name}'", line=node.line)

    def _eval_variable(self, node: VariableNode):
        if self.env.has_var(node.name):
            return self.env.get_var(node.name)
        raise JPSNameError(f"Name '{node.name}' is not defined", line=node.line)

    def _eval_binary_op(self, node: BinaryOpNode):
        left_val = self._eval(node.left)
        right_val = self._eval(node.right)

        if node.op == "+":
            return left_val + right_val
        elif node.op == "-":
            return left_val - right_val
        elif node.op == "*":
            return left_val * right_val
        elif node.op == "/":
            if right_val == 0:
                raise JPSRuntimeError("Division by zero", line=node.line)
            return left_val / right_val
        else:
            raise JPSRuntimeError(f"Unknown operator '{node.op}'", line=node.line)
