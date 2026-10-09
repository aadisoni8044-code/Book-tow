from typing import List, Any, Optional

class ASTNode:
    """Base AST Node."""
    def __init__(self, line: int = 1):
        self.line = line


class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode], line: int = 1):
        super().__init__(line)
        self.statements = statements


class ImportNode(ASTNode):
    def __init__(self, module_name: str, line: int = 1):
        super().__init__(line)
        self.module_name = module_name  # e.g., "box", "game"


class AssignNode(ASTNode):
    def __init__(self, var_name: str, value: ASTNode, line: int = 1):
        super().__init__(line)
        self.var_name = var_name
        self.value = value


class CallNode(ASTNode):
    def __init__(self, func_name: str, args: List[ASTNode], line: int = 1):
        super().__init__(line)
        self.func_name = func_name  # e.g. "body_2D.box", "size.box", "run.box", "print", "size.game", "run.game"
        self.args = args


class MemberAccessNode(ASTNode):
    def __init__(self, target: str, member: str, line: int = 1):
        super().__init__(line)
        self.target = target  # e.g. "run"
        self.member = member  # e.g. "box"
        self.full_name = f"{target}.{member}"


class LiteralNode(ASTNode):
    def __init__(self, value: Any, line: int = 1):
        super().__init__(line)
        self.value = value


class VariableNode(ASTNode):
    def __init__(self, name: str, line: int = 1):
        super().__init__(line)
        self.name = name


class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int = 1):
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right
