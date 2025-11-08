using HTTP
using JSON3

const RPC_URL = "https://mainnet.infura.io/v3/YOUR_KEY"

function rpc_call(method::String, params::Vector=[])
    body = Dict(
        "jsonrpc" => "2.0",
        "id" => 1,
        "method" => method,
        "params" => params
    )

    headers = ["Content-Type" => "application/json"]
    response = HTTP.post(RPC_URL, headers, JSON3.write(body))

    result = JSON3.read(String(response.body))
    return result.result
end

function hex_to_number(hex::String)
    hex_clean = replace(hex, "0x" => "")
    return parse(Int64, hex_clean, base=16)
end

function get_block_number()
    result = rpc_call("eth_blockNumber")
    return hex_to_number(result)
end

function get_balance(address::String)
    result = rpc_call("eth_getBalance", [address, "latest"])
    wei = hex_to_number(result)
    return wei / 1e18
end

function get_gas_price()
    result = rpc_call("eth_gasPrice")
    wei = hex_to_number(result)
    return wei / 1e9
end

function check_multiple_balances(addresses::Vector{String})
    balances = Dict{String, Float64}()

    @sync for address in addresses
        @async begin
            balance = get_balance(address)
            balances[address] = balance
        end
    end

    return balances
end

# Main
println("Current block: ", get_block_number())

vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
balance = get_balance(vitalik)
println("Vitalik balance: ", round(balance, digits=4), " ETH")

gas_price = get_gas_price()
println("Gas price: ", round(gas_price, digits=2), " Gwei")

# Check multiple balances
addresses = [
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
]

balances = check_multiple_balances(addresses)
println("\nBalances:")
for (addr, bal) in balances
    println("$addr: $(round(bal, digits=4)) ETH")
end

# Statistical analysis
all_balances = collect(values(balances))
println("\nStatistics:")
println("Average: ", round(sum(all_balances) / length(all_balances), digits=4), " ETH")
println("Total: ", round(sum(all_balances), digits=4), " ETH")
println("Max: ", round(maximum(all_balances), digits=4), " ETH")
