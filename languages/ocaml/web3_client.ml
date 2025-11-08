open Lwt.Infix
open Cohttp
open Cohttp_lwt_unix
open Yojson.Basic

type rpc_request = {
  jsonrpc : string;
  id : int;
  method_ : string;
  params : string list;
}

type 'a rpc_response = {
  jsonrpc : string;
  id : int;
  result : 'a option;
  error : Yojson.Basic.t option;
}

let rpc_url = "https://mainnet.infura.io/v3/YOUR_KEY"

let make_rpc_call method_name params =
  let request_body =
    `Assoc [
      ("jsonrpc", `String "2.0");
      ("id", `Int 1);
      ("method", `String method_name);
      ("params", `List (List.map (fun p -> `String p) params))
    ]
    |> Yojson.Basic.to_string
  in
  let headers = Header.init_with "Content-Type" "application/json" in
  let body = Cohttp_lwt.Body.of_string request_body in

  Client.post ~headers ~body (Uri.of_string rpc_url) >>= fun (resp, body) ->
  Cohttp_lwt.Body.to_string body >|= fun body_str ->
  let json = Yojson.Basic.from_string body_str in
  match json with
  | `Assoc fields ->
      (match List.assoc_opt "result" fields with
       | Some result -> Ok result
       | None -> Error "No result in response")
  | _ -> Error "Invalid response format"

let get_block_number () =
  make_rpc_call "eth_blockNumber" []

let get_balance address =
  make_rpc_call "eth_getBalance" [address; "latest"]

let get_gas_price () =
  make_rpc_call "eth_gasPrice" []

let get_transaction tx_hash =
  make_rpc_call "eth_getTransactionByHash" [tx_hash]

let hex_to_int64 hex_str =
  let cleaned = String.sub hex_str 2 (String.length hex_str - 2) in
  Int64.of_string ("0x" ^ cleaned)

let wei_to_ether wei =
  let wei_float = Int64.to_float wei in
  wei_float /. 1e18

let wei_to_gwei wei =
  let wei_float = Int64.to_float wei in
  wei_float /. 1e9

let check_balance address =
  get_balance address >>= function
  | Ok (`String balance_hex) ->
      let wei = hex_to_int64 balance_hex in
      let ether = wei_to_ether wei in
      Lwt.return (Some (address, ether))
  | _ -> Lwt.return None

let check_multiple_balances addresses =
  Lwt_list.map_p check_balance addresses >|= fun results ->
  List.filter_map (fun x -> x) results

let () =
  let main =
    (* Get block number *)
    get_block_number () >>= fun block_result ->
    (match block_result with
     | Ok (`String block_hex) ->
         let block_num = hex_to_int64 block_hex in
         Lwt_io.printf "Current block: %Ld\n" block_num
     | _ -> Lwt_io.printf "Error getting block\n") >>= fun () ->

    (* Get balance *)
    let vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" in
    get_balance vitalik >>= fun balance_result ->
    (match balance_result with
     | Ok (`String balance_hex) ->
         let wei = hex_to_int64 balance_hex in
         let ether = wei_to_ether wei in
         Lwt_io.printf "Vitalik's balance: %.4f ETH\n" ether
     | _ -> Lwt_io.printf "Error getting balance\n") >>= fun () ->

    (* Get gas price *)
    get_gas_price () >>= fun gas_result ->
    (match gas_result with
     | Ok (`String gas_hex) ->
         let wei = hex_to_int64 gas_hex in
         let gwei = wei_to_gwei wei in
         Lwt_io.printf "Gas price: %.2f Gwei\n" gwei
     | _ -> Lwt_io.printf "Error getting gas price\n") >>= fun () ->

    (* Check multiple balances *)
    let addresses = [
      "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
      "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb";
      "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
    ] in

    check_multiple_balances addresses >>= fun balances ->
    Lwt_list.iter_s (fun (addr, bal) ->
      Lwt_io.printf "%s: %.4f ETH\n" addr bal
    ) balances
  in
  Lwt_main.run main
