package com.web3.api

import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.plugins.contentnegotiation.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import org.web3j.protocol.Web3j
import org.web3j.protocol.http.HttpService
import org.web3j.protocol.core.DefaultBlockParameterName
import java.math.BigInteger
import java.math.BigDecimal

/**
 * Blockchain API Server
 *
 * A Ktor-based REST API for Ethereum blockchain interactions
 *
 * Features:
 * - RESTful endpoints for blockchain queries
 * - JSON serialization
 * - Web3j integration
 * - CORS support
 * - Error handling
 *
 * Endpoints:
 * - GET /api/v1/block/latest - Get latest block number
 * - GET /api/v1/balance/{address} - Get ETH balance
 * - GET /api/v1/gas-price - Get current gas price
 * - GET /api/v1/network - Get network info
 * - GET /api/v1/transaction/{hash} - Get transaction details
 */

// MARK: - Data Models
@Serializable
data class BlockResponse(
    val number: String,
    val hash: String?,
    val timestamp: String?,
    val transactionCount: Int?
)

@Serializable
data class BalanceResponse(
    val address: String,
    val balanceWei: String,
    val balanceEth: String
)

@Serializable
data class GasPriceResponse(
    val gasPriceWei: String,
    val gasPriceGwei: String
)

@Serializable
data class NetworkResponse(
    val chainId: String,
    val clientVersion: String,
    val blockNumber: String
)

@Serializable
data class TransactionResponse(
    val hash: String,
    val from: String?,
    val to: String?,
    val value: String?,
    val gasPrice: String?,
    val gas: String?,
    val blockNumber: String?,
    val status: String?
)

@Serializable
data class ErrorResponse(
    val error: String,
    val message: String
)

// MARK: - Blockchain Service
class BlockchainService(rpcUrl: String) {
    private val web3j = Web3j.build(HttpService(rpcUrl))

    fun getLatestBlockNumber(): BigInteger {
        return web3j.ethBlockNumber().send().blockNumber
    }

    fun getBlock(blockNumber: BigInteger): BlockResponse {
        val block = web3j.ethGetBlockByNumber(
            org.web3j.protocol.core.DefaultBlockParameter.valueOf(blockNumber),
            false
        ).send().block

        return BlockResponse(
            number = block.number.toString(),
            hash = block.hash,
            timestamp = block.timestamp.toString(),
            transactionCount = block.transactions?.size
        )
    }

    fun getBalance(address: String): BalanceResponse {
        val balanceWei = web3j.ethGetBalance(
            address,
            DefaultBlockParameterName.LATEST
        ).send().balance

        val balanceEth = org.web3j.utils.Convert.fromWei(
            BigDecimal(balanceWei),
            org.web3j.utils.Convert.Unit.ETHER
        )

        return BalanceResponse(
            address = address,
            balanceWei = balanceWei.toString(),
            balanceEth = balanceEth.toString()
        )
    }

    fun getGasPrice(): GasPriceResponse {
        val gasPriceWei = web3j.ethGasPrice().send().gasPrice

        val gasPriceGwei = org.web3j.utils.Convert.fromWei(
            BigDecimal(gasPriceWei),
            org.web3j.utils.Convert.Unit.GWEI
        )

        return GasPriceResponse(
            gasPriceWei = gasPriceWei.toString(),
            gasPriceGwei = gasPriceGwei.toString()
        )
    }

    fun getNetworkInfo(): NetworkResponse {
        val chainId = web3j.ethChainId().send().chainId
        val clientVersion = web3j.web3ClientVersion().send().web3ClientVersion
        val blockNumber = web3j.ethBlockNumber().send().blockNumber

        return NetworkResponse(
            chainId = chainId.toString(),
            clientVersion = clientVersion,
            blockNumber = blockNumber.toString()
        )
    }

    fun getTransaction(hash: String): TransactionResponse? {
        val tx = web3j.ethGetTransactionByHash(hash).send().transaction.orElse(null)
            ?: return null

        val receipt = web3j.ethGetTransactionReceipt(hash).send().transactionReceipt.orElse(null)

        return TransactionResponse(
            hash = tx.hash,
            from = tx.from,
            to = tx.to,
            value = tx.value?.toString(),
            gasPrice = tx.gasPrice?.toString(),
            gas = tx.gas?.toString(),
            blockNumber = tx.blockNumber?.toString(),
            status = receipt?.status
        )
    }

