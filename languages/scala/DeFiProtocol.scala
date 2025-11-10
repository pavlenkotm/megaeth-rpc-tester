package com.web3.defi

import cats.effect._
import cats.effect.std.Console
import cats.syntax.all._
import org.web3j.protocol.Web3j
import org.web3j.protocol.http.HttpService
import org.web3j.protocol.core.DefaultBlockParameterName
import org.web3j.crypto.{Credentials, TransactionEncoder}
import org.web3j.utils.Convert
import scala.concurrent.duration._
import java.math.{BigDecimal, BigInteger}

/**
 * DeFi Protocol - Functional Scala Implementation
 *
 * A functional approach to DeFi protocol using Cats Effect
 *
 * Features:
 * - Pure functional programming
 * - Effect system with IO monad
 * - Resource safety
 * - Error handling with Either
 * - Concurrent operations
 * - Type-safe blockchain interactions
 *
 * Core Operations:
 * - Liquidity pool management
 * - Token swapping
 * - Yield farming
 * - Staking/Unstaking
 * - Price oracle integration
 */

// MARK: - Domain Models
sealed trait DeFiError
case class NetworkError(message: String) extends DeFiError
case class InsufficientBalance(required: BigInteger, available: BigInteger) extends DeFiError
case class InvalidAddress(address: String) extends DeFiError
case class TransactionFailed(reason: String) extends DeFiError

case class TokenAmount(amount: BigInteger, decimals: Int) {
  def toDecimal: BigDecimal =
    Convert.fromWei(new BigDecimal(amount), Convert.Unit.ETHER)

  def +(other: TokenAmount): TokenAmount =
    TokenAmount(amount.add(other.amount), decimals)

  def -(other: TokenAmount): Either[DeFiError, TokenAmount] =
    if (amount.compareTo(other.amount) >= 0)
      Right(TokenAmount(amount.subtract(other.amount), decimals))
    else
      Left(InsufficientBalance(other.amount, amount))
}

case class LiquidityPool(
  tokenA: String,
  tokenB: String,
  reserveA: TokenAmount,
  reserveB: TokenAmount,
  totalSupply: TokenAmount
) {
  def price: BigDecimal = {
    val a = reserveA.toDecimal
    val b = reserveB.toDecimal
    if (b.compareTo(BigDecimal.ZERO) == 0) BigDecimal.ZERO
    else a.divide(b, 18, BigDecimal.ROUND_HALF_UP)
  }

  def addLiquidity(amountA: TokenAmount, amountB: TokenAmount): Either[DeFiError, (LiquidityPool, TokenAmount)] = {
    val newReserveA = reserveA + amountA
    val newReserveB = reserveB + amountB

    val liquidity = if (totalSupply.amount == BigInteger.ZERO) {
      // Initial liquidity
      TokenAmount(
        amountA.amount.multiply(amountB.amount).sqrt,
        totalSupply.decimals
      )
    } else {
      // Proportional liquidity
      val liquidityA = amountA.amount.multiply(totalSupply.amount).divide(reserveA.amount)
      val liquidityB = amountB.amount.multiply(totalSupply.amount).divide(reserveB.amount)
      TokenAmount(liquidityA.min(liquidityB), totalSupply.decimals)
    }

    val newTotalSupply = totalSupply + liquidity
    val newPool = copy(
      reserveA = newReserveA,
      reserveB = newReserveB,
      totalSupply = newTotalSupply
    )

    Right((newPool, liquidity))
  }

  def swap(amountIn: TokenAmount, fromTokenA: Boolean): Either[DeFiError, (LiquidityPool, TokenAmount)] = {
    val (reserveIn, reserveOut) = if (fromTokenA) (reserveA, reserveB) else (reserveB, reserveA)

    // Apply 0.3% fee
    val amountInWithFee = amountIn.amount.multiply(BigInteger.valueOf(997))
    val numerator = amountInWithFee.multiply(reserveOut.amount)
    val denominator = reserveIn.amount.multiply(BigInteger.valueOf(1000)).add(amountInWithFee)
    val amountOut = TokenAmount(numerator.divide(denominator), reserveOut.decimals)

    val newReserveIn = reserveIn + amountIn
    val newReserveOut = reserveOut - amountOut match {
      case Right(reserve) => reserve
      case Left(err) => return Left(err)
    }

    val newPool = if (fromTokenA) {
      copy(reserveA = newReserveIn, reserveB = newReserveOut)
    } else {
      copy(reserveA = newReserveOut, reserveB = newReserveIn)
    }

    Right((newPool, amountOut))
  }
}

