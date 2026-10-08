"""
Integration tests executing uploaded sample JPS files
"""

import os
import pytest
from jps_ide.compiler.lexer import Lexer
from jps_ide.compiler.parser import Parser
from jps_ide.compiler.runtime import Interpreter

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "jps_ide", "examples")

def run_sample_file(filename):
    filepath = os.path.join(EXAMPLES_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    output = []
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interp = Interpreter(output_callback=output.append)
    interp.execute(ast)
    return output

def test_example_boxrun():
    out = run_sample_file("boxrun.jps")
    assert len(out) == 1
    assert "[JPS Box #1 Created]" in out[0]

def test_example_fighter():
    out = run_sample_file("fighter.jps")
    assert len(out) == 1
    assert "[JPS Box #1 Size set to 500x500]" in out[0]

def test_example_game():
    out = run_sample_file("game.jap")
    assert len(out) == 1
    assert "Interactive Drag-and-Drop Enabled" in out[0]

def test_example_hello():
    out = run_sample_file("hello.jps")
    assert len(out) == 1
    assert out[0] == "hello"
