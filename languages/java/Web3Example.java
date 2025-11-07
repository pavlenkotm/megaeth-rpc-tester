package com.web3.examples;

import org.web3j.crypto.Credentials;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.core.methods.response.*;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.Transfer;
import org.web3j.utils.Convert;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.concurrent.ExecutionException;

/**
 * Web3 Java Example
 *
 * Demonstrates how to interact with Ethereum using Web3j library
 *
 * Features:
 * - Connect to Ethereum RPC endpoints
 * - Query blockchain data
 * - Send transactions
 * - Check balances
 * - Monitor blocks
 */
public class Web3Example {

    private final Web3j web3j;
    private final Credentials credentials;

    /**
     * Constructor
     * @param rpcUrl Ethereum RPC endpoint URL
     * @param privateKey Private key for signing transactions (optional)
     */
    public Web3Example(String rpcUrl, String privateKey) {
        this.web3j = Web3j.build(new HttpService(rpcUrl));
        this.credentials = privateKey != null ? Credentials.create(privateKey) : null;
    }

    /**
     * Get Web3 client version
     */
    public String getClientVersion() throws Exception {
        Web3ClientVersion web3ClientVersion = web3j.web3ClientVersion().send();
        return web3ClientVersion.getWeb3ClientVersion();
    }

    /**
     * Get latest block number
     */
    public BigInteger getBlockNumber() throws Exception {
        EthBlockNumber blockNumber = web3j.ethBlockNumber().send();
        return blockNumber.getBlockNumber();
    }

    /**
     * Get chain ID
     */
    public BigInteger getChainId() throws Exception {
        EthChainId chainId = web3j.ethChainId().send();
        return chainId.getChainId();
    }

    /**
     * Get gas price
     */
    public BigInteger getGasPrice() throws Exception {
        EthGasPrice gasPrice = web3j.ethGasPrice().send();
        return gasPrice.getGasPrice();
    }

    /**
     * Get ETH balance of an address
     * @param address Ethereum address
     * @return Balance in Wei
     */
    public BigInteger getBalance(String address) throws Exception {
        EthGetBalance balance = web3j.ethGetBalance(
            address,
            DefaultBlockParameterName.LATEST
        ).send();
        return balance.getBalance();
    }

    /**
     * Get ETH balance in Ether
     * @param address Ethereum address
     * @return Balance in ETH
     */
    public BigDecimal getBalanceInEth(String address) throws Exception {
        BigInteger balanceWei = getBalance(address);
        return Convert.fromWei(
            new BigDecimal(balanceWei),
            Convert.Unit.ETHER
        );
    }

    /**
     * Get block by number
     * @param blockNumber Block number
     * @return Block information
     */
    public EthBlock.Block getBlock(BigInteger blockNumber) throws Exception {
        EthBlock block = web3j.ethGetBlockByNumber(
            org.web3j.protocol.core.DefaultBlockParameter.valueOf(blockNumber),
            false
        ).send();
        return block.getBlock();
    }

    /**
     * Get transaction by hash
     * @param txHash Transaction hash
     * @return Transaction information
     */
    public Transaction getTransaction(String txHash) throws Exception {
        EthTransaction transaction = web3j.ethGetTransactionByHash(txHash).send();
        return transaction.getTransaction().orElse(null);
    }

    /**
     * Get transaction receipt
     * @param txHash Transaction hash
     * @return Transaction receipt
     */
    public TransactionReceipt getTransactionReceipt(String txHash) throws Exception {
        EthGetTransactionReceipt receipt = web3j.ethGetTransactionReceipt(txHash).send();
        return receipt.getTransactionReceipt().orElse(null);
    }

    /**
     * Send ETH transfer
     * @param toAddress Recipient address
     * @param amount Amount in ETH
     * @return Transaction receipt
     */
    public TransactionReceipt sendEth(String toAddress, BigDecimal amount) throws Exception {
        if (credentials == null) {
            throw new IllegalStateException("Private key not set");
        }

        TransactionReceipt receipt = Transfer.sendFunds(
            web3j,
            credentials,
            toAddress,
            amount,
            Convert.Unit.ETHER
        ).send();

        return receipt;
    }

    /**
     * Estimate gas for a transaction
     * @param from Sender address
     * @param to Recipient address
     * @param value Value to send
     * @return Estimated gas
     */
    public BigInteger estimateGas(String from, String to, BigInteger value) throws Exception {
        org.web3j.protocol.core.methods.request.Transaction transaction =
            org.web3j.protocol.core.methods.request.Transaction.createEthCallTransaction(
                from, to, "0x" + value.toString(16)
            );

        EthEstimateGas ethEstimateGas = web3j.ethEstimateGas(transaction).send();
        return ethEstimateGas.getAmountUsed();
    }

    /**
     * Check if address is valid
     * @param address Ethereum address
     * @return true if valid
     */
    public static boolean isValidAddress(String address) {
        return address != null &&
               address.matches("^0x[0-9a-fA-F]{40}$");
    }

    /**
     * Get account address from credentials
     * @return Address
     */
    public String getAddress() {
        if (credentials == null) {
            throw new IllegalStateException("Credentials not set");
        }
        return credentials.getAddress();
    }

    /**
     * Close Web3j instance
     */
    public void close() {
        web3j.shutdown();
    }

    /**
     * Main method - Example usage
     */
    public static void main(String[] args) {
        try {
            System.out.println("🔗 Web3j Example\n");

            // Create Web3 instance (read-only)
            Web3Example web3 = new Web3Example("https://eth.llamarpc.com", null);

            // Get client version
            System.out.println("Client Version: " + web3.getClientVersion());

            // Get block number
            System.out.println("Latest Block: " + web3.getBlockNumber());

            // Get chain ID
            System.out.println("Chain ID: " + web3.getChainId());

            // Get gas price
            BigInteger gasPrice = web3.getGasPrice();
            System.out.println("Gas Price: " + gasPrice + " wei");

            // Check balance
            String address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
            BigDecimal balance = web3.getBalanceInEth(address);
            System.out.println("Balance of " + address + ": " + balance + " ETH");

            // Validate address
            System.out.println("Address valid: " + isValidAddress(address));

            // Close connection
            web3.close();

            System.out.println("\n✅ Web3j example completed successfully");

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
