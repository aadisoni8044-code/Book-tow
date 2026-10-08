"""
JPS Script AST Nodes
Abstract Syntax Tree representations for JPS Script construct nodes.
"""

class ASTNode:
    def __init__(self, line, column):
        self.line = line
        self.column = column

class ProgramNode(ASTNode):
    def __init__(self, statements, line=1, column=1):
        super().__init__(line, column)
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode({self.statements})"

class ImportNode(ASTNode):
    def __init__(self, module_name, line, column):
        super().__init__(line, column)
        self.module_name = module_name

    def __repr__(self):
        return f"ImportNode({repr(self.module_name)})"

class AssignNode(ASTNode):
    def __init__(self, target, expr, line, column):
        super().__init__(line, column)
        self.target = target
        self.expr = expr

    def __repr__(self):
        return f"AssignNode({self.target} = {self.expr})"

class CallNode(ASTNode):
    def __init__(self, callee, args, line, column):
        super().__init__(line, column)
        self.callee = callee
        self.args = args

    def __repr__(self):
        return f"CallNode({self.callee}, args={self.args})"

class IdentifierNode(ASTNode):
    def __init__(self, name, line, column):
        super().__init__(line, column)
        self.name = name

    def __repr__(self):
        return f"IdentifierNode({repr(self.name)})"

class LiteralNode(ASTNode):
    def __init__(self, value, line, column):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f"LiteralNode({repr(self.value)})"
