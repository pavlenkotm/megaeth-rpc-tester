# 🌐 AssemblyScript Web3 WASM

Web3 utilities compiled to WebAssembly using AssemblyScript.

## 📋 Contents

- **assembly/index.ts** - AssemblyScript utilities
  - Keccak-256 (placeholder)
  - Hex conversions
  - Address validation
  - Wei/Eth conversion
  - Hash functions

## 🚀 Quick Start

```bash
cd languages/assemblyscript

# Install dependencies
npm install

# Build WASM
npm run asbuild
```

## 📚 Usage

```javascript
const fs = require('fs');
const wasmModule = await WebAssembly.instantiate(
  fs.readFileSync('./build/optimized.wasm')
);

const { isValidAddress } = wasmModule.instance.exports;
```

## 📄 License

MIT License
