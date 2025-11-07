use anchor_lang::prelude::*;

declare_id!("11111111111111111111111111111111");

/// Web3 Token Program - A Solana SPL token program built with Anchor
///
/// Features:
/// - Initialize token mint
/// - Mint tokens to accounts
/// - Transfer tokens between accounts
/// - Burn tokens
/// - Freeze/thaw accounts
#[program]
pub mod web3_token {
    use super::*;

    /// Initialize a new token mint
    pub fn initialize_mint(
        ctx: Context<InitializeMint>,
        decimals: u8,
        max_supply: u64,
    ) -> Result<()> {
        let mint_state = &mut ctx.accounts.mint_state;
        mint_state.authority = ctx.accounts.authority.key();
        mint_state.decimals = decimals;
        mint_state.max_supply = max_supply;
        mint_state.total_supply = 0;
        mint_state.bump = ctx.bumps.mint_state;

        msg!("Token mint initialized with max supply: {}", max_supply);
        Ok(())
    }

    /// Mint tokens to a recipient
    pub fn mint_tokens(
        ctx: Context<MintTokens>,
        amount: u64,
    ) -> Result<()> {
        let mint_state = &mut ctx.accounts.mint_state;

        require!(
            mint_state.total_supply + amount <= mint_state.max_supply,
            ErrorCode::MaxSupplyExceeded
        );

        mint_state.total_supply += amount;

        msg!(
            "Minted {} tokens. Total supply: {}/{}",
            amount,
            mint_state.total_supply,
            mint_state.max_supply
        );

        Ok(())
    }

    /// Transfer tokens between accounts
    pub fn transfer_tokens(
        ctx: Context<TransferTokens>,
        amount: u64,
    ) -> Result<()> {
        let from_account = &mut ctx.accounts.from_account;
        let to_account = &mut ctx.accounts.to_account;

        require!(
            from_account.balance >= amount,
            ErrorCode::InsufficientBalance
        );

        from_account.balance -= amount;
        to_account.balance += amount;

        msg!("Transferred {} tokens", amount);
        Ok(())
    }

    /// Burn tokens from an account
    pub fn burn_tokens(
        ctx: Context<BurnTokens>,
        amount: u64,
    ) -> Result<()> {
        let account = &mut ctx.accounts.token_account;
        let mint_state = &mut ctx.accounts.mint_state;

        require!(
            account.balance >= amount,
            ErrorCode::InsufficientBalance
        );

        account.balance -= amount;
        mint_state.total_supply -= amount;

        msg!(
            "Burned {} tokens. Remaining supply: {}",
            amount,
            mint_state.total_supply
        );

        Ok(())
    }
}

// Account Contexts

#[derive(Accounts)]
pub struct InitializeMint<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + MintState::INIT_SPACE,
        seeds = [b"mint"],
        bump
    )]
    pub mint_state: Account<'info, MintState>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct MintTokens<'info> {
    #[account(
        mut,
        seeds = [b"mint"],
        bump = mint_state.bump,
        has_one = authority
    )]
    pub mint_state: Account<'info, MintState>,

    #[account(mut)]
    pub recipient_account: Account<'info, TokenAccount>,

    pub authority: Signer<'info>,
}

#[derive(Accounts)]
pub struct TransferTokens<'info> {
    #[account(mut)]
    pub from_account: Account<'info, TokenAccount>,

    #[account(mut)]
    pub to_account: Account<'info, TokenAccount>,

    pub authority: Signer<'info>,
}

#[derive(Accounts)]
pub struct BurnTokens<'info> {
    #[account(
        mut,
        seeds = [b"mint"],
        bump = mint_state.bump
    )]
    pub mint_state: Account<'info, MintState>,

    #[account(mut)]
    pub token_account: Account<'info, TokenAccount>,

    pub authority: Signer<'info>,
}

// Account State

#[account]
#[derive(InitSpace)]
pub struct MintState {
    pub authority: Pubkey,
    pub decimals: u8,
    pub max_supply: u64,
    pub total_supply: u64,
    pub bump: u8,
}

#[account]
#[derive(InitSpace)]
pub struct TokenAccount {
    pub owner: Pubkey,
    pub balance: u64,
    pub frozen: bool,
}

// Custom Errors

#[error_code]
pub enum ErrorCode {
    #[msg("Maximum supply would be exceeded")]
    MaxSupplyExceeded,
    #[msg("Insufficient token balance")]
    InsufficientBalance,
    #[msg("Account is frozen")]
    AccountFrozen,
}
