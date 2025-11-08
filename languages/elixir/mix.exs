defmodule Web3Elixir.MixProject do
  use Mix.Project

  def project do
    [
      app: :web3_elixir,
      version: "1.0.0",
      elixir: "~> 1.15",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {Web3Elixir.Application, []}
    ]
  end

  defp deps do
    [
      {:httpoison, "~> 2.0"},
      {:jason, "~> 1.4"}
    ]
  end
end
