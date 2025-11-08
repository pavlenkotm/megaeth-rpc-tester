module Web3Client

open System
open System.Net.Http
open System.Text
open System.Text.Json
open System.Threading.Tasks

type RpcRequest = {
    jsonrpc: string
    id: int
    method: string
    params: string[]
}

type RpcResponse<'T> = {
    jsonrpc: string
    id: int
    result: 'T option
    error: JsonElement option
}

type EthereumClient(rpcUrl: string) =
    let httpClient = new HttpClient()

    member private this.RpcCall<'T>(method: string, parameters: string[]) : Task<Result<'T, string>> =
        task {
            let request = {
                jsonrpc = "2.0"
                id = 1
                method = method
                params = parameters
            }

            let json = JsonSerializer.Serialize(request)
            let content = new StringContent(json, Encoding.UTF8, "application/json")

            try
                let! response = httpClient.PostAsync(rpcUrl, content)
                let! responseBody = response.Content.ReadAsStringAsync()

                let rpcResponse = JsonSerializer.Deserialize<RpcResponse<'T>>(responseBody)

                return
                    match rpcResponse.result with
                    | Some result -> Ok result
                    | None -> Error "No result in response"
            with
            | ex -> return Error ex.Message
        }

    member this.GetBlockNumber() : Task<Result<string, string>> =
        this.RpcCall<string>("eth_blockNumber", [||])

    member this.GetBalance(address: string) : Task<Result<string, string>> =
        this.RpcCall<string>("eth_getBalance", [| address; "latest" |])

    member this.GetGasPrice() : Task<Result<string, string>> =
        this.RpcCall<string>("eth_gasPrice", [||])

    member this.GetTransaction(txHash: string) : Task<Result<JsonElement, string>> =
        this.RpcCall<JsonElement>("eth_getTransactionByHash", [| txHash |])

module Conversion =
    let hexToDecimal (hex: string) =
        let cleaned = hex.Replace("0x", "")
        Convert.ToInt64(cleaned, 16)

    let weiToEther (wei: int64) =
        (decimal wei) / 1_000_000_000_000_000_000M

    let weiToGwei (wei: int64) =
        (decimal wei) / 1_000_000_000M

module WalletService =
    open Conversion

    let checkMultipleBalances (client: EthereumClient) (addresses: string list) =
        task {
            let! results =
                addresses
                |> List.map (fun address ->
                    task {
                        let! balanceResult = client.GetBalance(address)
                        return
                            match balanceResult with
                            | Ok balance ->
                                let ether = balance |> hexToDecimal |> weiToEther
                                Some (address, ether)
                            | Error _ -> None
                    })
                |> Task.WhenAll

            return
                results
                |> Array.choose id
                |> Map.ofArray
        }

    let findRichestWallet (balances: Map<string, decimal>) =
        balances
        |> Map.toSeq
        |> Seq.maxBy snd

module Program =
    [<EntryPoint>]
    let main args =
        task {
            let client = EthereumClient("https://mainnet.infura.io/v3/YOUR_KEY")

            // Get block number
            let! blockResult = client.GetBlockNumber()
            match blockResult with
            | Ok block ->
                let blockNum = Conversion.hexToDecimal block
                printfn "Current block: %d" blockNum
            | Error err -> printfn "Error: %s" err

            // Get balance
            let vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
            let! balanceResult = client.GetBalance(vitalik)
            match balanceResult with
            | Ok balance ->
                let ether = balance |> Conversion.hexToDecimal |> Conversion.weiToEther
                printfn "Vitalik's balance: %M ETH" ether
            | Error err -> printfn "Error: %s" err

            // Get gas price
            let! gasPriceResult = client.GetGasPrice()
            match gasPriceResult with
            | Ok gasPrice ->
                let gwei = gasPrice |> Conversion.hexToDecimal |> Conversion.weiToGwei
                printfn "Gas price: %M Gwei" gwei
            | Error err -> printfn "Error: %s" err

            // Check multiple balances
            let addresses = [
                "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
                "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
            ]

            let! balances = WalletService.checkMultipleBalances client addresses

            balances |> Map.iter (fun addr bal ->
                printfn "%s: %M ETH" addr bal
            )

            let (richestAddr, richestBal) = WalletService.findRichestWallet balances
            printfn "Richest: %s with %M ETH" richestAddr richestBal

            return 0
        }
        |> Async.AwaitTask
        |> Async.RunSynchronously
