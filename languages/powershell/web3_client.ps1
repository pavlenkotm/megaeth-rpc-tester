#!/usr/bin/env pwsh

$RpcUrl = "https://mainnet.infura.io/v3/YOUR_KEY"

function Invoke-RpcCall {
    param(
        [string]$Method,
        [array]$Params = @()
    )

    $body = @{
        jsonrpc = "2.0"
        id = 1
        method = $Method
        params = $Params
    } | ConvertTo-Json -Depth 10

    $response = Invoke-RestMethod -Uri $RpcUrl -Method Post -Body $body -ContentType "application/json"
    return $response.result
}

function ConvertFrom-Hex {
    param([string]$Hex)

    $cleanHex = $Hex -replace '^0x', ''
    return [Convert]::ToInt64($cleanHex, 16)
}

function Get-BlockNumber {
    $result = Invoke-RpcCall -Method "eth_blockNumber"
    return ConvertFrom-Hex $result
}

function Get-Balance {
    param([string]$Address)

    $result = Invoke-RpcCall -Method "eth_getBalance" -Params @($Address, "latest")
    $wei = ConvertFrom-Hex $result
    return $wei / 1e18
}

function Get-GasPrice {
    $result = Invoke-RpcCall -Method "eth_gasPrice"
    $wei = ConvertFrom-Hex $result
    return $wei / 1e9
}

# Main
$blockNumber = Get-BlockNumber
Write-Host "Current block: $blockNumber"

$vitalikAddress = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
$balance = Get-Balance -Address $vitalikAddress
Write-Host ("Vitalik balance: {0:N4} ETH" -f $balance)

$gasPrice = Get-GasPrice
Write-Host ("Gas price: {0:N2} Gwei" -f $gasPrice)

# Check multiple balances
$addresses = @(
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
)

Write-Host "`nChecking multiple balances:"
foreach ($addr in $addresses) {
    $bal = Get-Balance -Address $addr
    Write-Host ("{0}: {1:N4} ETH" -f $addr, $bal)
}
