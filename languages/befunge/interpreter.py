#!/usr/bin/env python3
"""
Befunge-93 Interpreter for Web3 Examples

A 2D esoteric programming language interpreter demonstrating
stack-based operations similar to blockchain virtual machines.
"""

import sys
import time
from typing import List, Tuple, Optional


class BefungeInterpreter:
    """Befunge-93 interpreter with visualization support."""

    def __init__(self, width: int = 80, height: int = 25, visualize: bool = False, debug: bool = False):
        """Initialize the Befunge interpreter."""
        self.width = width
        self.height = height
        self.grid: List[List[str]] = [[' ' for _ in range(width)] for _ in range(height)]
        self.stack: List[int] = []
        self.pc_x: int = 0  # Program counter X
        self.pc_y: int = 0  # Program counter Y
        self.direction: Tuple[int, int] = (1, 0)  # Moving right initially
        self.string_mode: bool = False
        self.output: List[str] = []
        self.visualize = visualize
        self.debug = debug
        self.steps = 0

    def load_program(self, program: str):
        """Load a Befunge program into the grid."""
        lines = program.split('\n')
        for y, line in enumerate(lines):
            if y >= self.height:
                break
            for x, char in enumerate(line):
                if x >= self.width:
                    break
                self.grid[y][x] = char

    def get_current_cell(self) -> str:
        """Get the character at the current position."""
        return self.grid[self.pc_y][self.pc_x]

    def move(self):
        """Move the program counter in the current direction."""
        self.pc_x = (self.pc_x + self.direction[0]) % self.width
        self.pc_y = (self.pc_y + self.direction[1]) % self.height

    def execute(self, max_steps: int = 100000) -> str:
        """Execute the Befunge program."""
        while self.steps < max_steps:
            self.steps += 1
            current = self.get_current_cell()

            if self.debug:
                self.print_debug_info(current)

            if self.visualize and self.steps % 10 == 0:
                time.sleep(0.1)

            # String mode
            if current == '"':
                self.string_mode = not self.string_mode
                self.move()
                continue

            if self.string_mode:
                self.stack.append(ord(current))
                self.move()
                continue

            # Execute instruction
            if current == '@':
                # End program
                break

            elif current in '0123456789':
                # Push number
                self.stack.append(int(current))

            elif current == '+':
                # Addition
                b = self.stack.pop() if self.stack else 0
                a = self.stack.pop() if self.stack else 0
                self.stack.append(a + b)

            elif current == '-':
                # Subtraction
                b = self.stack.pop() if self.stack else 0
                a = self.stack.pop() if self.stack else 0
                self.stack.append(a - b)

            elif current == '*':
                # Multiplication
                b = self.stack.pop() if self.stack else 0
                a = self.stack.pop() if self.stack else 0
                self.stack.append(a * b)

            elif current == '/':
                # Division
                b = self.stack.pop() if self.stack else 0
                a = self.stack.pop() if self.stack else 0
                self.stack.append(a // b if b != 0 else 0)

            elif current == '%':
                # Modulo
                b = self.stack.pop() if self.stack else 0
                a = self.stack.pop() if self.stack else 0
                self.stack.append(a % b if b != 0 else 0)

            elif current == '!':
                # Logical NOT
                a = self.stack.pop() if self.stack else 0
                self.stack.append(1 if a == 0 else 0)

            elif current == '`':
                # Greater than
                b = self.stack.pop() if self.stack else 0
                a = self.stack.pop() if self.stack else 0
                self.stack.append(1 if a > b else 0)

            elif current == '>':
                # Move right
                self.direction = (1, 0)

            elif current == '<':
                # Move left
                self.direction = (-1, 0)

            elif current == '^':
                # Move up
                self.direction = (0, -1)

            elif current == 'v':
                # Move down
                self.direction = (0, 1)

            elif current == '_':
                # Horizontal if
                a = self.stack.pop() if self.stack else 0
                self.direction = (1, 0) if a == 0 else (-1, 0)

            elif current == '|':
                # Vertical if
                a = self.stack.pop() if self.stack else 0
                self.direction = (0, 1) if a == 0 else (0, -1)

            elif current == ':':
                # Duplicate
                if self.stack:
                    self.stack.append(self.stack[-1])
                else:
                    self.stack.append(0)

            elif current == '\\':
                # Swap
                if len(self.stack) >= 2:
                    self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

            elif current == '$':
                # Pop and discard
                if self.stack:
                    self.stack.pop()

            elif current == '.':
                # Output as number
                if self.stack:
                    num = self.stack.pop()
                    self.output.append(str(num))
                else:
                    self.output.append('0')

            elif current == ',':
                # Output as ASCII
                if self.stack:
                    char = chr(self.stack.pop() % 256)
                    self.output.append(char)

            elif current == '#':
                # Bridge (skip next cell)
                self.move()

            elif current == ' ':
                # No operation
                pass

            self.move()

        return ''.join(self.output)

    def print_debug_info(self, current: str):
        """Print debug information."""
        print(f"Step {self.steps}: Pos({self.pc_x},{self.pc_y}) Cmd='{current}' "
              f"Dir={self.direction} Stack={self.stack[-5:] if len(self.stack) > 5 else self.stack}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <befunge_file.bf> [--visualize] [--debug]")
        print("\nExample:")
        print("  python interpreter.py hello_web3.bf")
        print("  python interpreter.py blockchain_calc.bf --debug")
        sys.exit(1)

    filename = sys.argv[1]
    visualize = '--visualize' in sys.argv
    debug = '--debug' in sys.argv

    try:
        with open(filename, 'r') as f:
            program = f.read()

        print(f"🔷 Befunge-93 Interpreter - Web3 Edition")
        print(f"📄 Running: {filename}\n")
        print("=" * 50)

        interpreter = BefungeInterpreter(visualize=visualize, debug=debug)
        interpreter.load_program(program)

        output = interpreter.execute()

        print("\n🔤 Output:")
        print(output)
        print("=" * 50)
        print(f"\n✅ Execution completed in {interpreter.steps} steps")
        print(f"📊 Output length: {len(output)} characters")
        print(f"📚 Final stack: {interpreter.stack}")

    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
