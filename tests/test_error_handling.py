import pytest
from jps.lexer.lexer import Lexer
from jps.parser.parser import Parser
from jps.runtime.interpreter import Interpreter
from jps.errors.exceptions import JPSSyntaxError, JPSRuntimeError, JPSNameError, JPSImportError


def test_invalid_syntax_error():
    code = 'a = "unterminated string'
    with pytest.raises(JPSSyntaxError) as exc_info:
        lexer = Lexer(code)
        lexer.tokenize()
    assert "Unterminated string" in str(exc_info.value)
    assert "Line 1" in str(exc_info.value)


def test_unknown_function_error():
    code = "import.box\n abc.box()"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    with pytest.raises(JPSRuntimeError) as exc_info:
        interpreter.interpret(ast)
    assert "Unknown function 'abc.box()'" in str(exc_info.value)
    assert "Line 2" in str(exc_info.value)


def test_unimported_module_error():
    code = "a = body_2D.box()"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    with pytest.raises(JPSRuntimeError) as exc_info:
        interpreter.interpret(ast)
    assert "Module 'box' not imported" in str(exc_info.value)


def test_undefined_variable_error():
    code = "print(unknown_var)"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    with pytest.raises(JPSNameError) as exc_info:
        interpreter.interpret(ast)
    assert "Name 'unknown_var' is not defined" in str(exc_info.value)
