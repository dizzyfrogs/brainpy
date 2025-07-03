def interpret(code):
    tape_size = 1000
    tape = [0] * tape_size
    pointer = 0
    result = []

    i = 0
    while i < len(code):
        if code[i] == "+":
            tape[pointer] = (tape[pointer] + 1) % 256
        elif code[i] == "-":
            tape[pointer] = (tape[pointer] - 1) % 256
        elif code[i] == ">":
            pointer = min(tape_size-1, pointer + 1)
        elif code[i] == "<":
            pointer = max(0, pointer - 1)
        elif code[i] == ".":
            result.append(chr(tape[pointer]))
        elif code[i] == ",":
            tape[pointer] = ord(input()[0])
        elif code[i] == "[":
            if tape[pointer] == 0:
                count = 1
                while count > 0:
                    i += 1
                    if code[i] == "[":
                        count += 1
                    elif code[i] == "]":
                        count -= 1
        elif code[i] == "]":
            if tape[pointer] != 0:
                count = 1
                while count > 0:
                    i -= 1
                    if code[i] == "]":
                        count += 1
                    elif code[i] == "[":
                        count -= 1
        else:
            pass
        i += 1
    
    return ''.join(result)