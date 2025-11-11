#!/usr/bin/env python3
"""
Whitespace Interpreter for Web3 Examples

Interprets Whitespace programs where only Space, Tab, and Linefeed are meaningful.
All other characters are treated as comments.
"""

import sys
from typing import List, Dict, Optional


class WhitespaceInterpreter:
    """Interpreter for the Whitespace esoteric programming language."""

    def __init__(self, show_instructions: bool = False):
        """Initialize the interpreter."""
        self.stack: List[int] = []
        self.heap: Dict[int, int] = {}
        self.call_stack: List[int] = []
        self.labels: Dict[str, int] = {}
        self.pc: int = 0  # Program counter
        self.output: List[str] = []
        self.show_instructions = show_instructions

    def parse_program(self, source: str) -> List[str]:
        """Extract only whitespace characters from source."""
        # Convert to internal representation
        tokens = []
        for char in source:
            if char == ' ':
                tokens.append('S')  # Space
            elif char == '\t':
                tokens.append('T')  # Tab
            elif char == '\n':
                tokens.append('L')  # Linefeed
        return tokens

    def parse_number(self, tokens: List[str], start: int) -> tuple[int, int]:
        """Parse a number from tokens (S=0, T=1, L=terminator)."""
        idx = start
        sign = 1

        if tokens[idx] == 'S':
            sign = 1
        elif tokens[idx] == 'T':
            sign = -1
        idx += 1

        binary = ""
        while idx < len(tokens) and tokens[idx] != 'L':
            if tokens[idx] == 'S':
                binary += '0'
            elif tokens[idx] == 'T':
                binary += '1'
            idx += 1

        if binary == "":
            number = 0
        else:
            number = int(binary, 2) * sign

        return number, idx + 1

    def execute(self, source: str, input_data: str = "") -> str:
        """Execute Whitespace source code."""
        tokens = self.parse_program(source)

        if self.show_instructions:
            print(f"📋 Total tokens: {len(tokens)}")
            print(f"🔤 Token preview: {''.join(tokens[:50])}...\n")

        input_idx = 0

        while self.pc < len(tokens):
            try:
                instruction = self._read_instruction(tokens)

                if instruction is None:
                    break

                if self.show_instructions:
                    print(f"PC={self.pc}: {instruction}")

                # Stack manipulation
                if instruction.startswith('SS'):
                    # Push number
                    num, self.pc = self.parse_number(tokens, self.pc + 2)
                    self.stack.append(num)

                elif instruction == 'SLS':
                    # Duplicate top
                    if self.stack:
                        self.stack.append(self.stack[-1])
                    self.pc += 3

                elif instruction == 'SLT':
                    # Swap top two
                    if len(self.stack) >= 2:
                        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
                    self.pc += 3

                elif instruction == 'SLL':
                    # Discard top
                    if self.stack:
                        self.stack.pop()
                    self.pc += 3

                # Arithmetic
                elif instruction == 'TSSS':
                    # Addition
                    if len(self.stack) >= 2:
                        b = self.stack.pop()
                        a = self.stack.pop()
                        self.stack.append(a + b)
                    self.pc += 4

                elif instruction == 'TSST':
                    # Subtraction
                    if len(self.stack) >= 2:
                        b = self.stack.pop()
                        a = self.stack.pop()
                        self.stack.append(a - b)
                    self.pc += 4

                elif instruction == 'TSSL':
                    # Multiplication
                    if len(self.stack) >= 2:
                        b = self.stack.pop()
                        a = self.stack.pop()
                        self.stack.append(a * b)
                    self.pc += 4

                # I/O
                elif instruction == 'TLSS':
                    # Output character
                    if self.stack:
                        char = chr(self.stack.pop() % 128)
                        self.output.append(char)
                        if self.show_instructions:
                            print(f"  → Output: {repr(char)}")
                    self.pc += 4

                elif instruction == 'TLST':
                    # Output number
                    if self.stack:
                        num = self.stack.pop()
                        self.output.append(str(num))
                    self.pc += 4

                # End program
                elif instruction == 'LLL':
                    break

                else:
                    self.pc += 1

            except Exception as e:
                if self.show_instructions:
                    print(f"❌ Error at PC={self.pc}: {e}")
                break

        return ''.join(self.output)

    def _read_instruction(self, tokens: List[str]) -> Optional[str]:
        """Read the next instruction."""
        if self.pc >= len(tokens):
            return None

        # Try to match instruction patterns
        remaining = ''.join(tokens[self.pc:self.pc+10])

        # Check various instruction patterns
        if remaining.startswith('SS'):
            return 'SS'  # Push number
        elif remaining.startswith('SLS'):
            return 'SLS'  # Duplicate
        elif remaining.startswith('SLT'):
            return 'SLT'  # Swap
        elif remaining.startswith('SLL'):
            return 'SLL'  # Discard
        elif remaining.startswith('TSSS'):
            return 'TSSS'  # Add
        elif remaining.startswith('TSST'):
            return 'TSST'  # Subtract
        elif remaining.startswith('TSSL'):
            return 'TSSL'  # Multiply
        elif remaining.startswith('TLSS'):
            return 'TLSS'  # Output char
        elif remaining.startswith('TLST'):
            return 'TLST'  # Output number
        elif remaining.startswith('LLL'):
            return 'LLL'  # End

        return None


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <whitespace_file.ws> [--show-instructions]")
        print("\nExample:")
        print("  python interpreter.py hello_web3.ws")
        print("  python interpreter.py hello_web3.ws --show-instructions")
        sys.exit(1)

    filename = sys.argv[1]
    show_instructions = '--show-instructions' in sys.argv

    try:
        with open(filename, 'r') as f:
            source = f.read()

        print(f"⬜ Whitespace Interpreter - Web3 Edition")
        print(f"📄 Running: {filename}\n")
        print("=" * 50)

        interpreter = WhitespaceInterpreter(show_instructions=show_instructions)
        output = interpreter.execute(source)

        print("\n🔤 Output:")
        print(output)
        print("=" * 50)
        print(f"\n✅ Execution completed")
        print(f"📊 Output length: {len(output)} characters")

        if show_instructions:
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