case class StakePosition(
  user: String,
  amount: TokenAmount,
  startBlock: BigInteger,
  rewardDebt: TokenAmount
)

case class FarmingPool(
  stakingToken: String,
  rewardToken: String,
  totalStaked: TokenAmount,
  rewardPerBlock: TokenAmount,
  lastRewardBlock: BigInteger,
  accRewardPerShare: BigInteger,
  positions: Map[String, StakePosition]
) {
  def stake(user: String, amount: TokenAmount, currentBlock: BigInteger): FarmingPool = {
    val updatedPool = updatePool(currentBlock)
    val position = positions.getOrElse(
      user,
      StakePosition(user, TokenAmount(BigInteger.ZERO, amount.decimals), currentBlock, TokenAmount(BigInteger.ZERO, amount.decimals))
    )

    val newAmount = position.amount + amount
    val newRewardDebt = TokenAmount(
      newAmount.amount.multiply(updatedPool.accRewardPerShare).divide(BigInteger.valueOf(1e12.toLong)),
      position.rewardDebt.decimals
    )

    val newPosition = position.copy(amount = newAmount, rewardDebt = newRewardDebt)

    updatedPool.copy(
      totalStaked = updatedPool.totalStaked + amount,
      positions = updatedPool.positions + (user -> newPosition)
    )
  }

  def updatePool(currentBlock: BigInteger): FarmingPool = {
    if (currentBlock.compareTo(lastRewardBlock) <= 0 || totalStaked.amount == BigInteger.ZERO) {
      return this
    }

    val blocks = currentBlock.subtract(lastRewardBlock)
    val reward = blocks.multiply(rewardPerBlock.amount)
    val newAccRewardPerShare = accRewardPerShare.add(
      reward.multiply(BigInteger.valueOf(1e12.toLong)).divide(totalStaked.amount)
    )

    copy(
      lastRewardBlock = currentBlock,
      accRewardPerShare = newAccRewardPerShare
    )
  }

  def pendingReward(user: String): TokenAmount = {
    positions.get(user).map { position =>
      val accReward = position.amount.amount.multiply(accRewardPerShare).divide(BigInteger.valueOf(1e12.toLong))
      TokenAmount(accReward.subtract(position.rewardDebt.amount), rewardToken.decimals)
    }.getOrElse(TokenAmount(BigInteger.ZERO, 18))
  }
}

// MARK: - DeFi Protocol Service
class DeFiProtocol(rpcUrl: String) {
  private val web3j = Web3j.build(new HttpService(rpcUrl))

  def getCurrentBlock: IO[BigInteger] = IO.blocking {
    web3j.ethBlockNumber().send().getBlockNumber
  }

  def getBalance(address: String): IO[Either[DeFiError, TokenAmount]] = IO.blocking {
    try {
      val balance = web3j.ethGetBalance(address, DefaultBlockParameterName.LATEST).send().getBalance
      Right(TokenAmount(balance, 18))
    } catch {
      case e: Exception => Left(NetworkError(e.getMessage))
    }
  }

  def simulateSwap(
    pool: LiquidityPool,
    amountIn: TokenAmount,
    fromTokenA: Boolean
  ): IO[Either[DeFiError, TokenAmount]] = IO.pure {
    pool.swap(amountIn, fromTokenA).map(_._2)
  }

  def simulateAddLiquidity(
    pool: LiquidityPool,
    amountA: TokenAmount,
    amountB: TokenAmount
  ): IO[Either[DeFiError, TokenAmount]] = IO.pure {
    pool.addLiquidity(amountA, amountB).map(_._2)
  }

  def calculateOptimalSwapAmount(
    reserveIn: TokenAmount,
    reserveOut: TokenAmount,
    userBalance: TokenAmount
  ): TokenAmount = {
    // Simplified optimal swap calculation
    val optimalAmount = userBalance.amount.divide(BigInteger.valueOf(2))
    TokenAmount(optimalAmount, userBalance.decimals)
  }

  def shutdown: IO[Unit] = IO.blocking {
    web3j.shutdown()
  }
}

