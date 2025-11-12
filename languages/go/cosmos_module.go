package main

import (
	"encoding/json"
	"fmt"

	sdk "github.com/cosmos/cosmos-sdk/types"
	"github.com/cosmos/cosmos-sdk/types/module"
	"github.com/cosmos/cosmos-sdk/x/bank/keeper"
	banktypes "github.com/cosmos/cosmos-sdk/x/bank/types"
)

/*
   Cosmos SDK Module Example

   This file demonstrates building a custom Cosmos SDK module
   for blockchain applications. Cosmos SDK is used by chains like
   Cosmos Hub, Osmosis, Terra, and many others.
*/

// ModuleName defines the module name
const ModuleName = "customtoken"

// StoreKey is the store key string for the module
const StoreKey = ModuleName

// TokenKeeper manages custom token operations
type TokenKeeper struct {
	storeKey   sdk.StoreKey
	bankKeeper keeper.Keeper
	cdc        codec.BinaryCodec
}

// NewTokenKeeper creates a new TokenKeeper
func NewTokenKeeper(
	storeKey sdk.StoreKey,
	bankKeeper keeper.Keeper,
	cdc codec.BinaryCodec,
) TokenKeeper {
	return TokenKeeper{
		storeKey:   storeKey,
		bankKeeper: bankKeeper,
		cdc:        cdc,
	}
}

// Token represents a custom token on Cosmos
type Token struct {
	Denom       string         `json:"denom"`
	TotalSupply sdk.Int        `json:"total_supply"`
	Owner       sdk.AccAddress `json:"owner"`
	Mintable    bool           `json:"mintable"`
}

// MsgCreateToken defines a message to create a new token
type MsgCreateToken struct {
	Creator     sdk.AccAddress `json:"creator"`
	Denom       string         `json:"denom"`
	TotalSupply sdk.Int        `json:"total_supply"`
	Mintable    bool           `json:"mintable"`
}

// Route implements sdk.Msg
func (msg MsgCreateToken) Route() string {
	return ModuleName
}

// Type implements sdk.Msg
func (msg MsgCreateToken) Type() string {
	return "create_token"
}

// ValidateBasic implements sdk.Msg
func (msg MsgCreateToken) ValidateBasic() error {
	if msg.Creator.Empty() {
		return fmt.Errorf("creator address cannot be empty")
	}
	if msg.Denom == "" {
		return fmt.Errorf("denom cannot be empty")
	}
	if !msg.TotalSupply.IsPositive() {
		return fmt.Errorf("total supply must be positive")
	}
	return nil
}

// GetSignBytes implements sdk.Msg
func (msg MsgCreateToken) GetSignBytes() []byte {
	bz, _ := json.Marshal(msg)
	return sdk.MustSortJSON(bz)
}

// GetSigners implements sdk.Msg
func (msg MsgCreateToken) GetSigners() []sdk.AccAddress {
	return []sdk.AccAddress{msg.Creator}
}

// MsgMintToken defines a message to mint tokens
type MsgMintToken struct {
	Minter sdk.AccAddress `json:"minter"`
	Denom  string         `json:"denom"`
	Amount sdk.Int        `json:"amount"`
	To     sdk.AccAddress `json:"to"`
}

// Route implements sdk.Msg
func (msg MsgMintToken) Route() string {
	return ModuleName
}

// Type implements sdk.Msg
func (msg MsgMintToken) Type() string {
	return "mint_token"
}

// ValidateBasic implements sdk.Msg
func (msg MsgMintToken) ValidateBasic() error {
	if msg.Minter.Empty() {
		return fmt.Errorf("minter address cannot be empty")
	}
	if msg.To.Empty() {
		return fmt.Errorf("recipient address cannot be empty")
	}
	if msg.Denom == "" {
		return fmt.Errorf("denom cannot be empty")
	}
	if !msg.Amount.IsPositive() {
		return fmt.Errorf("amount must be positive")
	}
	return nil
}

// GetSignBytes implements sdk.Msg
func (msg MsgMintToken) GetSignBytes() []byte {
	bz, _ := json.Marshal(msg)
	return sdk.MustSortJSON(bz)
}

// GetSigners implements sdk.Msg
func (msg MsgMintToken) GetSigners() []sdk.AccAddress {
	return []sdk.AccAddress{msg.Minter}
}

