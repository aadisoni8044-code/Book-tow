import sys
import os
import argparse
from typing import TextIO

from .lexer.lexer import Lexer
from .parser.parser import Parser
from .runtime.interpreter import Interpreter
from .errors.exceptions import JPSError


def run_jps_code(source_code: str, output_stream: TextIO = sys.stdout, launch_gui_game: bool = True):
    """Executes JPS Script source code."""
    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter(output_stream=output_stream)
        interpreter.interpret(ast)

        # Launch Pygame 2D game runtime if game/box features were invoked and game execution is requested
        if launch_gui_game and (interpreter.env.game_running or len(interpreter.env.boxes) > 0):
            try:
                from .game.pygame_runtime import PygameRuntime
                runtime = PygameRuntime(interpreter.env, output_stream=output_stream)
                runtime.run()
            except Exception as e:
                print(f"[JPS Runtime] Warning: 2D Pygame engine notice: {e}", file=output_stream)

    except JPSError as jps_err:
        print(jps_err.formatted_message(), file=output_stream)
        output_stream.flush()
        sys.exit(1)
    except Exception as ex:
        print(f"JPS Error:\nLine 1: Runtime exception: {ex}", file=output_stream)
        output_stream.flush()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="JPS Script Engine Runner")
    parser.add_argument("filename", nargs="?", help="Path to JPS Script file (.jps / .jap)")
    parser.add_argument("-c", "--code", help="JPS Script inline code string")
    parser.add_argument("--no-gui", action="store_true", help="Disable Pygame GUI window (for tests/headless mode)")

    args = parser.parse_args()

    if args.code:
        run_jps_code(args.code, launch_gui_game=not args.no_gui)
    elif args.filename:
        if not os.path.exists(args.filename):
            print(f"JPS Error:\nLine 1: File not found: {args.filename}")
            sys.exit(1)
        with open(args.filename, "r", encoding="utf-8") as f:
            code = f.read()
        run_jps_code(code, launch_gui_game=not args.no_gui)
    else:
        print("Usage: python3 -m jps.runner <file.jps> OR python3 -m jps.runner -c \"<code>\"")


if __name__ == "__main__":
    main()
