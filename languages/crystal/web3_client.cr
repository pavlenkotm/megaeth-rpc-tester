require "http/client"
require "json"

module Web3Client
  RPC_URL = "https://mainnet.infura.io/v3/YOUR_KEY"

  def self.rpc_call(method : String, params : Array(String))
    client = HTTP::Client.new(URI.parse(RPC_URL))

    body = {
      "jsonrpc" => "2.0",
      "id" => 1,
      "method" => method,
      "params" => params
    }.to_json

    headers = HTTP::Headers{"Content-Type" => "application/json"}
    response = client.post("/", headers: headers, body: body)

    JSON.parse(response.body)["result"]
  end

  def self.get_block_number : Int64
    result = rpc_call("eth_blockNumber", [] of String)
    result.as_s.lchop("0x").to_i64(16)
  end

  def self.get_balance(address : String) : Float64
    result = rpc_call("eth_getBalance", [address, "latest"])
    wei = result.as_s.lchop("0x").to_i64(16)
    wei.to_f / 1e18
  end

  def self.get_gas_price : Float64
    result = rpc_call("eth_gasPrice", [] of String)
    wei = result.as_s.lchop("0x").to_i64(16)
    wei.to_f / 1e9
  end
end

# Main
puts "Current block: #{Web3Client.get_block_number}"
puts "Vitalik balance: #{Web3Client.get_balance("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")} ETH"
puts "Gas price: #{Web3Client.get_gas_price} Gwei"