// CreateToken creates a new token in the module
func (k TokenKeeper) CreateToken(ctx sdk.Context, msg MsgCreateToken) error {
	// Create token metadata
	token := Token{
		Denom:       msg.Denom,
		TotalSupply: msg.TotalSupply,
		Owner:       msg.Creator,
		Mintable:    msg.Mintable,
	}

	// Store token metadata
	store := ctx.KVStore(k.storeKey)
	bz := k.cdc.MustMarshal(&token)
	store.Set([]byte(msg.Denom), bz)

	// Mint initial supply to creator
	coins := sdk.NewCoins(sdk.NewCoin(msg.Denom, msg.TotalSupply))
	if err := k.bankKeeper.MintCoins(ctx, ModuleName, coins); err != nil {
		return err
	}

	// Send to creator
	if err := k.bankKeeper.SendCoinsFromModuleToAccount(
		ctx, ModuleName, msg.Creator, coins,
	); err != nil {
		return err
	}

	return nil
}

// MintToken mints additional tokens (if allowed)
func (k TokenKeeper) MintToken(ctx sdk.Context, msg MsgMintToken) error {
	// Get token metadata
	store := ctx.KVStore(k.storeKey)
	bz := store.Get([]byte(msg.Denom))
	if bz == nil {
		return fmt.Errorf("token %s does not exist", msg.Denom)
	}

	var token Token
	k.cdc.MustUnmarshal(bz, &token)

	// Check if minting is allowed
	if !token.Mintable {
		return fmt.Errorf("token %s is not mintable", msg.Denom)
	}

	// Check if minter is owner
	if !token.Owner.Equals(msg.Minter) {
		return fmt.Errorf("only owner can mint tokens")
	}

	// Mint tokens
	coins := sdk.NewCoins(sdk.NewCoin(msg.Denom, msg.Amount))
	if err := k.bankKeeper.MintCoins(ctx, ModuleName, coins); err != nil {
		return err
	}

	// Send to recipient
	if err := k.bankKeeper.SendCoinsFromModuleToAccount(
		ctx, ModuleName, msg.To, coins,
	); err != nil {
		return err
	}

	// Update total supply
	token.TotalSupply = token.TotalSupply.Add(msg.Amount)
	bz = k.cdc.MustMarshal(&token)
	store.Set([]byte(msg.Denom), bz)

	return nil
}

// GetToken retrieves token metadata
func (k TokenKeeper) GetToken(ctx sdk.Context, denom string) (*Token, error) {
	store := ctx.KVStore(k.storeKey)
	bz := store.Get([]byte(denom))
	if bz == nil {
		return nil, fmt.Errorf("token %s not found", denom)
	}

	var token Token
	k.cdc.MustUnmarshal(bz, &token)
	return &token, nil
}

// Example: Query all tokens
func (k TokenKeeper) GetAllTokens(ctx sdk.Context) []Token {
	store := ctx.KVStore(k.storeKey)
	iterator := sdk.KVStorePrefixIterator(store, []byte{})
	defer iterator.Close()

	var tokens []Token
	for ; iterator.Valid(); iterator.Next() {
		var token Token
		k.cdc.MustUnmarshal(iterator.Value(), &token)
		tokens = append(tokens, token)
	}

	return tokens
}

// AppModule implements the module.AppModule interface
type AppModule struct {
	keeper TokenKeeper
}

// NewAppModule creates a new AppModule object
func NewAppModule(keeper TokenKeeper) AppModule {
	return AppModule{
		keeper: keeper,
	}
}

// Name returns the module's name
func (AppModule) Name() string {
	return ModuleName
}

// RegisterInvariants registers the module's invariants
func (am AppModule) RegisterInvariants(ir sdk.InvariantRegistry) {}

// Example usage demonstration
func ExampleCosmosModule() {
	fmt.Println("=== Cosmos SDK Module Example ===")
	fmt.Println()
	fmt.Println("This module demonstrates:")
	fmt.Println("1. Creating custom tokens on Cosmos chains")
	fmt.Println("2. Minting tokens (if mintable)")
	fmt.Println("3. Querying token metadata")
	fmt.Println("4. Integration with bank keeper for transfers")
	fmt.Println()
	fmt.Println("Compatible with: Cosmos Hub, Osmosis, Terra, Juno, etc.")
}
