def interpret(code):
    tape = [0] * 1000
    pointer = 0
    result = []

    i = 0
    while i < len(code):
        if code[i] == "+":
            tape[pointer] = tape[pointer] + 1 if tape[pointer] <= 255 else 0
        elif code[i] == "-":
            tape[pointer] = tape[pointer] - 1 if tape[pointer] >= 0 else 255
        elif code[i] == ">":
            pointer += 1
        elif code[i] == "<":
            pointer -= 1
        elif code[i] == ".":
            result += chr(tape[pointer])
        elif code[i] == ",":
            tape[pointer] = ord(input())
        else:
            pass
        i += 1
    
    return ''.join(result)