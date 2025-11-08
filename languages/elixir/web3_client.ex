defmodule Web3Client do
  @moduledoc """
  Ethereum Web3 client for Elixir with GenServer support
  """
  use GenServer
  require Logger

  @rpc_url "https://mainnet.infura.io/v3/YOUR_KEY"

  # Client API
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def get_block_number do
    GenServer.call(__MODULE__, :get_block_number)
  end

  def get_balance(address) do
    GenServer.call(__MODULE__, {:get_balance, address})
  end

  def get_gas_price do
    GenServer.call(__MODULE__, :get_gas_price)
  end

  # Server Callbacks
  @impl true
  def init(_opts) do
    {:ok, %{rpc_url: @rpc_url}}
  end

  @impl true
  def handle_call(:get_block_number, _from, state) do
    result = rpc_call("eth_blockNumber", [])
    {:reply, result, state}
  end

  @impl true
  def handle_call({:get_balance, address}, _from, state) do
    result = rpc_call("eth_getBalance", [address, "latest"])
    {:reply, result, state}
  end

  @impl true
  def handle_call(:get_gas_price, _from, state) do
    result = rpc_call("eth_gasPrice", [])
    {:reply, result, state}
  end

  # Private Functions
  defp rpc_call(method, params) do
    body = Jason.encode!(%{
      jsonrpc: "2.0",
      id: 1,
      method: method,
      params: params
    })

    headers = [{"Content-Type", "application/json"}]

    case HTTPoison.post(@rpc_url, body, headers) do
      {:ok, %{body: response_body}} ->
        case Jason.decode(response_body) do
          {:ok, %{"result" => result}} -> {:ok, result}
          {:ok, %{"error" => error}} -> {:error, error}
          _ -> {:error, :invalid_response}
        end
      {:error, reason} -> {:error, reason}
    end
  end
end

defmodule WalletBalance do
  def check_multiple(addresses) do
    addresses
    |> Task.async_stream(fn address ->
      {:ok, balance} = Web3Client.get_balance(address)
      {address, hex_to_decimal(balance)}
    end)
    |> Enum.map(fn {:ok, result} -> result end)
    |> Map.new()
  end

  defp hex_to_decimal("0x" <> hex) do
    String.to_integer(hex, 16)
  end
end
