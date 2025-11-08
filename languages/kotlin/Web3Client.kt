import kotlinx.coroutines.*
import org.web3j.protocol.Web3j
import org.web3j.protocol.http.HttpService
import org.web3j.protocol.core.methods.response.*
import org.web3j.crypto.Credentials
import org.web3j.tx.gas.DefaultGasProvider
import org.web3j.utils.Convert
import java.math.BigDecimal
import java.math.BigInteger

/**
 * Modern Kotlin Web3 Client
 * Demonstrates coroutine-based async Ethereum interaction
 */
class EthereumClient(private val rpcUrl: String) {
    private val web3j: Web3j = Web3j.build(HttpService(rpcUrl))

    /**
     * Get current block number
     */
    suspend fun getBlockNumber(): BigInteger = withContext(Dispatchers.IO) {
        web3j.ethBlockNumber().send().blockNumber
    }

    /**
     * Get ETH balance for an address
     */
    suspend fun getBalance(address: String): BigDecimal = withContext(Dispatchers.IO) {
        val balance = web3j.ethGetBalance(address, org.web3j.protocol.core.DefaultBlockParameterName.LATEST)
            .send()
            .balance
        Convert.fromWei(balance.toBigDecimal(), Convert.Unit.ETHER)
    }

    /**
     * Get transaction by hash
     */
    suspend fun getTransaction(txHash: String): org.web3j.protocol.core.methods.response.Transaction? =
        withContext(Dispatchers.IO) {
            web3j.ethGetTransactionByHash(txHash).send().transaction.orElse(null)
        }

    /**
     * Send ETH transaction
     */
    suspend fun sendTransaction(
        credentials: Credentials,
        toAddress: String,
        amount: BigDecimal
    ): String = withContext(Dispatchers.IO) {
        val amountWei = Convert.toWei(amount, Convert.Unit.ETHER).toBigInteger()

        val transactionReceipt = org.web3j.tx.Transfer(web3j, credentials, DefaultGasProvider())
            .sendFunds(toAddress, amount, Convert.Unit.ETHER)
            .send()

        transactionReceipt.transactionHash
    }

    /**
     * Get gas price
     */
    suspend fun getGasPrice(): BigInteger = withContext(Dispatchers.IO) {
        web3j.ethGasPrice().send().gasPrice
    }

    /**
     * Estimate gas for a transaction
     */
    suspend fun estimateGas(
        from: String,
        to: String,
        data: String
    ): BigInteger = withContext(Dispatchers.IO) {
        val transaction = org.web3j.protocol.core.methods.request.Transaction.createFunctionCallTransaction(
            from, null, null, null, to, data
        )
        web3j.ethEstimateGas(transaction).send().amountUsed
    }

    /**
     * Monitor new blocks
     */
    fun observeBlocks() = flow {
        val subscription = web3j.blockFlowable(false)
        subscription.subscribe { block ->
            emit(block)
        }
    }

    fun close() {
        web3j.shutdown()
    }
}

/**
 * Smart Contract Interaction Helper
 */
data class ContractCall(
    val contractAddress: String,
    val functionName: String,
    val parameters: List<Any>
)

/**
 * Simple Token Balance Checker
 */
class TokenBalanceChecker(private val client: EthereumClient) {

    suspend fun checkMultipleBalances(addresses: List<String>): Map<String, BigDecimal> =
        coroutineScope {
            addresses.map { address ->
                async {
                    address to client.getBalance(address)
                }
            }.awaitAll().toMap()
        }
}

/**
 * Example usage
 */
fun main() = runBlocking {
    val client = EthereumClient("https://mainnet.infura.io/v3/YOUR_KEY")

    try {
        // Get current block
        val blockNumber = client.getBlockNumber()
        println("Current block: $blockNumber")

        // Get balance
        val vitalikAddress = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        val balance = client.getBalance(vitalikAddress)
        println("Vitalik's balance: $balance ETH")

        // Get gas price
        val gasPrice = client.getGasPrice()
        println("Current gas price: ${Convert.fromWei(gasPrice.toBigDecimal(), Convert.Unit.GWEI)} Gwei")

        // Check multiple balances concurrently
        val checker = TokenBalanceChecker(client)
        val addresses = listOf(
            "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
            "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
        )

        val balances = checker.checkMultipleBalances(addresses)
        balances.forEach { (address, bal) ->
            println("$address: $bal ETH")
        }

    } finally {
        client.close()
    }
}
