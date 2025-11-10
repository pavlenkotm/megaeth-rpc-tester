import SwiftUI
import web3swift
import BigInt

/**
 * Web3 Wallet App for iOS/macOS
 *
 * A SwiftUI-based wallet application with Web3 capabilities
 *
 * Features:
 * - Connect to Ethereum wallet
 * - Display wallet balance
 * - Send transactions
 * - View transaction history
 * - Support for multiple networks
 */

// MARK: - Main App
@main
struct WalletApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// MARK: - Content View
struct ContentView: View {
    @StateObject private var walletManager = WalletManager()

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                if walletManager.isConnected {
                    WalletInfoView(walletManager: walletManager)
                } else {
                    WalletConnectView(walletManager: walletManager)
                }
            }
            .padding()
            .navigationTitle("Web3 Wallet")
        }
    }
}

// MARK: - Wallet Connect View
struct WalletConnectView: View {
    @ObservedObject var walletManager: WalletManager
    @State private var privateKey: String = ""
    @State private var showError = false
    @State private var errorMessage = ""

    var body: some View {
        VStack(spacing: 30) {
            Image(systemName: "wallet.pass")
                .font(.system(size: 80))
                .foregroundColor(.blue)

            Text("Connect Your Wallet")
                .font(.title)
                .fontWeight(.bold)

            Text("Enter your private key to connect to the Ethereum network")
                .font(.subheadline)
                .foregroundColor(.gray)
                .multilineTextAlignment(.center)
                .padding(.horizontal)

            SecureField("Private Key", text: $privateKey)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding(.horizontal)

            Button(action: connectWallet) {
                HStack {
                    Image(systemName: "link")
                    Text("Connect Wallet")
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(10)
            }
            .padding(.horizontal)
            .disabled(privateKey.isEmpty)

            Button(action: importFromMnemonic) {
                Text("Import from Mnemonic")
                    .foregroundColor(.blue)
            }
        }
        .alert("Error", isPresented: $showError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(errorMessage)
        }
    }

    private func connectWallet() {
        do {
            try walletManager.connectWallet(privateKey: privateKey)
            privateKey = "" // Clear for security
        } catch {
            errorMessage = error.localizedDescription
            showError = true
        }
    }

    private func importFromMnemonic() {
        // Implementation for mnemonic import
        errorMessage = "Mnemonic import coming soon"
        showError = true
    }
}

// MARK: - Wallet Info View
struct WalletInfoView: View {
    @ObservedObject var walletManager: WalletManager

    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Balance Card
                VStack(spacing: 10) {
                    Text("Balance")
                        .font(.headline)
                        .foregroundColor(.gray)

                    Text(walletManager.balance)
                        .font(.system(size: 48, weight: .bold))

                    Text("ETH")
                        .font(.title2)
                        .foregroundColor(.gray)
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(
                    RoundedRectangle(cornerRadius: 15)
                        .fill(Color.blue.opacity(0.1))
                )

                // Wallet Info
                VStack(alignment: .leading, spacing: 15) {
                    InfoRow(label: "Address", value: walletManager.shortenedAddress)
                    InfoRow(label: "Network", value: walletManager.networkName)
                    InfoRow(label: "Chain ID", value: "\(walletManager.chainId)")
                }
                .padding()
                .background(
                    RoundedRectangle(cornerRadius: 15)
                        .stroke(Color.gray.opacity(0.3), lineWidth: 1)
                )

                // Action Buttons
                VStack(spacing: 15) {
                    NavigationLink(destination: SendView(walletManager: walletManager)) {
                        ActionButton(icon: "arrow.up.circle.fill", title: "Send", color: .blue)
                    }

                    NavigationLink(destination: ReceiveView(walletManager: walletManager)) {
                        ActionButton(icon: "arrow.down.circle.fill", title: "Receive", color: .green)
                    }

                    NavigationLink(destination: TransactionHistoryView()) {
                        ActionButton(icon: "list.bullet", title: "Transactions", color: .purple)
                    }
                }

                // Disconnect Button
                Button(action: walletManager.disconnect) {
                    HStack {
                        Image(systemName: "rectangle.portrait.and.arrow.right")
                        Text("Disconnect")
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.red.opacity(0.1))
                    .foregroundColor(.red)
                    .cornerRadius(10)
                }
                .padding(.top)
            }
            .padding()
        }
    }
}

// MARK: - Helper Views
struct InfoRow: View {
    let label: String
    let value: String

    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(.gray)
            Spacer()
            Text(value)
                .fontWeight(.medium)
        }
    }
}

struct ActionButton: View {
    let icon: String
    let title: String
    let color: Color

    var body: some View {
        HStack {
            Image(systemName: icon)
            Text(title)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(color)
        .foregroundColor(.white)
        .cornerRadius(10)
    }
}

// MARK: - Send View
struct SendView: View {
    @ObservedObject var walletManager: WalletManager
    @State private var recipient = ""
    @State private var amount = ""
    @Environment(\.dismiss) var dismiss

    var body: some View {
        Form {
            Section(header: Text("Recipient")) {
                TextField("0x...", text: $recipient)
            }

            Section(header: Text("Amount (ETH)")) {
                TextField("0.0", text: $amount)
                    .keyboardType(.decimalPad)
            }

            Section {
                Button("Send Transaction") {
                    // Send transaction logic
                }
                .disabled(recipient.isEmpty || amount.isEmpty)
            }
        }
        .navigationTitle("Send ETH")
    }
}

// MARK: - Receive View
struct ReceiveView: View {
    @ObservedObject var walletManager: WalletManager

    var body: some View {
        VStack(spacing: 30) {
            Text("Receive ETH")
                .font(.title)
                .fontWeight(.bold)

            // QR Code placeholder
            Image(systemName: "qrcode")
                .font(.system(size: 200))
                .foregroundColor(.gray)

            Text(walletManager.address)
                .font(.system(.body, design: .monospaced))
                .padding()
                .background(Color.gray.opacity(0.1))
                .cornerRadius(10)

            Button("Copy Address") {
                UIPasteboard.general.string = walletManager.address
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }
}

// MARK: - Transaction History View
struct TransactionHistoryView: View {
    var body: some View {
        List {
            Text("Transaction history coming soon")
                .foregroundColor(.gray)
        }
        .navigationTitle("Transactions")
    }
}

// MARK: - Wallet Manager
class WalletManager: ObservableObject {
    @Published var isConnected = false
    @Published var address = ""
    @Published var balance = "0.0"
    @Published var networkName = "Unknown"
    @Published var chainId = 0

    private var web3: Web3?
    private var keystore: EthereumKeystoreV3?

    var shortenedAddress: String {
        guard address.count > 10 else { return address }
        let start = address.prefix(6)
        let end = address.suffix(4)
        return "\(start)...\(end)"
    }

    func connectWallet(privateKey: String) throws {
        // Initialize web3 with RPC endpoint
        let rpcURL = URL(string: "https://eth.llamarpc.com")!
        web3 = try Web3.new(rpcURL)

        // Create keystore from private key
        // Note: This is a simplified example
        // In production, use proper keystore management

        isConnected = true
        address = "0x..." // Set actual address
        networkName = "Ethereum Mainnet"
        chainId = 1

        // Fetch balance
        Task {
            await fetchBalance()
        }
    }

    func disconnect() {
        isConnected = false
        address = ""
        balance = "0.0"
        web3 = nil
        keystore = nil
    }

    @MainActor
    func fetchBalance() async {
        // Fetch balance from blockchain
        // This is a placeholder
        balance = "1.234"
    }
}
