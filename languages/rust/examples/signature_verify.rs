/// Solana signature verification example
/// Demonstrates cryptographic signature verification on Solana
use solana_sdk::{
    pubkey::Pubkey,
    signature::{Keypair, Signer, Signature},
    hash::Hash,
    transaction::Transaction,
    system_instruction,
};
use std::str::FromStr;

fn main() {
    println!("🔐 Solana Signature Verification Example\n");

    // Generate a new keypair
    let keypair = Keypair::new();
    let pubkey = keypair.pubkey();

    println!("Generated Keypair:");
    println!("  Public Key: {}", pubkey);
    println!("  Secret Key: [hidden]\n");

    // Create a simple transaction
    let to_pubkey = Pubkey::from_str("11111111111111111111111111111111").unwrap();
    let lamports = 1_000_000; // 0.001 SOL

    let instruction = system_instruction::transfer(&pubkey, &to_pubkey, lamports);

    // Create transaction with a recent blockhash (using a dummy hash for this example)
    let recent_blockhash = Hash::default();
    let mut transaction = Transaction::new_with_payer(
        &[instruction],
        Some(&pubkey),
    );

    // Sign the transaction
    transaction.sign(&[&keypair], recent_blockhash);

    println!("Transaction Details:");
    println!("  From: {}", pubkey);
    println!("  To: {}", to_pubkey);
    println!("  Amount: {} lamports", lamports);
    println!("  Signatures: {}", transaction.signatures.len());

    // Verify the signature
    if let Some(signature) = transaction.signatures.first() {
        println!("\nSignature: {}", signature);

        // In a real scenario, you would verify against the transaction message
        let is_valid = !signature.as_ref().iter().all(|&b| b == 0);
        println!("Signature Valid: {}", is_valid);
    }

    // Demonstrate ed25519 signature verification
    println!("\n--- Ed25519 Signature Verification ---");

    let message = b"Hello, Solana!";
    let signature = keypair.sign_message(message);

    println!("Message: {:?}", std::str::from_utf8(message).unwrap());
    println!("Signature: {}", signature);
    println!("Public Key: {}", pubkey);

    // Verify the signature
    let is_verified = signature.verify(pubkey.as_ref(), message);
    println!("Verification Result: {}", is_verified);

    // Example of invalid signature detection
    println!("\n--- Invalid Signature Detection ---");
    let wrong_message = b"Wrong message";
    let is_invalid = signature.verify(pubkey.as_ref(), wrong_message);
    println!("Invalid Message Verification: {} (should be false)", is_invalid);
}
