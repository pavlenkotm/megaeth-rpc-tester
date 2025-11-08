# Erlang - Fault-Tolerant Blockchain Infrastructure

![Erlang](https://img.shields.io/badge/Erlang-red)
![OTP](https://img.shields.io/badge/OTP-25-orange)

## Features
- ✅ OTP gen_server RPC client
- ✅ Distributed blockchain nodes
- ✅ Fault tolerance & supervision
- ✅ Hot code reloading

## Installation
```bash
rebar3 compile
```

## Usage
```erlang
erl -pa _build/default/lib/*/ebin
web3_client:get_block_number().
```
