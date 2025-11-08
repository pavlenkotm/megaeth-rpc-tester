#!/usr/bin/env Rscript

library(httr)
library(jsonlite)

RPC_URL <- "https://mainnet.infura.io/v3/YOUR_KEY"

rpc_call <- function(method, params = list()) {
  body <- list(
    jsonrpc = "2.0",
    id = 1,
    method = method,
    params = params
  )

  response <- POST(
    RPC_URL,
    body = toJSON(body, auto_unbox = TRUE),
    content_type_json()
  )

  content <- content(response, as = "parsed", type = "application/json")
  return(content$result)
}

hex_to_number <- function(hex) {
  hex_clean <- sub("^0x", "", hex)
  strtoi(hex_clean, base = 16L)
}

get_block_number <- function() {
  result <- rpc_call("eth_blockNumber")
  return(hex_to_number(result))
}

get_balance <- function(address) {
  result <- rpc_call("eth_getBalance", list(address, "latest"))
  wei <- hex_to_number(result)
  return(as.numeric(wei) / 1e18)
}

get_gas_price <- function() {
  result <- rpc_call("eth_gasPrice")
  wei <- hex_to_number(result)
  return(as.numeric(wei) / 1e9)
}

check_multiple_balances <- function(addresses) {
  balances <- sapply(addresses, get_balance)
  data.frame(
    address = addresses,
    balance = balances,
    stringsAsFactors = FALSE
  )
}

# Main
cat("Current block:", get_block_number(), "\n")

vitalik <- "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
balance <- get_balance(vitalik)
cat(sprintf("Vitalik balance: %.4f ETH\n", balance))

gas_price <- get_gas_price()
cat(sprintf("Gas price: %.2f Gwei\n", gas_price))

# Check multiple balances
addresses <- c(
  "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
)

balances_df <- check_multiple_balances(addresses)
print(balances_df)

# Statistical analysis
cat(sprintf("\nAverage balance: %.4f ETH\n", mean(balances_df$balance)))
cat(sprintf("Total balance: %.4f ETH\n", sum(balances_df$balance)))
