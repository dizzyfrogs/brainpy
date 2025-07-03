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

def interpret(code):
    tape = defaultdict(int)
    pointer = 0
    loop_map = build_loop_map(code)
    result = []

    i = 0
    while i < len(code):
        if code[i] == "+":
            tape[pointer] = (tape[pointer] + 1) % 256
        elif code[i] == "-":
            tape[pointer] = (tape[pointer] - 1) % 256
        elif code[i] == ">":
            pointer += 1
        elif code[i] == "<":
            pointer -= 1
        elif code[i] == ".":
            result.append(chr(tape[pointer]))
        elif code[i] == ",":
            try:
                user_input = input("Input one character: ")
                tape[pointer] = ord(user_input[0]) if user_input else 0
            except EOFError:
                tape[pointer] = 0
        elif code[i] == "[":
            if tape[pointer] == 0:
                i = loop_map[i]
        elif code[i] == "]":
            if tape[pointer] != 0:
                i = loop_map[i]
        i += 1
    
    return ''.join(result)

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".bf"):
        print("Usage: python brainpy.py program.bf")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        raw_code = f.read()

    # Strip invalid characters
    valid_chars = set("+-<>[],.")
    code = ''.join(c for c in raw_code if c in valid_chars)

    output = interpret(code)
    print(output)