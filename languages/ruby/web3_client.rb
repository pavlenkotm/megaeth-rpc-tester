#!/usr/bin/env ruby

require 'net/http'
require 'json'
require 'uri'

##
# Web3 Ruby Client
#
# Simple Ruby client for interacting with Ethereum RPC endpoints
#
class Web3Client
  attr_reader :rpc_url

  def initialize(rpc_url)
    @rpc_url = rpc_url
    @uri = URI.parse(rpc_url)
  end

  # Make JSON-RPC call
  def rpc_call(method, params = [])
    request = {
      jsonrpc: '2.0',
      method: method,
      params: params,
      id: 1
    }

    http = Net::HTTP.new(@uri.host, @uri.port)
    http.use_ssl = (@uri.scheme == 'https')

    request_obj = Net::HTTP::Post.new(@uri.path, 'Content-Type' => 'application/json')
    request_obj.body = request.to_json

    response = http.request(request_obj)
    JSON.parse(response.body)
  end

  # Get latest block number
  def block_number
    result = rpc_call('eth_blockNumber')
    result['result'].to_i(16)
  end

  # Get chain ID
  def chain_id
    result = rpc_call('eth_chainId')
    result['result'].to_i(16)
  end

  # Get gas price
  def gas_price
    result = rpc_call('eth_gasPrice')
    result['result'].to_i(16)
  end

  # Get balance of address
  def get_balance(address)
    result = rpc_call('eth_getBalance', [address, 'latest'])
    result['result'].to_i(16)
  end

  # Convert Wei to Ether
  def wei_to_eth(wei)
    wei.to_f / 1_000_000_000_000_000_000
  end

  # Get transaction count (nonce)
  def transaction_count(address)
    result = rpc_call('eth_getTransactionCount', [address, 'latest'])
    result['result'].to_i(16)
  end

  # Get block by number
  def get_block(block_number)
    hex_block = "0x#{block_number.to_s(16)}"
    rpc_call('eth_getBlockByNumber', [hex_block, false])
  end

  # Get transaction by hash
  def get_transaction(tx_hash)
    rpc_call('eth_getTransactionByHash', [tx_hash])
  end

  # Get transaction receipt
  def get_transaction_receipt(tx_hash)
    rpc_call('eth_getTransactionReceipt', [tx_hash])
  end
end

# Example usage
if __FILE__ == $0
  puts "🔗 Web3 Ruby Client Example\n\n"

  # Create client
  client = Web3Client.new('https://eth.llamarpc.com')

  # Get block number
  block = client.block_number
  puts "Latest Block: #{block}"

  # Get chain ID
  chain = client.chain_id
  puts "Chain ID: #{chain}"

  # Get gas price
  gas = client.gas_price
  gas_gwei = gas / 1_000_000_000
  puts "Gas Price: #{gas_gwei} Gwei"

  # Check balance
  address = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
  balance = client.get_balance(address)
  balance_eth = client.wei_to_eth(balance)
  puts "Balance of #{address}: #{balance_eth.round(4)} ETH"

  puts "\n✅ Ruby client example completed successfully"
end
