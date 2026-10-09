import io
import pytest
from jps.lexer.lexer import Lexer
from jps.parser.parser import Parser
from jps.runtime.interpreter import Interpreter


def test_print_output():
    code = 'print("hello", 123)'
    out = io.StringIO()
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter(output_stream=out)
    interpreter.interpret(ast)

    assert "hello 123" in out.getvalue()


def test_import_box_and_body_2d_static():
    code = "import.box\na = body_2D.box()\nb = size.box(500,500)"
    out = io.StringIO()
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter(output_stream=out)
    interpreter.interpret(ast)

    assert interpreter.env.box_module_imported is True
    assert len(interpreter.env.boxes) == 1
    box = interpreter.env.boxes[0]
    assert box.width == 500
    assert box.height == 500
    assert box.is_running is False  # Static box without run.box()


def test_moving_box_run_box():
    code = "import.box\na = body_2D.box()\nb = size.box(500,500)\nc = run.box()"
    out = io.StringIO()
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter(output_stream=out)
    interpreter.interpret(ast)

    assert len(interpreter.env.boxes) == 1
    box = interpreter.env.boxes[0]
    assert box.is_running is True  # Moving box using run.box()


def test_switch_box_drag_and_drop():
    code = "import.box\na = body_2D.box()\nd = switch.box()"
    out = io.StringIO()
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter(output_stream=out)
    interpreter.interpret(ast)

    assert len(interpreter.env.boxes) == 1
    box = interpreter.env.boxes[0]
    assert box.is_switch is True  # Drag and drop switch enabled


def test_game_import_size_game_run_game():
    code = "import.game\nimport.box\na = size.game(1000,1000)\nb = run.game()\nc = run.box()\nd = switch.box()"
    out = io.StringIO()
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter(output_stream=out)
    interpreter.interpret(ast)

    assert interpreter.env.game_module_imported is True
    assert interpreter.env.game_size == (1000, 1000)
    assert interpreter.env.game_running is True
