<?php

class Web3Client {
    private $rpcUrl;

    public function __construct($rpcUrl) {
        $this->rpcUrl = $rpcUrl;
    }

    private function rpcCall($method, $params = []) {
        $request = [
            'jsonrpc' => '2.0',
            'id' => 1,
            'method' => $method,
            'params' => $params
        ];

        $ch = curl_init($this->rpcUrl);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($request));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);

        $response = curl_exec($ch);
        curl_close($ch);

        $data = json_decode($response, true);
        return $data['result'] ?? null;
    }

    private function hexToNumber($hex) {
        return hexdec(str_replace('0x', '', $hex));
    }

    public function getBlockNumber() {
        $result = $this->rpcCall('eth_blockNumber');
        return $this->hexToNumber($result);
    }

    public function getBalance($address) {
        $result = $this->rpcCall('eth_getBalance', [$address, 'latest']);
        $wei = $this->hexToNumber($result);
        return $wei / 1e18;
    }

    public function getGasPrice() {
        $result = $this->rpcCall('eth_gasPrice');
        $wei = $this->hexToNumber($result);
        return $wei / 1e9;
    }

    public function getTransaction($txHash) {
        return $this->rpcCall('eth_getTransactionByHash', [$txHash]);
    }

    public function checkMultipleBalances($addresses) {
        $balances = [];
        foreach ($addresses as $address) {
            $balances[$address] = $this->getBalance($address);
        }
        return $balances;
    }
}

// Main
$client = new Web3Client('https://mainnet.infura.io/v3/YOUR_KEY');

echo "Current block: " . $client->getBlockNumber() . "\n";

$vitalik = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045';
$balance = $client->getBalance($vitalik);
echo sprintf("Vitalik balance: %.4f ETH\n", $balance);

$gasPrice = $client->getGasPrice();
echo sprintf("Gas price: %.2f Gwei\n", $gasPrice);

// Check multiple balances
$addresses = [
    '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
    '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    '0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8'
];

echo "\nChecking multiple balances:\n";
$balances = $client->checkMultipleBalances($addresses);
foreach ($balances as $addr => $bal) {
    echo sprintf("%s: %.4f ETH\n", $addr, $bal);
}

// Find richest
$richest = array_keys($balances, max($balances))[0];
echo sprintf("\nRichest wallet: %s with %.4f ETH\n", $richest, $balances[$richest]);

?>
