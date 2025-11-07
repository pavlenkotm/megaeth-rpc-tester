#!/bin/bash

################################################################################
# Ethereum Node Manager
#
# Script for managing Ethereum nodes (Geth, Erigon, Nethermind)
# Supports starting, stopping, monitoring, and log management
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
NODE_TYPE="${NODE_TYPE:-geth}"
DATA_DIR="${DATA_DIR:-./ethereum-data}"
NETWORK="${NETWORK:-mainnet}"
HTTP_PORT="${HTTP_PORT:-8545}"
WS_PORT="${WS_PORT:-8546}"
METRICS_PORT="${METRICS_PORT:-6060}"

start_geth() {
    echo -e "${BLUE}Starting Geth node...${NC}"

    geth \
        --datadir "$DATA_DIR" \
        --${NETWORK} \
        --http \
        --http.addr "0.0.0.0" \
        --http.port "$HTTP_PORT" \
        --http.api "eth,net,web3,txpool" \
        --ws \
        --ws.addr "0.0.0.0" \
        --ws.port "$WS_PORT" \
        --ws.api "eth,net,web3" \
        --metrics \
        --metrics.addr "0.0.0.0" \
        --metrics.port "$METRICS_PORT" \
        --syncmode "snap" \
        --maxpeers 50 \
        &

    echo $! > geth.pid
    echo -e "${GREEN}✅ Geth started (PID: $(cat geth.pid))${NC}"
}

stop_node() {
    echo -e "${BLUE}Stopping node...${NC}"

    if [ -f "${NODE_TYPE}.pid" ]; then
        PID=$(cat "${NODE_TYPE}.pid")
        kill "$PID" 2>/dev/null || true
        rm "${NODE_TYPE}.pid"
        echo -e "${GREEN}✅ Node stopped${NC}"
    else
        echo -e "${RED}❌ PID file not found${NC}"
    fi
}

check_sync_status() {
    echo -e "${BLUE}Checking sync status...${NC}"

    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
        --data '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}' \
        "http://localhost:$HTTP_PORT")

    if echo "$RESPONSE" | grep -q '"result":false'; then
        echo -e "${GREEN}✅ Node is fully synced${NC}"
    else
        CURRENT_BLOCK=$(echo "$RESPONSE" | jq -r '.result.currentBlock')
        HIGHEST_BLOCK=$(echo "$RESPONSE" | jq -r '.result.highestBlock')
        echo -e "${BLUE}Syncing: Block $CURRENT_BLOCK / $HIGHEST_BLOCK${NC}"
    fi
}

view_logs() {
    LOG_FILE="${DATA_DIR}/geth.log"

    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo -e "${RED}❌ Log file not found${NC}"
    fi
}

case "$1" in
    start)
        start_geth
        ;;
    stop)
        stop_node
        ;;
    status)
        check_sync_status
        ;;
    logs)
        view_logs
        ;;
    *)
        echo "Usage: $0 {start|stop|status|logs}"
        exit 1
        ;;
esac
