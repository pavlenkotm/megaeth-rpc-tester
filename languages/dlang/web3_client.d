import std.stdio;
import std.net.curl;
import std.json;
import std.conv;
import std.string;
import std.algorithm;

immutable string RPC_URL = "https://mainnet.infura.io/v3/YOUR_KEY";

JSONValue rpcCall(string method, string[] params) {
    auto client = HTTP();

    JSONValue request = parseJSON(`{}`);
    request["jsonrpc"] = "2.0";
    request["id"] = 1;
    request["method"] = method;
    request["params"] = JSONValue(params);

    auto content = post(RPC_URL, request.toString(), client);
    auto response = parseJSON(content);

    return response["result"];
}

long hexToLong(string hex) {
    if (hex.startsWith("0x")) {
        hex = hex[2 .. $];
    }
    return to!long(hex, 16);
}

long getBlockNumber() {
    auto result = rpcCall("eth_blockNumber", []);
    return hexToLong(result.str);
}

double getBalance(string address) {
    auto result = rpcCall("eth_getBalance", [address, "latest"]);
    long wei = hexToLong(result.str);
    return cast(double)wei / 1e18;
}

double getGasPrice() {
    auto result = rpcCall("eth_gasPrice", []);
    long wei = hexToLong(result.str);
    return cast(double)wei / 1e9;
}

void main() {
    writeln("Current block: ", getBlockNumber());
    writeln("Vitalik balance: ", getBalance("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"), " ETH");
    writeln("Gas price: ", getGasPrice(), " Gwei");
}
