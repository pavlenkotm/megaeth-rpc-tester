# Yul - Ethereum Inline Assembly

![Yul](https://img.shields.io/badge/Yul-Ethereum-blue)
![Optimization](https://img.shields.io/badge/Gas-Optimized-green)

## Overview

Yul is an intermediate language that can compile to bytecode for different backends. It's primarily used for inline assembly in Solidity and for writing highly optimized smart contracts.

## Features

- ✅ Gas-Optimized Token
- ✅ Low-Level EVM Operations
- ✅ Direct Memory/Storage Access
- ✅ Maximum Control

## Usage

Yul can be used:
1. As inline assembly in Solidity
2. As standalone contracts compiled with `solc --strict-assembly`
3. For bytecode optimization

```bash
# Compile Yul contract
solc --strict-assembly token.yul
```

## Examples

### Gas-Optimized Token (`token.yul`)

Minimal ERC-20 implementation:
- Direct storage slot manipulation
- Optimized transfer logic
- Minimal gas usage

### Memory Manager (`memory.yul`)

Low-level memory operations:
- Dynamic array handling
- Efficient copying
- Memory safety

## Resources

- [Yul Documentation](https://docs.soliditylang.org/en/latest/yul.html)
- [Yul Specification](https://docs.soliditylang.org/en/latest/yul.html#specification-of-yul)
- [EVM Opcodes](https://www.evm.codes/)

## License

MIT License
