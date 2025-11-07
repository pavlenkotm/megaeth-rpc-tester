.PHONY: install compile test deploy clean

install:
	npm install

compile:
	npx hardhat compile

test:
	npx hardhat test

coverage:
	npx hardhat coverage

deploy-local:
	npx hardhat run scripts/deploy.js --network localhost

deploy-sepolia:
	npx hardhat run scripts/deploy.js --network sepolia

verify:
	npx hardhat verify --network sepolia $(ADDRESS)

clean:
	npx hardhat clean
	rm -rf cache artifacts

node:
	npx hardhat node

help:
	@echo "Available targets:"
	@echo "  install       - Install dependencies"
	@echo "  compile       - Compile contracts"
	@echo "  test          - Run tests"
	@echo "  coverage      - Generate coverage report"
	@echo "  deploy-local  - Deploy to local network"
	@echo "  deploy-sepolia- Deploy to Sepolia testnet"
	@echo "  verify        - Verify contract on Etherscan"
	@echo "  clean         - Clean build artifacts"
	@echo "  node          - Start local Hardhat node"
