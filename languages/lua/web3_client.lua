local http = require("socket.http")
local ltn12 = require("ltn12")
local json = require("json")

local RPC_URL = "https://mainnet.infura.io/v3/YOUR_KEY"

local function rpcCall(method, params)
    local request = {
        jsonrpc = "2.0",
        id = 1,
        method = method,
        params = params or {}
    }

    local requestBody = json.encode(request)
    local responseBody = {}

    local result, statusCode = http.request{
        url = RPC_URL,
        method = "POST",
        headers = {
            ["Content-Type"] = "application/json",
            ["Content-Length"] = #requestBody
        },
        source = ltn12.source.string(requestBody),
        sink = ltn12.sink.table(responseBody)
    }

    if result then
        local response = json.decode(table.concat(responseBody))
        return response.result
    end
    return nil
end

local function hexToNumber(hex)
    return tonumber(hex, 16)
end

local function getBlockNumber()
    local result = rpcCall("eth_blockNumber")
    return hexToNumber(result)
end

local function getBalance(address)
    local result = rpcCall("eth_getBalance", {address, "latest"})
    local wei = hexToNumber(result)
    return wei / 1e18
end

local function getGasPrice()
    local result = rpcCall("eth_gasPrice")
    local wei = hexToNumber(result)
    return wei / 1e9
end

-- Main
print("Current block: " .. getBlockNumber())
print("Vitalik balance: " .. getBalance("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045") .. " ETH")
print("Gas price: " .. getGasPrice() .. " Gwei")
