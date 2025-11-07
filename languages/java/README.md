# ☕ Java Web3 Examples

Professional Java examples for Ethereum development using Web3j library.

## 📋 Contents

- **Web3Example.java** - Complete Web3j client implementation
  - Connect to Ethereum RPC
  - Query blockchain data
  - Send transactions
  - Check balances
  - Monitor blocks and transactions
  - Gas estimation

## 🚀 Quick Start

### Prerequisites

```bash
Java >= 11
Maven >= 3.8
```

### Installation

```bash
cd languages/java

# Install dependencies
mvn clean install
```

### Build

```bash
# Compile
mvn compile

# Package JAR
mvn package
```

### Run

```bash
# Run with Maven
mvn exec:java -Dexec.mainClass="com.web3.examples.Web3Example"

# Or run JAR
java -jar target/web3-java-examples-1.0.0.jar
```

## 🔧 Features

### Blockchain Queries

- **Block Information**: Get latest block number and block details
- **Balance Queries**: Check ETH balance of any address
- **Gas Pricing**: Retrieve current network gas prices
- **Chain Info**: Get chain ID and client version
- **Transaction Data**: Query transactions and receipts

### Transaction Management

- **Send ETH**: Transfer Ether between accounts
- **Gas Estimation**: Calculate required gas for transactions
- **Transaction Monitoring**: Wait for confirmations
- **Receipt Verification**: Check transaction status

### Utility Functions

- **Address Validation**: Verify Ethereum address format
- **Unit Conversion**: Convert between Wei and Ether
- **Credentials Management**: Handle private keys securely

## 📚 Usage Examples

### Connect to Ethereum

```java
// Read-only connection
Web3Example web3 = new Web3Example("https://eth.llamarpc.com", null);

// With private key for transactions
Web3Example web3 = new Web3Example(rpcUrl, privateKey);
```

### Query Blockchain

```java
// Get latest block
BigInteger blockNumber = web3.getBlockNumber();

// Get balance
BigDecimal balance = web3.getBalanceInEth(address);

// Get gas price
BigInteger gasPrice = web3.getGasPrice();

// Get chain ID
BigInteger chainId = web3.getChainId();
```

### Send Transaction

```java
// Send 0.1 ETH
BigDecimal amount = new BigDecimal("0.1");
TransactionReceipt receipt = web3.sendEth(recipientAddress, amount);

System.out.println("Transaction hash: " + receipt.getTransactionHash());
System.out.println("Status: " + receipt.getStatus());
```

### Monitor Transaction

```java
// Get transaction details
Transaction tx = web3.getTransaction(txHash);

// Get transaction receipt
TransactionReceipt receipt = web3.getTransactionReceipt(txHash);

// Check if successful
boolean success = receipt.getStatus().equals("0x1");
```

### Validate Address

```java
boolean isValid = Web3Example.isValidAddress("0x...");
```

## 🧪 Testing

```bash
# Run tests
mvn test

# With coverage
mvn test jacoco:report

# View coverage report
open target/site/jacoco/index.html
```

## 📖 Project Structure

```
java/
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/web3/examples/
│   │           └── Web3Example.java
│   └── test/
│       └── java/
│           └── com/web3/examples/
│               └── Web3ExampleTest.java
├── pom.xml             # Maven configuration
└── README.md           # This file
```

## 🔐 Security Best Practices

- Never hardcode private keys
- Use environment variables for sensitive data
- Validate all inputs
- Handle exceptions properly
- Use secure RPC endpoints
- Verify transaction receipts before assuming success

## 📚 Learn More

- [Web3j Documentation](https://docs.web3j.io/)
- [Web3j GitHub](https://github.com/web3j/web3j)
- [Ethereum Java Development](https://ethereum.org/en/developers/docs/programming-languages/java/)

## 🎯 Use Cases

- **Enterprise Integration**: Connect Java backends to Ethereum
- **Trading Platforms**: Build automated trading systems
- **Wallet Services**: Create wallet management systems
- **Data Analytics**: Analyze blockchain data
- **DApp Backends**: Server-side Web3 logic

## 📄 License

MIT License - See LICENSE file for details
