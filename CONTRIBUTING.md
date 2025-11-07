# Contributing to Web3 Multi-Language Playground

Thank you for your interest in contributing! This repository showcases Web3 development across 14+ programming languages. We welcome contributions in any language or technology stack.

## 🌟 Ways to Contribute

- 🐛 **Bug Fixes**: Fix issues in any language implementation
- ✨ **New Features**: Add functionality to existing examples
- 🔤 **New Languages**: Add examples in additional programming languages
- 📚 **Documentation**: Improve READMEs, add tutorials, fix typos
- 🧪 **Tests**: Add or improve test coverage
- 🎨 **UI/UX**: Enhance the landing page or frontend components

## 🚀 Getting Started

### Prerequisites

Depending on which language you want to contribute to, you'll need different tools:

#### Smart Contract Languages
- **Solidity**: Node.js 16+, Hardhat
- **Vyper**: Python 3.10+, Vyper compiler
- **Rust**: Rust 1.70+, Anchor CLI
- **Move**: Aptos CLI

#### Application Languages
- **TypeScript/JavaScript**: Node.js 18+, npm/yarn
- **Go**: Go 1.21+
- **Python**: Python 3.9+
- **Java**: JDK 11+, Maven
- **Ruby**: Ruby 2.7+

#### Systems Languages
- **C++**: GCC/Clang, CMake, OpenSSL
- **Zig**: Zig 0.11+
- **AssemblyScript**: Node.js, asc compiler
- **Haskell**: GHC 9.0+

### Setting Up Development Environment

1. **Fork and clone:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/megaeth-rpc-tester.git
   cd megaeth-rpc-tester
   ```

2. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up your language environment:**
   ```bash
   # For example, if working on TypeScript:
   cd languages/typescript
   npm install
   ```

## 📝 Contribution Guidelines

### Code Quality

- Follow the existing code style in each language
- Add comprehensive comments and documentation
- Include error handling and input validation
- Write clean, maintainable code

### Documentation

- Update the README.md in the relevant language folder
- Include usage examples
- Document any new dependencies
- Add inline code comments for complex logic

### Testing

- Add tests for new functionality where applicable
- Ensure existing tests still pass
- Include test instructions in your PR

### Commit Messages

Use conventional commit format:

```
type(scope): brief description

- feat(solidity): add staking contract example
- fix(typescript): correct wallet connection bug
- docs(readme): update installation instructions
- test(rust): add integration tests for token program
- chore(deps): upgrade ethers.js to v6
```

## 🔤 Adding a New Language

To add a new programming language:

1. **Create language folder:**
   ```bash
   mkdir languages/your-language
   cd languages/your-language
   ```

2. **Add working code example:**
   - Implement a Web3-related functionality
   - RPC client, smart contract, or utility functions
   - Ensure code compiles/runs successfully

3. **Create README.md:**
   - Overview of the example
   - Prerequisites and setup
   - Build/run instructions
   - Usage examples
   - License information

4. **Add dependencies:**
   - Include package manager files (package.json, Cargo.toml, etc.)
   - List all required dependencies

5. **Update main README:**
   - Add your language to the language table
   - Include brief description

6. **Submit PR:**
   - Explain what the example demonstrates
   - Include screenshots if applicable

## 🧪 Testing Guidelines

### Language-Specific Tests

- **Solidity**: Use Hardhat or Foundry tests
- **Rust**: Use `cargo test` and Anchor tests
- **TypeScript**: Use Jest or Vitest
- **Go**: Use `go test`
- **Python**: Use pytest
- **Java**: Use JUnit

Example test structure:

```bash
languages/your-language/
├── src/
├── tests/
│   └── test_example.ext
├── README.md
└── package.json  # or equivalent
```

## 📦 Pull Request Process

1. **Update documentation:**
   - Update relevant READMEs
   - Add your changes to CHANGELOG.md

2. **Ensure quality:**
   - Code compiles/runs successfully
   - Tests pass (if applicable)
   - No linting errors
   - Documentation is clear

3. **Create PR:**
   - Use a descriptive title
   - Explain what changes you made and why
   - Reference any related issues
   - Add screenshots/demos if applicable

4. **Review process:**
   - Address reviewer feedback
   - Make requested changes
   - Keep PR focused and atomic

## 🎯 What We're Looking For

### High Priority

- ✅ Examples in new languages (Kotlin, Swift, C#, etc.)
- ✅ More advanced smart contract patterns
- ✅ Additional DApp frontend examples
- ✅ Integration examples (oracles, bridges, etc.)
- ✅ Performance optimizations

### Medium Priority

- ✅ Enhanced error handling
- ✅ More comprehensive tests
- ✅ CI/CD improvements
- ✅ Documentation improvements

### Nice to Have

- ✅ Video tutorials
- ✅ Blog posts / articles
- ✅ Translations
- ✅ Infographics

## 🤝 Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a welcoming and inspiring community for all.

## 💬 Community

- **Issues**: Report bugs or request features
- **Discussions**: Ask questions, share ideas
- **Discord**: [Join our community](https://discord.gg/your-invite) (if applicable)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for making Web3 development more accessible! 🚀

---

**Questions?** Open an issue or start a discussion. We're here to help!
