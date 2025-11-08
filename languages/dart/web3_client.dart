import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:web3dart/web3dart.dart';

/// Ethereum Web3 Client for Dart/Flutter
/// Supports async operations and smart contract interaction
class EthereumClient {
  final String rpcUrl;
  late Web3Client _client;
  late http.Client _httpClient;

  EthereumClient(this.rpcUrl) {
    _httpClient = http.Client();
    _client = Web3Client(rpcUrl, _httpClient);
  }

  /// Get current block number
  Future<int> getBlockNumber() async {
    return await _client.getBlockNumber();
  }

  /// Get ETH balance for an address
  Future<EtherAmount> getBalance(String address) async {
    final ethAddress = EthereumAddress.fromHex(address);
    return await _client.getBalance(ethAddress);
  }

  /// Get balance in ETH (double)
  Future<double> getBalanceEth(String address) async {
    final balance = await getBalance(address);
    return balance.getValueInUnit(EtherUnit.ether);
  }

  /// Get transaction by hash
  Future<TransactionInformation?> getTransaction(String txHash) async {
    return await _client.getTransactionByHash(txHash);
  }

  /// Get gas price
  Future<EtherAmount> getGasPrice() async {
    return await _client.getGasPrice();
  }

  /// Get gas price in Gwei
  Future<double> getGasPriceGwei() async {
    final gasPrice = await getGasPrice();
    return gasPrice.getValueInUnit(EtherUnit.gwei);
  }

  /// Estimate gas for a transaction
  Future<BigInt> estimateGas({
    required String from,
    required String to,
    EtherAmount? value,
    String? data,
  }) async {
    final transaction = Transaction(
      from: EthereumAddress.fromHex(from),
      to: EthereumAddress.fromHex(to),
      value: value,
      data: data != null ? hexToBytes(data) : null,
    );

    return await _client.estimateGas(
      sender: transaction.from,
      to: transaction.to,
      value: transaction.value,
      data: transaction.data,
    );
  }

  /// Send transaction
  Future<String> sendTransaction({
    required Credentials credentials,
    required String to,
    required EtherAmount value,
    int? gasLimit,
    EtherAmount? gasPrice,
  }) async {
    final transaction = Transaction(
      to: EthereumAddress.fromHex(to),
      value: value,
      gasPrice: gasPrice,
      maxGas: gasLimit,
    );

    return await _client.sendTransaction(
      credentials,
      transaction,
      chainId: 1, // Mainnet
    );
  }

  /// Call contract method (read-only)
  Future<List<dynamic>> callContract({
    required String contractAddress,
    required String functionName,
    required List<dynamic> params,
    required ContractAbi abi,
  }) async {
    final contract = DeployedContract(
      ContractAbi.fromJson(jsonEncode(abi), 'Contract'),
      EthereumAddress.fromHex(contractAddress),
    );

    final function = contract.function(functionName);

    return await _client.call(
      contract: contract,
      function: function,
      params: params,
    );
  }

  /// Listen to new blocks
  Stream<FilterEvent> subscribeToBlocks() {
    return _client.events(FilterOptions.events(
      fromBlock: const BlockNum.pending(),
    ));
  }

  /// Close client
  void dispose() {
    _client.dispose();
    _httpClient.close();
  }
}

/// Wallet Manager for multiple accounts
class WalletManager {
  final EthereumClient client;

  WalletManager(this.client);

  /// Check balances for multiple addresses
  Future<Map<String, double>> getMultipleBalances(List<String> addresses) async {
    final balances = <String, double>{};

    for (final address in addresses) {
      final balance = await client.getBalanceEth(address);
      balances[address] = balance;
    }

    return balances;
  }

  /// Find the richest wallet from a list
  Future<MapEntry<String, double>?> findRichestWallet(List<String> addresses) async {
    final balances = await getMultipleBalances(addresses);

    if (balances.isEmpty) return null;

    return balances.entries.reduce((a, b) => a.value > b.value ? a : b);
  }

  /// Monitor balance changes
  Stream<double> watchBalance(String address, Duration interval) async* {
    while (true) {
      final balance = await client.getBalanceEth(address);
      yield balance;
      await Future.delayed(interval);
    }
  }
}

/// Token Contract Helper
class ERC20Token {
  final String contractAddress;
  final EthereumClient client;

  ERC20Token(this.contractAddress, this.client);

  // Minimal ERC20 ABI
  static const abi = '''
  [
    {
      "constant": true,
      "inputs": [{"name": "_owner", "type": "address"}],
      "name": "balanceOf",
      "outputs": [{"name": "balance", "type": "uint256"}],
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "decimals",
      "outputs": [{"name": "", "type": "uint8"}],
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "name",
      "outputs": [{"name": "", "type": "string"}],
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "symbol",
      "outputs": [{"name": "", "type": "string"}],
      "type": "function"
    }
  ]
  ''';

  /// Get token balance for an address
  Future<BigInt> balanceOf(String address) async {
    final contract = DeployedContract(
      ContractAbi.fromJson(abi, 'ERC20'),
      EthereumAddress.fromHex(contractAddress),
    );

    final function = contract.function('balanceOf');
    final result = await client._client.call(
      contract: contract,
      function: function,
      params: [EthereumAddress.fromHex(address)],
    );

    return result.first as BigInt;
  }
}

/// Example usage
void main() async {
  final client = EthereumClient('https://mainnet.infura.io/v3/YOUR_KEY');
  final wallet = WalletManager(client);

  try {
    // Get current block
    final blockNumber = await client.getBlockNumber();
    print('Current block: $blockNumber');

    // Get balance
    const vitalikAddress = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045';
    final balance = await client.getBalanceEth(vitalikAddress);
    print('Vitalik\'s balance: $balance ETH');

    // Get gas price
    final gasPrice = await client.getGasPriceGwei();
    print('Gas price: $gasPrice Gwei');

    // Check multiple balances
    final addresses = [
      '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
      '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
      '0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8',
    ];

    final balances = await wallet.getMultipleBalances(addresses);
    balances.forEach((address, bal) {
      print('$address: $bal ETH');
    });

    // Find richest wallet
    final richest = await wallet.findRichestWallet(addresses);
    if (richest != null) {
      print('Richest wallet: ${richest.key} with ${richest.value} ETH');
    }
  } catch (e) {
    print('Error: $e');
  } finally {
    client.dispose();
  }
}
