.PHONY: build test deploy clean fmt clippy

build:
	anchor build

test:
	anchor test

deploy-devnet:
	anchor deploy --provider.cluster devnet

deploy-mainnet:
	anchor deploy --provider.cluster mainnet

clean:
	anchor clean
	cargo clean

fmt:
	cargo fmt

clippy:
	cargo clippy -- -D warnings

check:
	cargo check

run-example:
	cargo run --example signature_verify

help:
	@echo "Available targets:"
	@echo "  build          - Build Anchor program"
	@echo "  test           - Run tests"
	@echo "  deploy-devnet  - Deploy to devnet"
	@echo "  deploy-mainnet - Deploy to mainnet"
	@echo "  clean          - Clean build artifacts"
	@echo "  fmt            - Format code"
	@echo "  clippy         - Run clippy linter"
	@echo "  check          - Check code compilation"
	@echo "  run-example    - Run signature verify example"
