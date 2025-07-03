import sys
from collections import defaultdict

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

    i = 0
    while i < len(code):
        cmd = code[i]
        
        if cmd in dispatch:
            dispatch[cmd]()
        elif cmd == '[' and tape[pointer] == 0:
            i = loop_map[i]
        elif cmd == ']' and tape[pointer] != 0:
            i = loop_map[i]

        if debug:
            print(f"[{i}] {code[i]} | Ptr: {pointer} | Val: {tape[pointer]}")

        i += 1
    
    return ''.join(result)

def main():
    args = sys.argv[1:]
    if not args or (args[0].startswith("--") and len(args) == 1):
        print("Usage: python brainpy.py program.bf [--debug]")
        sys.exit(1)

    debug = "--debug" in args
    filename = [arg for arg in args if arg.endswith(".bf") or arg.endswith(".b")]
    
    if not filename:
        print("Error: Missing .bf file.")
        sys.exit(1)

    with open(filename[0], "r") as f:
        raw_code = f.read()

    valid_chars = set("+-<>[],.")
    code = ''.join(c for c in raw_code if c in valid_chars)

    output = interpret(code, debug=debug)
    print(output, end="")

if __name__ == "__main__":
    main()