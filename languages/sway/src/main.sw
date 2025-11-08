contract;

use std::{
    auth::msg_sender,
    call_frames::msg_asset_id,
    context::msg_amount,
    hash::Hash,
    storage::storage_map::*,
    token::*,
};

storage {
    total_supply: u64 = 0,
    balances: StorageMap<Identity, u64> = StorageMap {},
    name: str[10] = __to_str_array("FuelToken"),
    symbol: str[4] = __to_str_array("FUEL"),
}

abi Token {
    #[storage(read, write)]
    fn mint(amount: u64);

    #[storage(read, write)]
    fn burn(amount: u64);

    #[storage(read, write)]
    fn transfer(recipient: Identity, amount: u64);

    #[storage(read)]
    fn balance_of(account: Identity) -> u64;

    #[storage(read)]
    fn total_supply() -> u64;

    #[storage(read)]
    fn name() -> str[10];

    #[storage(read)]
    fn symbol() -> str[4];
}

impl Token for Contract {
    #[storage(read, write)]
    fn mint(amount: u64) {
        let sender = msg_sender().unwrap();

        // Update total supply
        storage.total_supply.write(storage.total_supply.read() + amount);

        // Update balance
        let current_balance = storage.balances.get(sender).try_read().unwrap_or(0);
        storage.balances.insert(sender, current_balance + amount);

        // Mint tokens
        mint_to(sender, DEFAULT_SUB_ID, amount);
    }

    #[storage(read, write)]
    fn burn(amount: u64) {
        let sender = msg_sender().unwrap();
        let current_balance = storage.balances.get(sender).read();

        require(current_balance >= amount, "Insufficient balance");

        // Update total supply
        storage.total_supply.write(storage.total_supply.read() - amount);

        // Update balance
        storage.balances.insert(sender, current_balance - amount);

        // Burn tokens
        burn(DEFAULT_SUB_ID, amount);
    }

    #[storage(read, write)]
    fn transfer(recipient: Identity, amount: u64) {
        let sender = msg_sender().unwrap();
        let sender_balance = storage.balances.get(sender).read();

        require(sender_balance >= amount, "Insufficient balance");

        // Update sender balance
        storage.balances.insert(sender, sender_balance - amount);

        // Update recipient balance
        let recipient_balance = storage.balances.get(recipient).try_read().unwrap_or(0);
        storage.balances.insert(recipient, recipient_balance + amount);

        // Transfer tokens
        transfer(recipient, DEFAULT_SUB_ID, amount);
    }

    #[storage(read)]
    fn balance_of(account: Identity) -> u64 {
        storage.balances.get(account).try_read().unwrap_or(0)
    }

    #[storage(read)]
    fn total_supply() -> u64 {
        storage.total_supply.read()
    }

    #[storage(read)]
    fn name() -> str[10] {
        storage.name.read()
    }

    #[storage(read)]
    fn symbol() -> str[4] {
        storage.symbol.read()
    }
}
