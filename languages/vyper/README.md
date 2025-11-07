# 🐍 Vyper Smart Contracts

Professional Vyper smart contract examples demonstrating secure DeFi patterns and EVM development.

## 📋 Contents

- **SimpleVault.vy** - ETH vault contract
  - Deposit and withdrawal functionality
  - Balance tracking per user
  - Pausable mechanism
  - Owner controls
  - Emergency withdrawal

- **ERC20Token.vy** - Standard ERC20 implementation
  - Full ERC20 interface
  - Mint and burn functionality
  - Supply cap enforcement
  - Owner-only minting
  - Transfer and approval system

## 🚀 Quick Start

### Prerequisites

```bash
python >= 3.10
pip >= 23.0
```

### Installation

```bash
cd languages/vyper

# Install Vyper compiler
pip install vyper

# Or use specific version
pip install vyper==0.3.9
```

### Compile

```bash
# Compile a contract
vyper SimpleVault.vy

# Compile to ABI
vyper -f abi SimpleVault.vy > SimpleVault.abi

# Compile to bytecode
vyper -f bytecode SimpleVault.vy > SimpleVault.bin

# Compile with optimization
vyper -f bytecode_runtime SimpleVault.vy
```

### Deploy with Brownie

```bash
# Install Brownie
pip install eth-brownie

# Initialize project
brownie init

# Deploy
brownie run scripts/deploy.py
```

## 🔧 Contract Features

### SimpleVault

A secure ETH vault with:

- **Deposits**: Accept ETH with min/max limits
- **Withdrawals**: Users can withdraw their deposits
- **Balance Tracking**: Individual balance management
- **Pausable**: Emergency pause mechanism
- **Owner Controls**: Admin functions for vault management
- **Events**: Comprehensive event logging

### ERC20Token

A complete ERC20 implementation with:

- **Standard Functions**: transfer, approve, transferFrom
- **Minting**: Owner can mint up to max supply
- **Burning**: Users can burn their tokens
- **Supply Cap**: Configurable maximum supply
- **Decimal Support**: Configurable token decimals

## 📚 Usage Examples

### Deploy SimpleVault

```python
from vyper import compile_code

# Compile contract
with open('SimpleVault.vy', 'r') as f:
    source = f.read()

output = compile_code(source, ['abi', 'bytecode'])

# Deploy with web3.py
contract = w3.eth.contract(
    abi=output['abi'],
    bytecode=output['bytecode']
)
tx_hash = contract.constructor().transact()
```

### Interact with Vault

```python
# Deposit ETH
vault.functions.deposit().transact({'value': Web3.to_wei(1, 'ether')})

# Check balance
balance = vault.functions.get_my_balance().call()

# Withdraw
vault.functions.withdraw(Web3.to_wei(0.5, 'ether')).transact()
```

### Deploy ERC20Token

```python
# Deploy with parameters
token = deploy_contract(
    'ERC20Token',
    name="My Token",
    symbol="MTK",
    decimals=18,
    initial_supply=1000000 * 10**18,
    max_supply=10000000 * 10**18
)
```

### Interact with Token

```python
# Transfer tokens
token.functions.transfer(recipient, amount).transact()

# Approve spender
token.functions.approve(spender, amount).transact()

# Mint new tokens (owner only)
token.functions.mint(recipient, amount).transact()

# Burn tokens
token.functions.burn(amount).transact()
```

## 🧪 Testing

```bash
# Run tests with Brownie
brownie test

# With coverage
brownie test --coverage

# Specific test
brownie test tests/test_vault.py
```

## 📖 Project Structure

```
vyper/
├── SimpleVault.vy       # ETH vault contract
├── ERC20Token.vy        # ERC20 token implementation
├── tests/               # Contract tests
├── scripts/             # Deployment scripts
└── README.md            # This file
```

## 🔐 Security Features

### Vyper Safety Benefits

- **No class inheritance**: Prevents complex inheritance bugs
- **Bounds checking**: Automatic array bounds verification
- **Overflow protection**: Safe math operations
- **No inline assembly**: Reduced attack surface
- **Readable syntax**: Python-like code for easier auditing

### Contract Security

- Input validation on all functions
- Access control for privileged operations
- Reentrancy protection via state changes before external calls
- Event logging for transparency
- Emergency pause mechanism

## 📚 Learn More

- [Vyper Documentation](https://docs.vyperlang.org/)
- [Vyper by Example](https://vyper.readthedocs.io/en/latest/vyper-by-example.html)
- [Brownie Documentation](https://eth-brownie.readthedocs.io/)

## 🎯 Why Vyper?

- **Security-focused**: Designed to prevent common vulnerabilities
- **Auditability**: Python-like syntax is easier to read and audit
- **No footguns**: Removes dangerous Solidity features
- **EVM compatible**: Compiles to standard EVM bytecode
- **Growing ecosystem**: Used by major DeFi projects (Curve, Yearn)

## 📄 License

MIT License - See LICENSE file for details