    fun close() {
        web3j.shutdown()
    }
}

// MARK: - Application Configuration
fun Application.module() {
    // Configure JSON serialization
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
        })
    }

    // Initialize blockchain service
    val blockchainService = BlockchainService("https://eth.llamarpc.com")

    routing {
        route("/api/v1") {
            // Health check
            get("/health") {
                call.respond(HttpStatusCode.OK, mapOf("status" to "healthy"))
            }

            // Get latest block
            get("/block/latest") {
                try {
                    val blockNumber = blockchainService.getLatestBlockNumber()
                    val block = blockchainService.getBlock(blockNumber)
                    call.respond(HttpStatusCode.OK, block)
                } catch (e: Exception) {
                    call.respond(
                        HttpStatusCode.InternalServerError,
                        ErrorResponse("BLOCKCHAIN_ERROR", e.message ?: "Unknown error")
                    )
                }
            }

            // Get balance
            get("/balance/{address}") {
                val address = call.parameters["address"]
                if (address == null) {
                    call.respond(
                        HttpStatusCode.BadRequest,
                        ErrorResponse("INVALID_REQUEST", "Address parameter is required")
                    )
                    return@get
                }

                try {
                    val balance = blockchainService.getBalance(address)
                    call.respond(HttpStatusCode.OK, balance)
                } catch (e: Exception) {
                    call.respond(
                        HttpStatusCode.InternalServerError,
                        ErrorResponse("BLOCKCHAIN_ERROR", e.message ?: "Unknown error")
                    )
                }
            }

            // Get gas price
            get("/gas-price") {
                try {
                    val gasPrice = blockchainService.getGasPrice()
                    call.respond(HttpStatusCode.OK, gasPrice)
                } catch (e: Exception) {
                    call.respond(
                        HttpStatusCode.InternalServerError,
                        ErrorResponse("BLOCKCHAIN_ERROR", e.message ?: "Unknown error")
                    )
                }
            }

            // Get network info
            get("/network") {
                try {
                    val network = blockchainService.getNetworkInfo()
                    call.respond(HttpStatusCode.OK, network)
                } catch (e: Exception) {
                    call.respond(
                        HttpStatusCode.InternalServerError,
                        ErrorResponse("BLOCKCHAIN_ERROR", e.message ?: "Unknown error")
                    )
                }
            }

            // Get transaction
            get("/transaction/{hash}") {
                val hash = call.parameters["hash"]
                if (hash == null) {
                    call.respond(
                        HttpStatusCode.BadRequest,
                        ErrorResponse("INVALID_REQUEST", "Transaction hash is required")
                    )
                    return@get
                }

                try {
                    val transaction = blockchainService.getTransaction(hash)
                    if (transaction != null) {
                        call.respond(HttpStatusCode.OK, transaction)
                    } else {
                        call.respond(
                            HttpStatusCode.NotFound,
                            ErrorResponse("NOT_FOUND", "Transaction not found")
                        )
                    }
                } catch (e: Exception) {
                    call.respond(
                        HttpStatusCode.InternalServerError,
                        ErrorResponse("BLOCKCHAIN_ERROR", e.message ?: "Unknown error")
                    )
                }
            }
        }
    }

    // Shutdown hook
    environment.monitor.subscribe(ApplicationStopped) {
        blockchainService.close()
    }
}

// MARK: - Main
fun main() {
    embeddedServer(Netty, port = 8080, host = "0.0.0.0") {
        module()
    }.start(wait = true)

    println("""
        ╔════════════════════════════════════════╗
        ║   🔗 Blockchain API Server Started    ║
        ║                                        ║
        ║   Port: 8080                          ║
        ║   Endpoints:                          ║
        ║   - GET /api/v1/health                ║
        ║   - GET /api/v1/block/latest          ║
        ║   - GET /api/v1/balance/{address}     ║
        ║   - GET /api/v1/gas-price             ║
        ║   - GET /api/v1/network               ║
        ║   - GET /api/v1/transaction/{hash}    ║
        ╚════════════════════════════════════════╝
    """.trimIndent())
}
