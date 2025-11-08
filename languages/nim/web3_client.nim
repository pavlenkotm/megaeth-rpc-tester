import httpclient, json, strutils, asyncdispatch

const RPC_URL = "https://mainnet.infura.io/v3/YOUR_KEY"

proc rpcCall(client: HttpClient, methodName, params: string): JsonNode =
  let body = %*{
    "jsonrpc": "2.0",
    "id": 1,
    "method": methodName,
    "params": parseJson(params)
  }
  let response = client.postContent(RPC_URL, $body, "application/json")
  parseJson(response)["result"]

proc getBlockNumber*(client: HttpClient): int64 =
  let result = rpcCall(client, "eth_blockNumber", "[]")
  fromHex[int64](result.getStr)

proc getBalance*(client: HttpClient, address: string): float =
  let result = rpcCall(client, "eth_getBalance", "[\"$1\", \"latest\"]" % address)
  let wei = fromHex[int64](result.getStr)
  float(wei) / 1e18

proc getGasPrice*(client: HttpClient): float =
  let result = rpcCall(client, "eth_gasPrice", "[]")
  let wei = fromHex[int64](result.getStr)
  float(wei) / 1e9

when isMainModule:
  var client = newHttpClient()

  echo "Current block: ", client.getBlockNumber()
  echo "Vitalik balance: ", client.getBalance("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"), " ETH"
  echo "Gas price: ", client.getGasPrice(), " Gwei"

  client.close()
