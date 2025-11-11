# Whitespace - Invisible Web3 Programming

![Whitespace](https://img.shields.io/badge/Whitespace-Esoteric-lightgrey)
![Difficulty](https://img.shields.io/badge/Difficulty-Extreme-red)

## Overview

Whitespace is an esoteric programming language where ONLY whitespace characters (space, tab, and linefeed) are meaningful. All other characters are ignored, making it perfect for hiding code in plain sight!

## Features

- ✅ Only uses Space, Tab, and Linefeed
- ✅ All other characters are comments
- ✅ Stack-based architecture
- ✅ Turing-complete
- ✅ Perfect for steganography

## Syntax

The language consists of three characters:

| Character | Notation | Description |
|-----------|----------|-------------|
| Space | `[Space]` | Represents 0 or push |
| Tab | `[Tab]` | Represents 1 or operation |
| Linefeed (LF) | `[LF]` | End of instruction |

## Instruction Set

### Stack Manipulation
- `[Space][Space]` - Push number onto stack
- `[Space][LF][Space]` - Duplicate top of stack
- `[Space][LF][Tab]` - Swap top two items
- `[Space][LF][LF]` - Discard top of stack

### Arithmetic
- `[Tab][Space][Space][Space]` - Addition
- `[Tab][Space][Space][Tab]` - Subtraction
- `[Tab][Space][Space][LF]` - Multiplication
- `[Tab][Space][Tab][Space]` - Integer Division
- `[Tab][Space][Tab][Tab]` - Modulo

### I/O
- `[Tab][LF][Space][Space]` - Output character
- `[Tab][LF][Space][Tab]` - Output number
- `[Tab][LF][Tab][Space]` - Read character
- `[Tab][LF][Tab][Tab]` - Read number

## Examples

### hello_web3.ws
Outputs "Web3!" using only whitespace characters. The visible text in the file is ignored by the interpreter.

### block_number.ws
Demonstrates simple arithmetic operations representing block number calculations.

### interpreter.py
Python-based Whitespace interpreter with visible instruction highlighting.

## Usage

### Run Examples

```bash
# Hello Web3 example
python interpreter.py hello_web3.ws

# Block number calculation
python interpreter.py block_number.ws

# View visible representation
python interpreter.py hello_web3.ws --show-instructions
```

## Web3 Concepts

This esoteric language demonstrates:

1. **Steganography**: Hide Web3 operations in visible text
2. **Stack-Based Operations**: Similar to EVM (Ethereum Virtual Machine)
3. **Deterministic Execution**: Same as blockchain transactions
4. **Minimalist Design**: Core computational primitives

## Educational Value

- **EVM Understanding**: Stack-based operations like Ethereum
- **Code Obfuscation**: Understanding hidden code patterns
- **Low-Level Thinking**: Direct stack manipulation
- **Theoretical CS**: Turing completeness with minimal syntax

## Technical Details

Whitespace programs are:
- Stack-based (like EVM)
- Turing-complete
- Perfect for code golf
- Great for understanding computational minimalism

## Why This Matters for Web3

1. **EVM Similarity**: Ethereum Virtual Machine is also stack-based
2. **Security**: Understanding obfuscation and hidden code
3. **Optimization**: Minimal instruction sets like optimized bytecode
4. **Theory**: Foundation of computational completeness

## Resources

- [Whitespace Tutorial](https://web.archive.org/web/20150717140342/http://compsoc.dur.ac.uk/whitespace/tutorial.php)
- [Whitespace on Esolangs](https://esolangs.org/wiki/Whitespace)
- [Online Interpreter](https://vii5ard.github.io/whitespace/)

## Fun Facts

- Created as an April Fools' joke in 2003
- Source code looks empty in text editors
- You can write poems that are also programs
- Perfect for code steganography

---

*Note: While fascinating, use practical languages for real blockchain development. This is for education and fun!*
