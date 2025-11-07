/// Simple Token Module for Aptos/Sui
/// Demonstrates Move language patterns for Web3 development
module web3_examples::simple_token {
    use std::signer;
    use std::string::String;
    use aptos_framework::coin::{Self, Coin, MintCapability, BurnCapability};
    use aptos_framework::event;

    /// Error codes
    const E_NOT_AUTHORIZED: u64 = 1;
    const E_INSUFFICIENT_BALANCE: u64 = 2;
    const E_MAX_SUPPLY_EXCEEDED: u64 = 3;

    /// Token metadata structure
    struct TokenMetadata has key {
        name: String,
        symbol: String,
        decimals: u8,
        max_supply: u64,
        total_supply: u64,
    }

    /// Capability holders
    struct Capabilities has key {
        mint_cap: MintCapability<SimpleToken>,
        burn_cap: BurnCapability<SimpleToken>,
    }

    /// The token type marker
    struct SimpleToken {}

    /// Events
    struct MintEvent has drop, store {
        amount: u64,
        recipient: address,
    }

    struct BurnEvent has drop, store {
        amount: u64,
        from: address,
    }

    struct TransferEvent has drop, store {
        amount: u64,
        from: address,
        to: address,
    }

    /// Event handles
    struct TokenEvents has key {
        mint_events: event::EventHandle<MintEvent>,
        burn_events: event::EventHandle<BurnEvent>,
        transfer_events: event::EventHandle<TransferEvent>,
    }

    /// Initialize the token
    public entry fun initialize(
        account: &signer,
        name: vector<u8>,
        symbol: vector<u8>,
        decimals: u8,
        max_supply: u64,
    ) {
        let account_addr = signer::address_of(account);

        // Initialize the coin
        let (burn_cap, freeze_cap, mint_cap) = coin::initialize<SimpleToken>(
            account,
            string::utf8(name),
            string::utf8(symbol),
            decimals,
            true, // monitor_supply
        );

        // Destroy freeze capability (we don't use it)
        coin::destroy_freeze_cap(freeze_cap);

        // Store capabilities
        move_to(account, Capabilities {
            mint_cap,
            burn_cap,
        });

        // Store metadata
        move_to(account, TokenMetadata {
            name: string::utf8(name),
            symbol: string::utf8(symbol),
            decimals,
            max_supply,
            total_supply: 0,
        });

        // Initialize events
        move_to(account, TokenEvents {
            mint_events: event::new_event_handle<MintEvent>(account),
            burn_events: event::new_event_handle<BurnEvent>(account),
            transfer_events: event::new_event_handle<TransferEvent>(account),
        });
    }

    /// Mint new tokens
    public entry fun mint(
        admin: &signer,
        recipient: address,
        amount: u64,
    ) acquires Capabilities, TokenMetadata, TokenEvents {
        let admin_addr = signer::address_of(admin);

        // Get capabilities and metadata
        let caps = borrow_global<Capabilities>(admin_addr);
        let metadata = borrow_global_mut<TokenMetadata>(admin_addr);

        // Check max supply
        assert!(
            metadata.total_supply + amount <= metadata.max_supply,
            E_MAX_SUPPLY_EXCEEDED
        );

        // Mint coins
        let coins = coin::mint<SimpleToken>(amount, &caps.mint_cap);

        // Update total supply
        metadata.total_supply = metadata.total_supply + amount;

        // Deposit to recipient
        coin::deposit(recipient, coins);

        // Emit event
        let events = borrow_global_mut<TokenEvents>(admin_addr);
        event::emit_event(&mut events.mint_events, MintEvent {
            amount,
            recipient,
        });
    }

    /// Burn tokens
    public entry fun burn(
        account: &signer,
        amount: u64,
    ) acquires Capabilities, TokenMetadata, TokenEvents {
        let account_addr = signer::address_of(account);

        // Withdraw coins from account
        let coins = coin::withdraw<SimpleToken>(account, amount);

        // Get burn capability
        let caps = borrow_global<Capabilities>(account_addr);

        // Burn the coins
        coin::burn(coins, &caps.burn_cap);

        // Update metadata
        let metadata = borrow_global_mut<TokenMetadata>(account_addr);
        metadata.total_supply = metadata.total_supply - amount;

        // Emit event
        let events = borrow_global_mut<TokenEvents>(account_addr);
        event::emit_event(&mut events.burn_events, BurnEvent {
            amount,
            from: account_addr,
        });
    }

    /// Transfer tokens
    public entry fun transfer(
        from: &signer,
        to: address,
        amount: u64,
    ) acquires TokenEvents {
        let from_addr = signer::address_of(from);

        // Transfer coins
        coin::transfer<SimpleToken>(from, to, amount);

        // Emit event
        let events = borrow_global_mut<TokenEvents>(from_addr);
        event::emit_event(&mut events.transfer_events, TransferEvent {
            amount,
            from: from_addr,
            to,
        });
    }

    /// Get balance of an account
    public fun balance_of(account: address): u64 {
        coin::balance<SimpleToken>(account)
    }

    /// Get total supply
    public fun total_supply(admin: address): u64 acquires TokenMetadata {
        borrow_global<TokenMetadata>(admin).total_supply
    }

    /// Get remaining supply
    public fun remaining_supply(admin: address): u64 acquires TokenMetadata {
        let metadata = borrow_global<TokenMetadata>(admin);
        metadata.max_supply - metadata.total_supply
    }

    #[test_only]
    use aptos_framework::account;

    #[test(admin = @0x1, user = @0x2)]
    public fun test_mint_and_transfer(admin: &signer, user: &signer) acquires Capabilities, TokenMetadata, TokenEvents {
        // Setup
        account::create_account_for_test(signer::address_of(admin));
        account::create_account_for_test(signer::address_of(user));

        // Initialize token
        initialize(admin, b"Test Token", b"TEST", 8, 1000000);

        // Mint tokens
        mint(admin, signer::address_of(admin), 1000);

        // Check balance
        assert!(balance_of(signer::address_of(admin)) == 1000, 0);

        // Transfer
        transfer(admin, signer::address_of(user), 500);

        // Verify balances
        assert!(balance_of(signer::address_of(admin)) == 500, 1);
        assert!(balance_of(signer::address_of(user)) == 500, 2);
    }
}
