import org.web3j.protocol.Web3j
import org.web3j.protocol.http.HttpService
import org.web3j.protocol.core.methods.response._
import org.web3j.crypto.Credentials
import org.web3j.utils.Convert
import cats.effect._
import cats.implicits._
import java.math.{BigDecimal, BigInteger}
import scala.concurrent.ExecutionContext
import scala.util.{Try, Success, Failure}

/**
 * Functional Web3 Client using Cats Effect
 */
class EthereumClient(rpcUrl: String)(implicit cs: ContextShift[IO]) {
  private val web3j: Web3j = Web3j.build(new HttpService(rpcUrl))

  /**
   * Get current block number
   */
  def getBlockNumber: IO[BigInteger] = IO.fromTry(
    Try(web3j.ethBlockNumber().send().getBlockNumber)
  )

  /**
   * Get balance for an address
   */
  def getBalance(address: String): IO[BigDecimal] = IO.fromTry(
    Try {
      val balance = web3j.ethGetBalance(
        address,
        org.web3j.protocol.core.DefaultBlockParameterName.LATEST
      ).send().getBalance

      Convert.fromWei(new BigDecimal(balance), Convert.Unit.ETHER)
    }
  )

  /**
   * Get transaction by hash
   */
  def getTransaction(txHash: String): IO[Option[EthTransaction.Transaction]] = IO.fromTry(
    Try {
      val result = web3j.ethGetTransactionByHash(txHash).send()
      if (result.getTransaction.isPresent) {
        Some(result.getTransaction.get())
      } else {
        None
      }
    }
  )

  /**
   * Get gas price
   */
  def getGasPrice: IO[BigInteger] = IO.fromTry(
    Try(web3j.ethGasPrice().send().getGasPrice)
  )

  /**
   * Estimate gas for transaction
   */
  def estimateGas(from: String, to: String, data: String): IO[BigInteger] = IO.fromTry(
    Try {
      val transaction = org.web3j.protocol.core.methods.request.Transaction.createFunctionCallTransaction(
        from, null, null, null, to, data
      )
      web3j.ethEstimateGas(transaction).send().getAmountUsed
    }
  )

  /**
   * Get block by number
   */
  def getBlock(blockNumber: BigInteger): IO[Option[EthBlock.Block]] = IO.fromTry(
    Try {
      val result = web3j.ethGetBlockByNumber(
        org.web3j.protocol.core.DefaultBlockParameter.valueOf(blockNumber),
        false
      ).send()

      if (result.getBlock != null) Some(result.getBlock) else None
    }
  )

  def shutdown(): IO[Unit] = IO(web3j.shutdown())
}

/**
 * Functional Wallet
 */
case class Wallet(address: String, balance: BigDecimal)

object Wallet {
  def fromAddress(address: String)(implicit client: EthereumClient): IO[Wallet] =
    client.getBalance(address).map(balance => Wallet(address, balance))

  def fromAddresses(addresses: List[String])(implicit client: EthereumClient): IO[List[Wallet]] =
    addresses.parTraverse(fromAddress)
}

/**
 * Blockchain Explorer
 */
trait BlockchainExplorer {
  def getLatestBlocks(count: Int): IO[List[BigInteger]]
  def getBlockTransactions(blockNumber: BigInteger): IO[List[String]]
  def analyzeGasPrice: IO[GasAnalysis]
}

case class GasAnalysis(
  currentPrice: BigInteger,
  avgPrice: BigInteger,
  recommendation: String
)

class EthereumExplorer(implicit client: EthereumClient, cs: ContextShift[IO]) extends BlockchainExplorer {

  override def getLatestBlocks(count: Int): IO[List[BigInteger]] = for {
    current <- client.getBlockNumber
    blocks = (0 until count).map(i => current.subtract(BigInteger.valueOf(i.toLong))).toList
  } yield blocks

  override def getBlockTransactions(blockNumber: BigInteger): IO[List[String]] =
    client.getBlock(blockNumber).map {
      case Some(block) => block.getTransactions.asScala.map(_.get().asInstanceOf[String]).toList
      case None => List.empty
    }

  override def analyzeGasPrice: IO[GasAnalysis] = for {
    currentPrice <- client.getGasPrice
    recommendation = if (currentPrice.compareTo(BigInteger.valueOf(50_000_000_000L)) > 0)
      "Gas price is high. Consider waiting."
    else
      "Gas price is normal."
  } yield GasAnalysis(currentPrice, currentPrice, recommendation)
}

/**
 * Token Balance Service
 */
object TokenService {

  def checkMultipleBalances(addresses: List[String])(implicit client: EthereumClient): IO[Map[String, BigDecimal]] =
    addresses.parTraverse { address =>
      client.getBalance(address).map(balance => address -> balance)
    }.map(_.toMap)

  def findRichestWallet(addresses: List[String])(implicit client: EthereumClient): IO[Option[Wallet]] =
    Wallet.fromAddresses(addresses).map { wallets =>
      wallets.maxByOption(_.balance)
    }
}

/**
 * Main application
 */
object Web3App extends IOApp {

  override def run(args: List[String]): IO[ExitCode] = {
    implicit val client: EthereumClient = new EthereumClient("https://mainnet.infura.io/v3/YOUR_KEY")

    val program = for {
      // Get current block
      blockNumber <- client.getBlockNumber
      _ <- IO(println(s"Current block: $blockNumber"))

      // Get balance
      vitalikAddress = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
      balance <- client.getBalance(vitalikAddress)
      _ <- IO(println(s"Vitalik's balance: $balance ETH"))

      // Gas analysis
      explorer = new EthereumExplorer
      gasAnalysis <- explorer.analyzeGasPrice
      _ <- IO(println(s"Gas price: ${Convert.fromWei(new BigDecimal(gasAnalysis.currentPrice), Convert.Unit.GWEI)} Gwei"))
      _ <- IO(println(s"Recommendation: ${gasAnalysis.recommendation}"))

      // Check multiple balances
      addresses = List(
        "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
        "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
      )

      richest <- TokenService.findRichestWallet(addresses)
      _ <- IO(println(s"Richest wallet: ${richest.map(w => s"${w.address} with ${w.balance} ETH")}"))

      // Cleanup
      _ <- client.shutdown()
    } yield ()

    program.as(ExitCode.Success).handleErrorWith { e =>
      IO(println(s"Error: ${e.getMessage}")).as(ExitCode.Error)
    }
  }
}
