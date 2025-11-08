(* FA2 Token Implementation in CameLIGO *)

type token_id = nat

type transfer_destination = {
  to_ : address;
  token_id : token_id;
  amount : nat;
}

type transfer = {
  from_ : address;
  txs : transfer_destination list;
}

type balance_of_request = {
  owner : address;
  token_id : token_id;
}

type balance_of_response = {
  request : balance_of_request;
  balance : nat;
}

type operator_param = {
  owner : address;
  operator : address;
  token_id : token_id;
}

type update_operator =
  | Add_operator of operator_param
  | Remove_operator of operator_param

type token_metadata = {
  token_id : token_id;
  token_info : (string, bytes) map;
}

type storage = {
  ledger : ((address * token_id), nat) big_map;
  operators : ((address * (address * token_id)), unit) big_map;
  token_metadata : (token_id, token_metadata) big_map;
  total_supply : nat;
}

type parameter =
  | Transfer of transfer list
  | Balance_of of (balance_of_request list * (balance_of_response list contract))
  | Update_operators of update_operator list
  | Mint of (address * nat)

type return = operation list * storage

(* Error codes *)
let err_insufficient_balance = "FA2_INSUFFICIENT_BALANCE"
let err_not_operator = "FA2_NOT_OPERATOR"
let err_not_owner = "FA2_NOT_OWNER"

(* Helper: Get balance *)
let get_balance (ledger : ((address * token_id), nat) big_map) (owner : address) (token_id : token_id) : nat =
  match Big_map.find_opt (owner, token_id) ledger with
  | Some balance -> balance
  | None -> 0n

(* Helper: Update balance *)
let update_balance (ledger : ((address * token_id), nat) big_map) (owner : address) (token_id : token_id) (amount : nat) : ((address * token_id), nat) big_map =
  Big_map.update (owner, token_id) (Some amount) ledger

(* Transfer tokens *)
let transfer (params : transfer list) (storage : storage) : return =
  let process_transfer (store : storage) (param : transfer) : storage =
    let process_tx (s : storage) (tx : transfer_destination) : storage =
      let sender_balance = get_balance s.ledger param.from_ tx.token_id in
      let () = assert_with_error (sender_balance >= tx.amount) err_insufficient_balance in

      (* Check operator permission *)
      let is_owner = Tezos.get_sender () = param.from_ in
      let is_operator = Big_map.mem (param.from_, (Tezos.get_sender (), tx.token_id)) s.operators in
      let () = assert_with_error (is_owner || is_operator) err_not_operator in

      (* Update balances *)
      let new_sender_balance = sender_balance - tx.amount in
      let new_ledger = update_balance s.ledger param.from_ tx.token_id new_sender_balance in

      let receiver_balance = get_balance new_ledger tx.to_ tx.token_id in
      let new_receiver_balance = receiver_balance + tx.amount in
      let final_ledger = update_balance new_ledger tx.to_ tx.token_id new_receiver_balance in

      { s with ledger = final_ledger }
    in
    List.fold process_tx param.txs store
  in
  let new_storage = List.fold process_transfer params storage in
  ([] : operation list), new_storage

(* Get balances *)
let balance_of (requests : balance_of_request list) (callback : balance_of_response list contract) (storage : storage) : return =
  let get_balance_response (request : balance_of_request) : balance_of_response =
    let balance = get_balance storage.ledger request.owner request.token_id in
    { request = request; balance = balance }
  in
  let responses = List.map get_balance_response requests in
  let op = Tezos.transaction responses 0mutez callback in
  [op], storage

(* Update operators *)
let update_operators (params : update_operator list) (storage : storage) : return =
  let update_operator (operators : ((address * (address * token_id)), unit) big_map) (param : update_operator) : ((address * (address * token_id)), unit) big_map =
    match param with
    | Add_operator op_param ->
        Big_map.update (op_param.owner, (op_param.operator, op_param.token_id)) (Some unit) operators
    | Remove_operator op_param ->
        Big_map.update (op_param.owner, (op_param.operator, op_param.token_id)) (None : unit option) operators
  in
  let new_operators = List.fold update_operator params storage.operators in
  ([] : operation list), { storage with operators = new_operators }

(* Mint new tokens *)
let mint (recipient : address) (amount : nat) (storage : storage) : return =
  let current_balance = get_balance storage.ledger recipient 0n in
  let new_balance = current_balance + amount in
  let new_ledger = update_balance storage.ledger recipient 0n new_balance in
  let new_supply = storage.total_supply + amount in
  ([] : operation list), { storage with ledger = new_ledger; total_supply = new_supply }

(* Main entry point *)
let main (param : parameter) (storage : storage) : return =
  match param with
  | Transfer transfers -> transfer transfers storage
  | Balance_of (requests, callback) -> balance_of requests callback storage
  | Update_operators updates -> update_operators updates storage
  | Mint (recipient, amount) -> mint recipient amount storage
