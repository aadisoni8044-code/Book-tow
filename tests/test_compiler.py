"""
Unit tests for JPS Script Compiler & Runtime
"""

import pytest
from jps_ide.compiler.lexer import Lexer, TokenType
from jps_ide.compiler.parser import Parser
from jps_ide.compiler.errors import JPSSyntaxError, JPSNameError, JPSImportError
from jps_ide.compiler.runtime import Interpreter

def test_lexer_basic():
    code = "import.box\na = body_2D.box()\nprint(a)"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    kw_tokens = [t.value for t in tokens if t.type == TokenType.KEYWORD]
    assert "import.box" in kw_tokens
    assert "body_2D.box" in kw_tokens
    assert "print" in kw_tokens

def test_interpreter_boxrun():
    code = """
import.box
a = body_2D.box()
b = size.box(500,500)
c = run.box()
print(a,b)
"""
    output = []
    def capture(msg):
        output.append(msg)

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interp = Interpreter(output_callback=capture)
    interp.execute(ast)

    assert len(output) == 1
    assert "[JPS Box #1 Created]" in output[0]
    assert "[JPS Box #1 Size set to 500x500]" in output[0]

def test_interpreter_game():
    code = """
import.game
import.box
a = size.game(1000,1000)
b = run.game()
c = run.box()
d = switch.box()
print(a,b,c,d)
"""
    output = []
    lexer = Lexer(code)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    interp = Interpreter(output_callback=output.append)
    interp.execute(ast)

    assert len(output) == 1
    assert "1000x1000" in output[0]
    assert "Interactive Drag-and-Drop" in output[0]

def test_unimported_module_error():
    code = "a = body_2D.box()"
    lexer = Lexer(code)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    interp = Interpreter()
    with pytest.raises(JPSImportError) as exc_info:
        interp.execute(ast)
    assert "Module 'box' is not imported" in str(exc_info.value)
