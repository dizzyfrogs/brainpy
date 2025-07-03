import sys
from collections import defaultdict

class UserInterrupt(Exception):
    def __init__(self, result):
        self.result = result

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

def interpret(code, debug=False):
    tape = defaultdict(int)
    pointer = 0
    loop_map = build_loop_map(code)
    result = []

    def add(): tape[pointer] = (tape[pointer] + 1) % 256
    def sub(): tape[pointer] = (tape[pointer] - 1) % 256
    def inc(): nonlocal pointer; pointer += 1
    def dec(): nonlocal pointer; pointer -= 1
    def output(): result.append(chr(tape[pointer]))
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

    STEP_WARNING_THRESHOLD = 10_000_000
    warned = False
    step_count = 0
    i = 0

    try:
        while i < len(code):
            step_count += 1
            if step_count >= STEP_WARNING_THRESHOLD and not warned:
                print(
                    f"\nWarning: Program has executed over {STEP_WARNING_THRESHOLD:,} steps. "
                    "Press Ctrl+C to terminate and see partial output.",
                    file=sys.stderr
                )
                warned = True

            cmd = code[i]

            if cmd in dispatch:
                dispatch[cmd]()
            elif cmd == '[' and tape[pointer] == 0:
                i = loop_map[i]
            elif cmd == ']' and tape[pointer] != 0:
                i = loop_map[i]

            if debug:
                print(f"[{i:04d}] {code[i]} | Ptr: {pointer:03d} | Val: {tape[pointer]:03d} | Output: {''.join(result)}")

            i += 1
            
    except KeyboardInterrupt:
        raise UserInterrupt(result)

    return ''.join(result)

def main():
    args = sys.argv[1:]
    if not args or (args[0].startswith("--") and len(args) == 1):
        print(f"Usage: python {sys.argv[0]} program.bf [--debug]")
        sys.exit(1)

    debug = "--debug" in args
    try:
        filename = next(arg for arg in args if arg.endswith((".bf", ".b")))
    except StopIteration:
        print("Error: Missing .bf or .b file.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(filename, "r") as f:
            raw_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'", file=sys.stderr)
        sys.exit(1)

    valid_chars = set("+-<>[],.")
    code = ''.join(c for c in raw_code if c in valid_chars)

    try:
        final_output = interpret(code, debug=debug)
        print(final_output, end="")

    except UserInterrupt as e:
        partial_output = ''.join(e.result)
        print(partial_output, end="")
        print("\n\n[Partial Output] Execution interrupted by user (Ctrl+C).", file=sys.stderr)

    except (SyntaxError, KeyError) as e:
        print(f"\n[Error] {e}", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n[No output generated] Execution interrupted very early.", file=sys.stderr)


if __name__ == "__main__":
    main()