# ⚡ MegaETH RPC Tester

Simple async CLI tool for testing the speed and reliability of Ethereum RPC endpoints.  
Ideal for MegaETH, Alchemy, Ankr, or any EVM node.

## 🚀 Quick Start
```bash
# 1) clone
git clone https://github.com/pavlenkotm/megaeth-rpc-tester
cd megaeth-rpc-tester

# 2) install
python -m pip install -r requirements.txt

# 3) run (пример публичных RPC)
python rpc_tester/main.py https://eth.llamarpc.com https://rpc.ankr.com/eth