// MARK: - Main Application
object DeFiProtocolApp extends IOApp {

  def createExamplePool: LiquidityPool = LiquidityPool(
    tokenA = "ETH",
    tokenB = "USDC",
    reserveA = TokenAmount(BigInteger.valueOf(100).multiply(BigInteger.valueOf(1e18.toLong)), 18),
    reserveB = TokenAmount(BigInteger.valueOf(200000).multiply(BigInteger.valueOf(1e6.toLong)), 6),
    totalSupply = TokenAmount(BigInteger.valueOf(14142).multiply(BigInteger.valueOf(1e18.toLong)), 18)
  )

  def run(args: List[String]): IO[ExitCode] = {
    val protocol = new DeFiProtocol("https://eth.llamarpc.com")

    val program = for {
      _ <- Console[IO].println("🏦 DeFi Protocol - Functional Scala")
      _ <- Console[IO].println("=" * 50)

      // Create example pool
      pool = createExamplePool
      _ <- Console[IO].println(s"\n📊 Liquidity Pool: ${pool.tokenA}/${pool.tokenB}")
      _ <- Console[IO].println(s"   Reserve A: ${pool.reserveA.toDecimal} ${pool.tokenA}")
      _ <- Console[IO].println(s"   Reserve B: ${pool.reserveB.toDecimal} ${pool.tokenB}")
      _ <- Console[IO].println(s"   Price: 1 ${pool.tokenA} = ${pool.price} ${pool.tokenB}")

      // Simulate swap
      swapAmount = TokenAmount(BigInteger.valueOf(1).multiply(BigInteger.valueOf(1e18.toLong)), 18)
      swapResult <- protocol.simulateSwap(pool, swapAmount, fromTokenA = true)
      _ <- swapResult match {
        case Right(amountOut) =>
          Console[IO].println(s"\n💱 Swap Simulation:")
          Console[IO].println(s"   Input: ${swapAmount.toDecimal} ${pool.tokenA}")
          Console[IO].println(s"   Output: ${amountOut.toDecimal} ${pool.tokenB}")
        case Left(error) =>
          Console[IO].println(s"\n❌ Swap failed: $error")
      }

      // Simulate add liquidity
      addAmountA = TokenAmount(BigInteger.valueOf(10).multiply(BigInteger.valueOf(1e18.toLong)), 18)
      addAmountB = TokenAmount(BigInteger.valueOf(20000).multiply(BigInteger.valueOf(1e6.toLong)), 6)
      liquidityResult <- protocol.simulateAddLiquidity(pool, addAmountA, addAmountB)
      _ <- liquidityResult match {
        case Right(lpTokens) =>
          Console[IO].println(s"\n💧 Add Liquidity Simulation:")
          Console[IO].println(s"   Add ${addAmountA.toDecimal} ${pool.tokenA}")
          Console[IO].println(s"   Add ${addAmountB.toDecimal} ${pool.tokenB}")
          Console[IO].println(s"   Receive: ${lpTokens.toDecimal} LP tokens")
        case Left(error) =>
          Console[IO].println(s"\n❌ Add liquidity failed: $error")
      }

      // Create farming pool
      farmingPool = FarmingPool(
        stakingToken = "LP-ETH-USDC",
        rewardToken = "REWARD",
        totalStaked = TokenAmount(BigInteger.ZERO, 18),
        rewardPerBlock = TokenAmount(BigInteger.valueOf(1e18.toLong), 18),
        lastRewardBlock = BigInteger.valueOf(1000000),
        accRewardPerShare = BigInteger.ZERO,
        positions = Map.empty
      )

      currentBlock <- protocol.getCurrentBlock
      _ <- Console[IO].println(s"\n🌾 Farming Pool")
      _ <- Console[IO].println(s"   Staking Token: ${farmingPool.stakingToken}")
      _ <- Console[IO].println(s"   Reward/Block: ${farmingPool.rewardPerBlock.toDecimal} ${farmingPool.rewardToken}")
      _ <- Console[IO].println(s"   Current Block: $currentBlock")

      // Shutdown
      _ <- protocol.shutdown
      _ <- Console[IO].println("\n✅ DeFi Protocol example completed")

    } yield ExitCode.Success

    program.handleErrorWith { error =>
      Console[IO].errorln(s"Error: ${error.getMessage}") *> IO.pure(ExitCode.Error)
    }
  }
}
