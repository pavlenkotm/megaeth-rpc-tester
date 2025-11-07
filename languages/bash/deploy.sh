#!/bin/bash

################################################################################
# Smart Contract Deployment Script
#
# A comprehensive Bash script for deploying and managing smart contracts
# Supports Hardhat, Foundry, and direct RPC deployment
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NETWORK="${NETWORK:-localhost}"
RPC_URL="${RPC_URL:-http://localhost:8545}"
PRIVATE_KEY="${PRIVATE_KEY:-}"
GAS_PRICE="${GAS_PRICE:-auto}"
GAS_LIMIT="${GAS_LIMIT:-3000000}"

# Functions
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

check_dependencies() {
    print_info "Checking dependencies..."

    # Check for Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed"
        exit 1
    fi

    # Check for either Hardhat or Foundry
    if ! command -v hardhat &> /dev/null && ! command -v forge &> /dev/null; then
        print_warning "Neither Hardhat nor Foundry found"
        print_info "Install Hardhat: npm install --save-dev hardhat"
        print_info "Install Foundry: curl -L https://foundry.paradigm.xyz | bash"
    fi

    print_success "Dependencies check passed"
}

check_network_connection() {
    print_info "Checking network connection to $RPC_URL..."

    # Try to get block number
    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
        --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
        "$RPC_URL")

    if echo "$RESPONSE" | grep -q "result"; then
        BLOCK_NUMBER=$(echo "$RESPONSE" | jq -r '.result')
        print_success "Connected to network. Latest block: $BLOCK_NUMBER"
    else
        print_error "Failed to connect to RPC endpoint"
        echo "$RESPONSE"
        exit 1
    fi
}

get_gas_price() {
    print_info "Fetching current gas price..."

    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
        --data '{"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}' \
        "$RPC_URL")

    GAS_PRICE_WEI=$(echo "$RESPONSE" | jq -r '.result')
    GAS_PRICE_GWEI=$((16#${GAS_PRICE_WEI:2} / 1000000000))

    print_info "Current gas price: $GAS_PRICE_GWEI Gwei"
}

get_chain_id() {
    print_info "Fetching chain ID..."

    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
        --data '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}' \
        "$RPC_URL")

    CHAIN_ID=$(echo "$RESPONSE" | jq -r '.result')
    CHAIN_ID_DEC=$((16#${CHAIN_ID:2}))

    print_info "Chain ID: $CHAIN_ID_DEC"
}

deploy_with_hardhat() {
    print_info "Deploying with Hardhat..."

    if [ ! -f "hardhat.config.js" ] && [ ! -f "hardhat.config.ts" ]; then
        print_error "Hardhat config not found"
        exit 1
    fi

    npx hardhat run scripts/deploy.js --network "$NETWORK"
    print_success "Deployment with Hardhat completed"
}

deploy_with_foundry() {
    print_info "Deploying with Foundry..."

    if [ ! -f "foundry.toml" ]; then
        print_error "Foundry config not found"
        exit 1
    fi

    if [ -z "$PRIVATE_KEY" ]; then
        print_error "PRIVATE_KEY environment variable not set"
        exit 1
    fi

    forge script script/Deploy.s.sol:Deploy \
        --rpc-url "$RPC_URL" \
        --private-key "$PRIVATE_KEY" \
        --broadcast \
        --verify

    print_success "Deployment with Foundry completed"
}

verify_contract() {
    local CONTRACT_ADDRESS=$1
    local NETWORK=$2

    print_info "Verifying contract at $CONTRACT_ADDRESS on $NETWORK..."

    # Add your verification logic here
    # This is a placeholder
    print_warning "Contract verification not implemented yet"
}

backup_deployment() {
    local DEPLOYMENT_FILE=$1
    local BACKUP_DIR="deployments/backups"

    mkdir -p "$BACKUP_DIR"

    if [ -f "$DEPLOYMENT_FILE" ]; then
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        cp "$DEPLOYMENT_FILE" "$BACKUP_DIR/deployment_$TIMESTAMP.json"
        print_success "Deployment backed up"
    fi
}

main() {
    echo "═══════════════════════════════════════════"
    echo "   Smart Contract Deployment Script"
    echo "═══════════════════════════════════════════"
    echo

    # Check dependencies
    check_dependencies

    # Check network connection
    check_network_connection

    # Get network info
    get_chain_id
    get_gas_price

    # Backup existing deployments
    backup_deployment "deployments/${NETWORK}.json"

    # Deploy based on available tools
    if command -v hardhat &> /dev/null; then
        deploy_with_hardhat
    elif command -v forge &> /dev/null; then
        deploy_with_foundry
    else
        print_error "No deployment tool found (Hardhat or Foundry required)"
        exit 1
    fi

    echo
    print_success "Deployment process completed successfully!"
    echo "═══════════════════════════════════════════"
}

# Run main function
main "$@"
