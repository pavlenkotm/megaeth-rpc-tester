import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Web3Token } from "../target/types/web3_token";
import { expect } from "chai";

describe("web3-token", () => {
  // Configure the client to use the local cluster
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.Web3Token as Program<Web3Token>;

  let mintPda: anchor.web3.PublicKey;
  let tokenAccountPda: anchor.web3.PublicKey;
  let authority = provider.wallet.publicKey;

  it("Initializes the token mint", async () => {
    const decimals = 9;

    [mintPda] = await anchor.web3.PublicKey.findProgramAddress(
      [Buffer.from("mint"), authority.toBuffer()],
      program.programId
    );

    const tx = await program.methods
      .initialize(decimals)
      .accounts({
        authority: authority,
        mint: mintPda,
        systemProgram: anchor.web3.SystemProgram.programId,
        tokenProgram: anchor.utils.token.TOKEN_PROGRAM_ID,
        rent: anchor.web3.SYSVAR_RENT_PUBKEY,
      })
      .rpc();

    console.log("Initialize transaction signature", tx);

    // Fetch mint account
    const mintAccount = await program.account.mint.fetch(mintPda);
    expect(mintAccount.authority.toString()).to.equal(authority.toString());
    expect(mintAccount.decimals).to.equal(decimals);
  });

  it("Mints tokens to a user account", async () => {
    const amount = new anchor.BN(1000000000); // 1 token with 9 decimals

    [tokenAccountPda] = await anchor.web3.PublicKey.findProgramAddress(
      [
        Buffer.from("token_account"),
        authority.toBuffer(),
        mintPda.toBuffer(),
      ],
      program.programId
    );

    const tx = await program.methods
      .mintTokens(amount)
      .accounts({
        authority: authority,
        mint: mintPda,
        tokenAccount: tokenAccountPda,
        tokenProgram: anchor.utils.token.TOKEN_PROGRAM_ID,
      })
      .rpc();

    console.log("Mint tokens transaction signature", tx);

    // Verify token balance
    const tokenAccount = await program.account.tokenAccount.fetch(
      tokenAccountPda
    );
    expect(tokenAccount.amount.toString()).to.equal(amount.toString());
  });

  it("Transfers tokens between accounts", async () => {
    const recipient = anchor.web3.Keypair.generate();
    const transferAmount = new anchor.BN(500000000); // 0.5 tokens

    const [recipientTokenAccount] =
      await anchor.web3.PublicKey.findProgramAddress(
        [
          Buffer.from("token_account"),
          recipient.publicKey.toBuffer(),
          mintPda.toBuffer(),
        ],
        program.programId
      );

    // Initialize recipient token account
    await program.methods
      .initializeTokenAccount()
      .accounts({
        authority: recipient.publicKey,
        mint: mintPda,
        tokenAccount: recipientTokenAccount,
        systemProgram: anchor.web3.SystemProgram.programId,
        tokenProgram: anchor.utils.token.TOKEN_PROGRAM_ID,
        rent: anchor.web3.SYSVAR_RENT_PUBKEY,
      })
      .signers([recipient])
      .rpc();

    // Transfer tokens
    const tx = await program.methods
      .transfer(transferAmount)
      .accounts({
        from: authority,
        to: recipient.publicKey,
        fromTokenAccount: tokenAccountPda,
        toTokenAccount: recipientTokenAccount,
        tokenProgram: anchor.utils.token.TOKEN_PROGRAM_ID,
      })
      .rpc();

    console.log("Transfer transaction signature", tx);

    // Verify balances
    const fromAccount = await program.account.tokenAccount.fetch(
      tokenAccountPda
    );
    const toAccount = await program.account.tokenAccount.fetch(
      recipientTokenAccount
    );

    expect(fromAccount.amount.toString()).to.equal("500000000");
    expect(toAccount.amount.toString()).to.equal(transferAmount.toString());
  });

  it("Burns tokens from user account", async () => {
    const burnAmount = new anchor.BN(250000000); // 0.25 tokens

    const beforeBalance = await program.account.tokenAccount.fetch(
      tokenAccountPda
    );

    const tx = await program.methods
      .burn(burnAmount)
      .accounts({
        authority: authority,
        mint: mintPda,
        tokenAccount: tokenAccountPda,
        tokenProgram: anchor.utils.token.TOKEN_PROGRAM_ID,
      })
      .rpc();

    console.log("Burn transaction signature", tx);

    // Verify reduced balance
    const afterBalance = await program.account.tokenAccount.fetch(
      tokenAccountPda
    );
    const expectedBalance = beforeBalance.amount.sub(burnAmount);
    expect(afterBalance.amount.toString()).to.equal(expectedBalance.toString());
  });

  it("Fails to mint with unauthorized account", async () => {
    const unauthorized = anchor.web3.Keypair.generate();
    const amount = new anchor.BN(1000000);

    try {
      await program.methods
        .mintTokens(amount)
        .accounts({
          authority: unauthorized.publicKey,
          mint: mintPda,
          tokenAccount: tokenAccountPda,
          tokenProgram: anchor.utils.token.TOKEN_PROGRAM_ID,
        })
        .signers([unauthorized])
        .rpc();

      expect.fail("Should have thrown an error");
    } catch (error) {
      expect(error).to.exist;
    }
  });
});
