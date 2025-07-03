import argparse
import sys
from collections import defaultdict

class UserInterrupt(Exception):
    def __init__(self, result):
        self.result = result
        super().__init__("Execution interrupted by user.")

def build_loop_map(code):
    loop_map = {}
    stack = []

    for i, char in enumerate(code):
        if char == "[":
            stack.append(i)
        elif char == "]":
            if not stack:
                raise SyntaxError(f"Unmatched closing bracket at position {i}")
            start = stack.pop()
            loop_map[start] = i
            loop_map[i] = start

    if stack:
        raise SyntaxError(f"Unmatched opening bracket(s) at position(s): {stack}")

    return loop_map

def interpret(code, debug=False, tape_size=None, tape_wrap=False):
    tape = defaultdict(int) if tape_size is None else [0] * tape_size
    pointer = 0
    loop_map = build_loop_map(code)
    result = []

    def add(): tape[pointer] = (tape[pointer] + 1) % 256
    def sub(): tape[pointer] = (tape[pointer] - 1) % 256
    def inc():
        nonlocal pointer
        pointer += 1
        if tape_size is not None:
            if pointer >= tape_size:
                if tape_wrap:
                    pointer = 0
                else:
                    raise MemoryError(f"Pointer out of bounds: {pointer} >= {tape_size}")
    def dec(): 
        nonlocal pointer
        pointer -= 1
        if tape_size is not None:
            if pointer < 0:
                if tape_wrap:
                    pointer = tape_size-1
                else:
                    raise MemoryError(f"Pointer out of bounds: {pointer} < 0")
    def output():
        char = chr(tape[pointer])
        result.append(char)
        if not debug:
            print(char, end='', flush=True)
    def input_char():
        try:
            user_input = input("Input one character: ")
            tape[pointer] = ord(user_input[0]) if user_input else 0
        except EOFError:
            tape[pointer] = 0

    dispatch = {
        '+': add,
        '-': sub,
        '>': inc,
        '<': dec,
        '.': output,
        ',': input_char
    }

    i = 0

    try:
        while i < len(code):

            cmd = code[i]

            if cmd in dispatch:
                dispatch[cmd]()
            elif cmd == '[' and tape[pointer] == 0:
                i = loop_map[i]
            elif cmd == ']' and tape[pointer] != 0:
                i = loop_map[i]

            i += 1

            if debug:
                print(f"[{i:04d}] {code[i]} | Ptr: {pointer:03d} | Val: {tape[pointer]:03d} | Output: {''.join(result)}")

    except KeyboardInterrupt:
        raise UserInterrupt(result)

    return ''.join(result)

def main():
    parser = argparse.ArgumentParser(description="A Brainfuck interpreter in Python.")
    
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("filename", nargs='?', default=None, help="The .bf or .b file to execute.")
    source_group.add_argument("-c", "--code", help="Execute Brainfuck code directly from the command line.")

    parser.add_argument("--debug", action="store_true", help="Enable debug mode to see execution step-by-step.")
    parser.add_argument("--tape-size", type=int, default=None, help="Specify a fixed tape size (e.g., 30000). Default is infinite.")
    parser.add_argument("--tape-wrap", action="store_true", help="Enable tape wrapping for fixed-size tapes. Requires --tape-size.")

    args = parser.parse_args()

    if args.tape_wrap and args.tape_size is None:
        parser.error("--tape-wrap requires --tape-size to be set.")

    if args.code:
        raw_code = args.code
    else:
        try:
            with open(args.filename, "r") as f:
                raw_code = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at '{args.filename}'", file=sys.stderr)
            sys.exit(1)
        except TypeError:
             print("Error: No input file specified.", file=sys.stderr)
             parser.print_help(sys.stderr)
             sys.exit(1)

    valid_chars = set("+-<>[],.")
    code = ''.join(c for c in raw_code if c in valid_chars)

    try:
        final_output = interpret(code, debug=args.debug, tape_size=args.tape_size, tape_wrap=args.tape_wrap)
        if args.debug:
            print(f"\n--- Final Output---\n\n{final_output}", end="")

    except UserInterrupt as e:
        partial_output = ''.join(e.result)
        print(partial_output, end="")
        print("\n\n[Partial Output] Execution interrupted by user (Ctrl+C).", file=sys.stderr)

    except (SyntaxError, KeyError, MemoryError) as e:
        print(f"\n[Error] {e}", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n[No output generated] Execution interrupted very early.", file=sys.stderr)


if __name__ == "__main__":
    main()