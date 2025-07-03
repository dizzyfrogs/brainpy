# BrainPy

 A Simple Brainfuck Interpreter in Python

## Features

- Fully supports Brainfuck's 8 commands: `+ - > < [ ] , .`
- Infinite tape in both directions
- Optional `--debug` for step-by-step execution tracing
- Ignores non-Brainfuck characters
- Detects unmatched brackets with helpful errors
- Supports `.bf` and `.b` file extensions

## Usage

1. Run a `.bf` file

```command
python brainpy.py hello.bf
```

2. Enable debug mode

```command
python brainpy.py program.bf --debug
```

This will print the current instruction, pointer location, and cell value after every step:
```yaml
[12] + | Ptr: 4 | Val: 255
[13] > | Ptr: 5 | Val: 0
```

## Example

A simple `hello.bf` file:
```brainfuck
>++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<+
+.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-
]<+.
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

- Input (`,`) is handled interactively. You'll be prompted to type a character when needed.
- Each cell wraps at 256 (`% 256`) to simulate 8-bit behavior