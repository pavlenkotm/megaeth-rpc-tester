#!/usr/bin/env perl
use strict;
use warnings;
use LWP::UserAgent;
use JSON;
use Math::BigInt;

my $RPC_URL = 'https://mainnet.infura.io/v3/YOUR_KEY';

sub rpc_call {
    my ($method, $params) = @_;

    my $ua = LWP::UserAgent->new;
    my $json = JSON->new;

    my $request = {
        jsonrpc => '2.0',
        id => 1,
        method => $method,
        params => $params || []
    };

    my $response = $ua->post(
        $RPC_URL,
        Content_Type => 'application/json',
        Content => $json->encode($request)
    );

    if ($response->is_success) {
        my $data = $json->decode($response->content);
        return $data->{result};
    }
    return undef;
}

sub hex_to_number {
    my ($hex) = @_;
    $hex =~ s/^0x//;
    return Math::BigInt->from_hex($hex)->numify();
}

sub get_block_number {
    my $result = rpc_call('eth_blockNumber');
    return hex_to_number($result);
}

sub get_balance {
    my ($address) = @_;
    my $result = rpc_call('eth_getBalance', [$address, 'latest']);
    my $wei = hex_to_number($result);
    return $wei / 1e18;
}

sub get_gas_price {
    my $result = rpc_call('eth_gasPrice');
    my $wei = hex_to_number($result);
    return $wei / 1e9;
}

# Main
my $block = get_block_number();
print "Current block: $block\n";

my $balance = get_balance('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
printf "Vitalik balance: %.4f ETH\n", $balance;

my $gas = get_gas_price();
printf "Gas price: %.2f Gwei\n", $gas;
