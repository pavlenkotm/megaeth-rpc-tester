(ns web3-client
  (:require [clj-http.client :as http]
            [cheshire.core :as json]
            [clojure.core.async :as async]))

(def rpc-url "https://mainnet.infura.io/v3/YOUR_KEY")

(defn rpc-call
  "Make JSON-RPC call to Ethereum node"
  [method params]
  (let [body (json/generate-string
              {:jsonrpc "2.0"
               :id 1
               :method method
               :params params})
        response (http/post rpc-url
                           {:body body
                            :headers {"Content-Type" "application/json"}
                            :as :json})]
    (get-in response [:body :result])))

(defn get-block-number
  "Get current block number"
  []
  (rpc-call "eth_blockNumber" []))

(defn get-balance
  "Get ETH balance for address"
  [address]
  (rpc-call "eth_getBalance" [address "latest"]))

(defn get-gas-price
  "Get current gas price"
  []
  (rpc-call "eth_gasPrice" []))

(defn get-transaction
  "Get transaction by hash"
  [tx-hash]
  (rpc-call "eth_getTransactionByHash" [tx-hash]))

(defn hex->decimal
  "Convert hex string to decimal"
  [hex-str]
  (Long/parseLong (subs hex-str 2) 16))

(defn wei->ether
  "Convert wei to ether"
  [wei]
  (/ (bigdec wei) 1e18))

(defn check-multiple-balances
  "Check balances for multiple addresses concurrently"
  [addresses]
  (let [results (async/chan (count addresses))]
    (doseq [address addresses]
      (async/go
        (let [balance (get-balance address)
              ether (-> balance hex->decimal wei->ether)]
          (async/>! results {:address address :balance ether}))))
    (async/<!! (async/into [] (async/take (count addresses) results)))))

(defn- find-richest
  "Find wallet with highest balance"
  [balances]
  (apply max-key :balance balances))

;; Example usage
(defn -main []
  (let [block-number (get-block-number)
        _ (println "Current block:" (hex->decimal block-number))

        vitalik "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        balance (get-balance vitalik)
        _ (println "Vitalik balance:" (wei->ether (hex->decimal balance)) "ETH")

        addresses ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
                   "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                   "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"]

        balances (check-multiple-balances addresses)
        richest (find-richest balances)]

    (doseq [{:keys [address balance]} balances]
      (println address ":" balance "ETH"))

    (println "Richest:" (:address richest) "with" (:balance richest) "ETH")))
