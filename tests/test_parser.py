import pytest
from jps.lexer.lexer import Lexer
from jps.parser.parser import Parser
from jps.ast.nodes import ImportNode, AssignNode, CallNode


def test_parser_import_and_calls():
    code = "import.box\na = body_2D.box()\nb = size.box(500,500)"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    assert len(ast.statements) == 3
    assert isinstance(ast.statements[0], ImportNode)
    assert ast.statements[0].module_name == "box"

    assert isinstance(ast.statements[1], AssignNode)
    assert ast.statements[1].var_name == "a"
    assert isinstance(ast.statements[1].value, CallNode)
    assert ast.statements[1].value.func_name == "body_2D.box"

    assert isinstance(ast.statements[2], AssignNode)
    assert ast.statements[2].value.func_name == "size.box"
    assert len(ast.statements[2].value.args) == 2
