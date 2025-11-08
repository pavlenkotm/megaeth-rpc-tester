(defproject web3-clojure "1.0.0"
  :description "Web3 Ethereum client for Clojure"
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [clj-http "3.12.3"]
                 [cheshire "5.12.0"]
                 [org.clojure/core.async "1.6.681"]]
  :main ^:skip-aot web3-client
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
