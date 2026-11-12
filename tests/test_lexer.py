import pytest
from jps.lexer.lexer import Lexer
from jps.lexer.token import TokenType


def test_lexer_keywords_and_dotted_identifiers():
    code = "import.game\nimport.box\nbody_2D.box()\nsize.box(500,500)"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.IMPORT
    assert tokens[1].type == TokenType.DOT
    assert tokens[2].value == "game"

    assert any(t.value == "body_2D" for t in tokens)
    assert any(t.value == "box" for t in tokens)


def test_lexer_strings_numbers():
    code = 'a = 1000\nb = "hello world"'
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    number_tok = [t for t in tokens if t.type == TokenType.NUMBER][0]
    string_tok = [t for t in tokens if t.type == TokenType.STRING][0]

    assert number_tok.value == "1000"
    assert string_tok.value == "hello world"
