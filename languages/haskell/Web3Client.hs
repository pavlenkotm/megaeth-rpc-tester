module Web3Client where

import Network.HTTP.Simple
import Data.Aeson
import qualified Data.ByteString.Char8 as BS
import qualified Data.Text as T

-- | JSON-RPC Request
data RPCRequest = RPCRequest
  { jsonrpc :: String
  , method :: String
  , params :: [Value]
  , reqId :: Int
  } deriving (Show)

instance ToJSON RPCRequest where
  toJSON req = object
    [ "jsonrpc" .= jsonrpc req
    , "method" .= method req
    , "params" .= params req
    , "id" .= reqId req
    ]

-- | JSON-RPC Response
data RPCResponse = RPCResponse
  { result :: Maybe Value
  , rpcError :: Maybe Value
  , respId :: Int
  } deriving (Show)

instance FromJSON RPCResponse where
  parseJSON = withObject "RPCResponse" $ \v -> RPCResponse
    <$> v .:? "result"
    <*> v .:? "error"
    <*> v .: "id"

-- | Make RPC call
makeRPCCall :: String -> String -> [Value] -> IO RPCResponse
makeRPCCall url methodName methodParams = do
  let request = RPCRequest "2.0" methodName methodParams 1

  response <- httpJSON =<< parseRequest ("POST " ++ url)
    & setRequestBodyJSON request
    & setRequestHeader "Content-Type" ["application/json"]

  return $ getResponseBody response

-- | Get latest block number
getBlockNumber :: String -> IO (Maybe Integer)
getBlockNumber url = do
  response <- makeRPCCall url "eth_blockNumber" []
  case result response of
    Just (String hexBlock) -> return $ Just $ hexToInt hexBlock
    _ -> return Nothing

-- | Convert hex string to integer
hexToInt :: T.Text -> Integer
hexToInt hex = read ("0x" ++ T.unpack hex) :: Integer

-- | Get chain ID
getChainId :: String -> IO (Maybe Integer)
getChainId url = do
  response <- makeRPCCall url "eth_chainId" []
  case result response of
    Just (String hexId) -> return $ Just $ hexToInt hexId
    _ -> return Nothing

-- | Get gas price
getGasPrice :: String -> IO (Maybe Integer)
getGasPrice url = do
  response <- makeRPCCall url "eth_gasPrice" []
  case result response of
    Just (String hexPrice) -> return $ Just $ hexToInt hexPrice
    _ -> return Nothing

-- | Example usage
main :: IO ()
main = do
  putStrLn "🔗 Haskell Web3 Client Example\n"

  let rpcUrl = "https://eth.llamarpc.com"

  -- Get block number
  blockNum <- getBlockNumber rpcUrl
  case blockNum of
    Just num -> putStrLn $ "Latest Block: " ++ show num
    Nothing -> putStrLn "Failed to get block number"

  -- Get chain ID
  chainId <- getChainId rpcUrl
  case chainId of
    Just cid -> putStrLn $ "Chain ID: " ++ show cid
    Nothing -> putStrLn "Failed to get chain ID"

  putStrLn "\n✅ Haskell example completed"
