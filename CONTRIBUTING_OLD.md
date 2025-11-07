# Contributing to MegaETH RPC Tester

Thank you for your interest in contributing to MegaETH RPC Tester! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- pip or poetry for dependency management

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/megaeth-rpc-tester.git
   cd megaeth-rpc-tester
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Install development dependencies:**
   ```bash
   pip install black isort flake8 mypy pytest pytest-asyncio pytest-cov
   ```

## 📝 Development Workflow

### 1. Create a Branch

Create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

### 2. Make Changes

- Write clear, concise code
- Follow the existing code style
- Add tests for new features
- Update documentation as needed

### 3. Code Style

We use several tools to maintain code quality:

**Format code with Black:**
```bash
black rpc_tester/
```

**Sort imports with isort:**
```bash
isort rpc_tester/
```

**Lint with flake8:**
```bash
flake8 rpc_tester/
```

**Type check with mypy:**
```bash
mypy rpc_tester/
```

### 4. Run Tests

Always run tests before submitting:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=rpc_tester --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run async tests
pytest tests/test_integration.py -v
```

### 5. Commit Messages

Write clear, descriptive commit messages:

```
Add feature: Brief description

Longer explanation of what changed and why.
Describe the problem this solves or the feature it adds.

- Bullet points for multiple changes
- Reference issues with #123
```

**Good examples:**
```
Add WebSocket support for real-time testing

Implemented WebSocketTester class with subscription support.
Enables testing of WebSocket RPC endpoints and real-time
event monitoring.

Fixes #45
```

```
Fix rate limiting edge case

Fixed issue where rate limiter could allow burst beyond
configured limit when tokens accumulated during idle periods.

Closes #67
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 🧪 Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Test both success and failure cases
- Use fixtures for common setup

**Example test:**
```python
import pytest
from rpc_tester.core import RPCTester

@pytest.mark.asyncio
async def test_endpoint_success(sample_config):
    """Test successful RPC request."""
    async with RPCTester(sample_config) as tester:
        result = await tester.test_endpoint(
            "https://eth.llamarpc.com",
            "eth_blockNumber"
        )
        assert result is not None
        assert len(result) > 0
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Mock external dependencies
- Use parametrize for multiple test cases

## 📚 Documentation

### Docstrings

Use Google-style docstrings:

```python
def calculate_percentile(data: List[float], percentile: float) -> float:
    """
    Calculate percentile value from data.

    Args:
        data: List of numeric values
        percentile: Percentile to calculate (0.0-1.0)

    Returns:
        Calculated percentile value

    Raises:
        ValueError: If percentile is out of range

    Example:
        >>> calculate_percentile([1, 2, 3, 4, 5], 0.95)
        4.8
    """
    pass
```

### README Updates

Update README.md when adding:
- New features
- New CLI options
- New configuration options
- Breaking changes

## 🐛 Bug Reports

When reporting bugs, include:

1. **Description:** Clear description of the bug
2. **Steps to Reproduce:** Minimal steps to reproduce
3. **Expected Behavior:** What should happen
4. **Actual Behavior:** What actually happens
5. **Environment:**
   - Python version
   - OS version
   - Package version

**Template:**
```markdown
## Bug Description
Brief description of the bug.

## Steps to Reproduce
1. Run command: `python -m rpc_tester ...`
2. Observe error

## Expected Behavior
Should successfully test endpoint.

## Actual Behavior
Raises ConnectionError.

## Environment
- Python: 3.11.2
- OS: Ubuntu 22.04
- Version: 2.0.0
```

## ✨ Feature Requests

When requesting features:

1. **Use Case:** Describe the problem/use case
2. **Proposed Solution:** How should it work?
3. **Alternatives:** Other approaches considered
4. **Additional Context:** Examples, mockups, etc.

## 🔍 Code Review Process

Pull requests are reviewed for:

1. **Functionality:** Does it work as intended?
2. **Tests:** Are there adequate tests?
3. **Documentation:** Is it documented?
4. **Code Style:** Does it follow conventions?
5. **Performance:** Are there performance implications?
6. **Security:** Are there security concerns?

## 📋 Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines (black, isort, flake8)
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts

## 🤝 Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the code of conduct

## 📞 Getting Help

- **Issues:** Open an issue for bugs or features
- **Discussions:** Use GitHub Discussions for questions
- **Email:** Contact maintainers for security issues

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- CHANGELOG.md for their contributions
- README.md contributors section
- GitHub contributors page

Thank you for contributing to MegaETH RPC Tester!
