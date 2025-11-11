# Befunge - 2D Web3 Programming

![Befunge](https://img.shields.io/badge/Befunge-2D-blue)
![Esoteric](https://img.shields.io/badge/Esoteric-Extreme-red)

## Overview

Befunge is a two-dimensional esoteric programming language where the program counter can move in four directions (up, down, left, right) across a grid of characters. It's stack-based and Turing-complete, making blockchain operations flow in any direction!

## Features

- ✅ Two-dimensional code layout
- ✅ Stack-based execution (like EVM!)
- ✅ Four-directional flow control
- ✅ Self-modifying code capability
- ✅ Turing-complete
- ✅ Visually unique programs

## How It Works

### The 2D Grid

Programs are laid out in a grid where each cell contains a command. The instruction pointer (IP) starts at the top-left corner moving right.

```
>987v>.v
v456<  :
>321 ^ _@
```

### Movement Commands

| Command | Direction |
|---------|-----------|
| `>` | Move right |
| `<` | Move left |
| `^` | Move up |
| `v` | Move down |
| `#` | Bridge (skip next cell) |
| `?` | Random direction |

### Stack Operations

| Command | Action |
|---------|--------|
| `0-9` | Push digit onto stack |
| `+` | Add top two values |
| `-` | Subtract |
| `*` | Multiply |
| `/` | Divide |
| `%` | Modulo |
| `:` | Duplicate top value |
| `\` | Swap top two values |
| `$` | Pop and discard |

### I/O Operations

| Command | Action |
|---------|--------|
| `.` | Pop and output as number |
| `,` | Pop and output as ASCII |
| `&` | Read integer input |
| `~` | Read character input |

### Logic & Flow

| Command | Action |
|---------|--------|
| `` ` `` | Greater than (push 1 or 0) |
| `!` | Logical NOT |
| `_` | Horizontal if (pop: right if 0, left if not) |
| `\|` | Vertical if (pop: down if 0, up if not) |
| `@` | End program |

### Memory Operations

| Command | Action |
|---------|--------|
| `g` | Get value from grid (y,x) |
| `p` | Put value into grid (y,x,value) |
| `"` | Toggle string mode |

## Examples

### hello_web3.bf
Classic "Hello Web3" output using Befunge's 2D navigation.

### blockchain_calc.bf
Demonstrates blockchain calculations flowing in multiple directions.

### hash_path.bf
Hash-like operations where the execution path itself represents the algorithm.

### interpreter.py
Python-based Befunge-93 interpreter with visual execution tracking.

## Usage

### Using Python Interpreter

```bash
# Run a Befunge program
python interpreter.py hello_web3.bf

# Show execution path
python interpreter.py hello_web3.bf --visualize

# Step-by-step debugging
python interpreter.py blockchain_calc.bf --debug
```

### Online Interpreters

- [Befunge Playground](https://www.bedroomlan.org/tools/befunge-playground)
- [TIO - Try It Online](https://tio.run/#befunge)

## Befunge-93 Specification

- **Grid Size**: 80x25 characters
- **Stack**: Unlimited depth (implementation dependent)
- **Wrapping**: Execution wraps around edges
- **Self-Modification**: Code can modify itself using `p`

## Web3 Concepts in 2D

This unique language demonstrates:

### 1. Multi-Directional Flow
Like blockchain state transitions happening in parallel

### 2. Stack-Based Operations
Direct analogy to Ethereum Virtual Machine (EVM)

### 3. Self-Modifying Code
Similar to upgradeable smart contracts

### 4. Deterministic Execution
Same input always produces same path

### 5. Visual Representation
Code flow visualizes transaction paths

## Example Programs

### Hello World

```befunge
"!dlroW olleH">:#,_@
```

How it works:
1. `"` - Start string mode
2. `!dlroW olleH` - Push characters (reversed)
3. `"` - End string mode
4. `>` - Move right
5. `:` - Duplicate top
6. `#` - Skip next
7. `,` - Output character
8. `_` - If 0, go right to `@`, else go left to `:`

### Simple Calculator (Add Two Numbers)

```befunge
&  Get first number
&  Get second number
+  Add them
.  Output result
@  End
```

### Block Number Counter

```befunge
0>1+:.:v
      @
```

## Why Befunge for Blockchain?

### Educational Value

1. **Visual Learning**: See execution flow
2. **Stack Understanding**: Same as EVM operations
3. **State Changes**: Track modifications visually
4. **Parallel Thinking**: Multiple execution paths

### Unique Features

- **2D Layout**: Represents network topology
- **Self-Modification**: Like contract upgrades
- **Multiple Paths**: Like different transaction routes
- **Stack-Based**: Direct EVM analogy

## Programming Tips

### 1. Plan Your Grid
Sketch the execution path before coding.

### 2. Use Comments Wisely
Any character not on the execution path is ignored.

### 3. Leverage Wrapping
Use edge wrapping for compact code.

### 4. Stack Management
Always track what's on the stack.

### 5. Test Incrementally
Build and test small sections.

## Common Patterns

### Loop Pattern
```befunge
v
>1+:#v_@
    ^
```

### Conditional Pattern
```befunge
condition _left pathway  right pathway@
```

### Output Pattern
```befunge
value .,@ or value .@
```

## Technical Details

### Befunge-93 vs Befunge-98

**Befunge-93** (simpler, used here):
- 80x25 grid
- Basic instructions
- Standard for learning

**Befunge-98** (extended):
- Unbounded grid
- Additional instructions
- More complex features

## Resources

- [Befunge on Esolangs](https://esolangs.org/wiki/Befunge)
- [Befunge-93 Spec](https://github.com/catseye/Befunge-93)
- [Tutorial](https://quadium.net/befunge/tutorial.html)
- [Online Interpreter](https://www.bedroomlan.org/tools/befunge-playground)

## Fun Facts

- Created by Chris Pressey in 1993
- Designed to be as difficult to compile as possible
- Self-modifying code capability
- Visual appeal makes it popular for code golf
- Used in programming competitions

## Project Philosophy

Befunge demonstrates:

- **Multi-Dimensional Thinking**: Beyond linear code
- **Visual Programming**: Code as art
- **Stack Operations**: Core to blockchain VMs
- **Creative Problem-Solving**: Think in 2D

## Advanced Examples

### Fibonacci Sequence
```befunge
>1>:.:1+v
^      _@
```

### Factorial
```befunge
&1>:v
  v *<
  >$. @
```

---

*Navigate your Web3 journey in all directions!* ⬆️⬇️⬅️➡️
