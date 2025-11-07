# Testing Guide

This guide explains how to run tests for each language in the repository.

## Solidity

```bash
cd languages/solidity
npm test

# With coverage
npm run coverage

# Specific test
npx hardhat test test/Web3Token.test.js
```

## TypeScript

```bash
cd languages/typescript
npm test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

## Rust/Anchor

```bash
cd languages/rust
anchor test

# Verbose output
anchor test -- --nocapture

# Specific test
cargo test test_mint_and_transfer
```

## Go

```bash
cd languages/go
go test -v ./...

# With coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Python

```bash
cd ../  # root directory
pytest tests/ -v

# With coverage
pytest --cov=rpc_tester tests/
```

## Java

```bash
cd languages/java
mvn test

# With coverage (JaCoCo)
mvn clean test jacoco:report
```

## C++

```bash
cd languages/cpp
mkdir build && cd build
cmake ..
make
ctest
```

## Move

```bash
cd languages/move
aptos move test

# Verbose
aptos move test --verbose

# Coverage
aptos move test --coverage
```

## Testing Best Practices

### For Smart Contracts

- Test all edge cases
- Test access controls
- Test arithmetic operations for overflow
- Test reentrancy scenarios
- Use fuzzing where applicable
- Aim for >80% code coverage

### For Applications

- Unit test individual functions
- Integration test workflows
- Mock external dependencies
- Test error handling
- Test with different network conditions

### CI/CD

All tests run automatically on:
- Every pull request
- Every push to main branch
- Nightly builds (full test suite)

## Coverage Requirements

| Language | Minimum Coverage |
|----------|------------------|
| Solidity | 80% |
| TypeScript | 70% |
| Rust | 75% |
| Go | 70% |
| Python | 80% |
| Java | 70% |

## Continuous Integration

Our CI pipeline runs:
1. Linting and formatting checks
2. Compilation/build verification
3. Unit tests
4. Integration tests (where applicable)
5. Security scans

See `.github/workflows/multi-language-ci.yml` for details.
