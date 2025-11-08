import Array "mo:base/Array";
import HashMap "mo:base/HashMap";
import Hash "mo:base/Hash";
import Iter "mo:base/Iter";
import Nat "mo:base/Nat";
import Option "mo:base/Option";
import Principal "mo:base/Principal";
import Result "mo:base/Result";
import Text "mo:base/Text";

actor Token {
    type Account = Principal;
    type Balance = Nat;
    type TransferArgs = {
        from: Account;
        to: Account;
        amount: Balance;
    };

    private stable var totalSupply_ : Balance = 0;
    private stable var name_ : Text = "Internet Computer Token";
    private stable var symbol_ : Text = "ICT";
    private stable var decimals_ : Nat8 = 8;

    private var balances = HashMap.HashMap<Account, Balance>(
        10,
        Principal.equal,
        Principal.hash
    );

    // Initialize with some supply
    private stable var owner : Principal = Principal.fromText("2vxsx-fae");

    // Get token name
    public query func name() : async Text {
        name_
    };

    // Get token symbol
    public query func symbol() : async Text {
        symbol_
    };

    // Get decimals
    public query func decimals() : async Nat8 {
        decimals_
    };

    // Get total supply
    public query func totalSupply() : async Balance {
        totalSupply_
    };

    // Get balance of an account
    public query func balanceOf(account : Account) : async Balance {
        switch (balances.get(account)) {
            case (?balance) { balance };
            case null { 0 };
        }
    };

    // Transfer tokens
    public shared(msg) func transfer(to : Account, amount : Balance) : async Result.Result<(), Text> {
        let from = msg.caller;

        let fromBalance = switch (balances.get(from)) {
            case (?balance) { balance };
            case null { 0 };
        };

        if (fromBalance < amount) {
            return #err("Insufficient balance");
        };

        let toBalance = switch (balances.get(to)) {
            case (?balance) { balance };
            case null { 0 };
        };

        balances.put(from, fromBalance - amount);
        balances.put(to, toBalance + amount);

        #ok(())
    };

    // Mint new tokens (only owner)
    public shared(msg) func mint(to : Account, amount : Balance) : async Result.Result<(), Text> {
        if (msg.caller != owner) {
            return #err("Only owner can mint");
        };

        let toBalance = switch (balances.get(to)) {
            case (?balance) { balance };
            case null { 0 };
        };

        balances.put(to, toBalance + amount);
        totalSupply_ += amount;

        #ok(())
    };

    // Burn tokens
    public shared(msg) func burn(amount : Balance) : async Result.Result<(), Text> {
        let from = msg.caller;

        let fromBalance = switch (balances.get(from)) {
            case (?balance) { balance };
            case null { 0 };
        };

        if (fromBalance < amount) {
            return #err("Insufficient balance");
        };

        balances.put(from, fromBalance - amount);
        totalSupply_ -= amount;

        #ok(())
    };
}
