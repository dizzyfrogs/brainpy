# BrainPy

A robust Brainfuck interpreter in Python.

## What is Brainfuck?

Brainfuck is a famous esoteric programming language created in 1993 by Urban Müller. It is notable for its extreme minimalism and for being Turing-complete, meaning it can theoretically compute anything that a regular computer can.

The language operates on a simple model consisting of:
- An **array of memory cells** (the "tape"), which are initialized to zero.
- A **data pointer** that starts at the first cell of the tape and can move left or right.

There are only eight commands, each consisting of a single character, which makes it one of the simplest programming languages in existence.


| Command | Description                                                                                                           |
| ------- | --------------------------------------------------------------------------------------------------------------------- |
| `+`     | Increment the value of the cell at the pointer.                                                                       |
| `-`     | Decrement the value of the cell at the pointer.                                                                       |
| `>`     | Move the data pointer to the right by one cell.                                                                       |
| `<`     | Move the data pointer to the left by one cell.                                                                        |
| `[`     | If the value at the current cell is zero, jump the instruction pointer forward to the command after the matching `]`. |
| `]`     | If the value at the current cell is non-zero, jump the instruction pointer back to the command after matching `[`.    | 
| `.`     | Output the character represented by the ASCII value of the current cell.                                              |
| `,`     | Accept one byte of input and store its value in the current cell.                                                     |

## Features

- **Full BF Support**: Implements all 8 standard Brainfuck 8 commands: `+ - > < [ ] , .`.
- **Flexible Code Input**: Execute code from `.bf`/`.b` files or directly from the command line with the `-c` flag.
- **Versatile Memory Model**:
    - Defaults to an **infinite tape** in both directions.
    - Option to use a **fixed-size** tape with `--tape-size`.
    - Option to **wrap the pointer** on fixed-size tapes with `--tape-wrap`.
- **Robust Execution**:
    - **Interruptible**: Safely stop long-running programs with (Ctrl+C) and see the partial output.
    - **Pre-validated Loops**: Detects unmatched brackets before execution begins.
- **Powerful Debugging**: A `--debug` flag provides a step-by-step trace of the program's state.

## Usage

**1. Run a `.bf` file**

```command
python brainpy.py hello.bf
```

**2. Execute code directly from the command line**
```command
python brainpy.py -c "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
```

**3. Use a fixed-size tape with wrapping**

This configuration micmics many classic Brainfuck interpreters.
```command
python mandelbrot.bf --tape-size 30000 --tape-wrap
```

**4. Enable debug mode**

```command
python brainpy.py program.bf --debug
```

This will print the current instruction, pointer location, and cell value, and cumulative output after every step:
```yaml
[0012] + | Ptr: 004 | Val: 255 | Output: Hello
[0013] > | Ptr: 005 | Val: 000 | Output: Hello
```

## Example

A simple `hello.bf` file. The interpreter ignores all non-command characters, so the code can be formatted with line breaks for readability.
```brainfuck
>++++++++[<+++++++++>-]<.
>++++[<+++++++>-]<+.
+++++++..
+++.
>>++++++[<+++++++>-]<++.
------------.
>++++++[<+++++++++>-]<+.
<.
+++.
------.
--------.
>>>++++[<++++++++>-]<+.
```

Run it:
```command
python brainpy.py hello.bf
```

Output:
```
Hello World!
```

## Notes

- **Cell Behavior**: Each cell is an 8-bit integer and will wrap on overflow/underflow (e.g., `255 + 1 = 0`).
- **Input**: The input command (`,`) is handled interactively. You will be prompted in the console to type a character when the command is reached.
- **Comments & Formatting**: Any characters that are not `+-<>[].,` (including whitespace, newlines, and text) are ignored and can be used as comments.