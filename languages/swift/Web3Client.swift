import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif

/**
 * Ethereum Web3 Client for Swift
 * Supports async/await for modern iOS/macOS development
 */

// MARK: - Data Types

struct EthereumAddress: Codable {
    let value: String

    var checksummed: String {
        // Simplified checksum implementation
        return value
    }
}

struct TransactionHash: Codable {
    let value: String
}

struct Wei: Codable {
    let value: String

    func toEther() -> Double {
        guard let weiValue = Double(value) else { return 0 }
        return weiValue / 1_000_000_000_000_000_000
    }
}

struct BlockNumber: Codable {
    let value: UInt64
}

// MARK: - RPC Request/Response

struct JSONRPCRequest: Codable {
    let jsonrpc: String = "2.0"
    let id: Int
    let method: String
    let params: [String]
}

struct JSONRPCResponse<T: Codable>: Codable {
    let jsonrpc: String
    let id: Int
    let result: T?
    let error: JSONRPCError?
}

struct JSONRPCError: Codable {
    let code: Int
    let message: String
}

// MARK: - Ethereum Client

@available(macOS 12.0, iOS 15.0, *)
class EthereumClient {
    private let rpcURL: URL
    private let session: URLSession

    init(rpcURL: String) {
        self.rpcURL = URL(string: rpcURL)!
        self.session = URLSession.shared
    }

    // MARK: - Public Methods

    /**
     * Get current block number
     */
    func getBlockNumber() async throws -> UInt64 {
        let response: JSONRPCResponse<String> = try await call(
            method: "eth_blockNumber",
            params: []
        )

        guard let result = response.result else {
            throw Web3Error.invalidResponse
        }

        return UInt64(result.dropFirst(2), radix: 16) ?? 0
    }

    /**
     * Get ETH balance for address
     */
    func getBalance(address: String) async throws -> Wei {
        let response: JSONRPCResponse<String> = try await call(
            method: "eth_getBalance",
            params: [address, "latest"]
        )

        guard let result = response.result else {
            throw Web3Error.invalidResponse
        }

        return Wei(value: String(UInt64(result.dropFirst(2), radix: 16) ?? 0))
    }

    /**
     * Get transaction by hash
     */
    func getTransaction(hash: String) async throws -> Transaction? {
        let response: JSONRPCResponse<Transaction> = try await call(
            method: "eth_getTransactionByHash",
            params: [hash]
        )

        return response.result
    }

    /**
     * Get gas price
     */
    func getGasPrice() async throws -> Wei {
        let response: JSONRPCResponse<String> = try await call(
            method: "eth_gasPrice",
            params: []
        )

        guard let result = response.result else {
            throw Web3Error.invalidResponse
        }

        return Wei(value: String(UInt64(result.dropFirst(2), radix: 16) ?? 0))
    }

    /**
     * Send raw transaction
     */
    func sendRawTransaction(signedTx: String) async throws -> TransactionHash {
        let response: JSONRPCResponse<String> = try await call(
            method: "eth_sendRawTransaction",
            params: [signedTx]
        )

        guard let result = response.result else {
            throw Web3Error.transactionFailed
        }

        return TransactionHash(value: result)
    }

    /**
     * Call contract method (read-only)
     */
    func call(to: String, data: String) async throws -> String {
        let params = [
            [
                "to": to,
                "data": data
            ],
            "latest"
        ]

        let response: JSONRPCResponse<String> = try await callWithDictParams(
            method: "eth_call",
            params: params
        )

        guard let result = response.result else {
            throw Web3Error.contractCallFailed
        }

        return result
    }

    // MARK: - Private Methods

    private func call<T: Codable>(
        method: String,
        params: [String]
    ) async throws -> JSONRPCResponse<T> {
        let request = JSONRPCRequest(
            id: 1,
            method: method,
            params: params
        )

        var urlRequest = URLRequest(url: rpcURL)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        urlRequest.httpBody = try JSONEncoder().encode(request)

        let (data, _) = try await session.data(for: urlRequest)
        let response = try JSONDecoder().decode(JSONRPCResponse<T>.self, from: data)

        if let error = response.error {
            throw Web3Error.rpcError(code: error.code, message: error.message)
        }

        return response
    }

    private func callWithDictParams<T: Codable>(
        method: String,
        params: [[String: String]]
    ) async throws -> JSONRPCResponse<T> {
        // Simplified implementation - would need proper JSON encoding
        return try await call(method: method, params: [])
    }
}

// MARK: - Transaction Model

struct Transaction: Codable {
    let hash: String
    let from: String
    let to: String?
    let value: String
    let gas: String
    let gasPrice: String
    let nonce: String
    let input: String
    let blockNumber: String?
}

// MARK: - Errors

enum Web3Error: Error {
    case invalidResponse
    case transactionFailed
    case contractCallFailed
    case rpcError(code: Int, message: String)
}

// MARK: - Wallet Manager

@available(macOS 12.0, iOS 15.0, *)
class WalletManager {
    private let client: EthereumClient

    init(rpcURL: String) {
        self.client = EthereumClient(rpcURL: rpcURL)
    }

    /**
     * Get wallet balance in ETH
     */
    func getWalletBalance(address: String) async throws -> Double {
        let wei = try await client.getBalance(address: address)
        return wei.toEther()
    }

    /**
     * Monitor multiple wallets
     */
    func getMultipleBalances(addresses: [String]) async throws -> [String: Double] {
        var balances: [String: Double] = [:]

        for address in addresses {
            let balance = try await getWalletBalance(address: address)
            balances[address] = balance
        }

        return balances
    }

    /**
     * Get current network gas price in Gwei
     */
    func getGasPriceGwei() async throws -> Double {
        let gasPrice = try await client.getGasPrice()
        return gasPrice.toEther() * 1_000_000_000
    }
}

// MARK: - Example Usage

@available(macOS 12.0, iOS 15.0, *)
@main
struct Web3App {
    static func main() async {
        let client = EthereumClient(rpcURL: "https://mainnet.infura.io/v3/YOUR_KEY")
        let wallet = WalletManager(rpcURL: "https://mainnet.infura.io/v3/YOUR_KEY")

        do {
            // Get block number
            let blockNumber = try await client.getBlockNumber()
            print("Current block: \\(blockNumber)")

            // Get balance
            let vitalikAddress = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
            let balance = try await wallet.getWalletBalance(address: vitalikAddress)
            print("Vitalik's balance: \\(balance) ETH")

            // Get gas price
            let gasPrice = try await wallet.getGasPriceGwei()
            print("Gas price: \\(gasPrice) Gwei")

            // Check multiple balances
            let addresses = [
                "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
                "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
                "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
            ]

            let balances = try await wallet.getMultipleBalances(addresses: addresses)
            for (address, bal) in balances {
                print("\\(address): \\(bal) ETH")
            }

        } catch {
            print("Error: \\(error)")
        }
    }
}
