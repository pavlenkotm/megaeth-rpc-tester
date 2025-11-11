#!/usr/bin/env python3
"""
Brainfuck Interpreter for Web3 Examples

A simple interpreter to run Brainfuck programs demonstrating
blockchain and Web3 concepts through esoteric programming.
"""

import sys
from typing import List


class BrainfuckInterpreter:
    """Brainfuck interpreter with 30,000 memory cells."""

    def __init__(self, memory_size: int = 30000):
        """Initialize the interpreter."""
        self.memory: List[int] = [0] * memory_size
        self.pointer: int = 0
        self.output: List[str] = []

    def execute(self, code: str, input_data: str = "") -> str:
        """Execute Brainfuck code and return output."""
        # Remove non-command characters (comments)
        code = ''.join(c for c in code if c in '><+-.,[]')

        code_pointer = 0
        input_pointer = 0
        loop_stack = []

        while code_pointer < len(code):
            command = code[code_pointer]

            if command == '>':
                # Move pointer right
                self.pointer = (self.pointer + 1) % len(self.memory)

            elif command == '<':
                # Move pointer left
                self.pointer = (self.pointer - 1) % len(self.memory)

            elif command == '+':
                # Increment current cell
                self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256

            elif command == '-':
                # Decrement current cell
                self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256

            elif command == '.':
                # Output current cell as ASCII
                self.output.append(chr(self.memory[self.pointer]))

            elif command == ',':
                # Input to current cell
                if input_pointer < len(input_data):
                    self.memory[self.pointer] = ord(input_data[input_pointer])
                    input_pointer += 1
                else:
                    self.memory[self.pointer] = 0

            elif command == '[':
                # Jump forward if current cell is 0
                if self.memory[self.pointer] == 0:
                    bracket_count = 1
                    while bracket_count > 0:
                        code_pointer += 1
                        if code[code_pointer] == '[':
                            bracket_count += 1
                        elif code[code_pointer] == ']':
                            bracket_count -= 1
                else:
                    loop_stack.append(code_pointer)

            elif command == ']':
                # Jump backward if current cell is non-zero
                if self.memory[self.pointer] != 0:
                    code_pointer = loop_stack[-1]
                else:
                    loop_stack.pop()

            code_pointer += 1

        return ''.join(self.output)


def main():
    """Main entry point for the interpreter."""
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <brainfuck_file.bf>")
        print("\nExample:")
        print("  python interpreter.py hello_web3.bf")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            code = f.read()

        print(f"🧠 Brainfuck Interpreter - Web3 Edition")
        print(f"📄 Running: {filename}\n")
        print("=" * 50)

        interpreter = BrainfuckInterpreter()
        output = interpreter.execute(code)

        print(output)
        print("=" * 50)
        print(f"\n✅ Execution completed successfully")
        print(f"📊 Output length: {len(output)} characters")

    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
