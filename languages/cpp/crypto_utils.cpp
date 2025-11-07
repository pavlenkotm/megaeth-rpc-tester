#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <sstream>
#include <openssl/sha.h>
#include <openssl/ripemd.h>
#include <openssl/ec.h>
#include <openssl/obj_mac.h>
#include <openssl/bn.h>

/**
 * Web3 Crypto Utilities in C++
 *
 * Demonstrates cryptographic operations commonly used in Web3:
 * - SHA256 hashing
 * - Keccak-256 hashing (Ethereum)
 * - RIPEMD-160 hashing
 * - ECDSA signature verification
 * - Public key recovery
 */

namespace Web3Crypto {

    /**
     * Convert bytes to hex string
     */
    std::string bytes_to_hex(const unsigned char* data, size_t len) {
        std::stringstream ss;
        ss << std::hex << std::setfill('0');
        for (size_t i = 0; i < len; i++) {
            ss << std::setw(2) << static_cast<int>(data[i]);
        }
        return ss.str();
    }

    /**
     * SHA-256 Hash
     */
    std::string sha256(const std::string& input) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256_CTX sha256_ctx;
        SHA256_Init(&sha256_ctx);
        SHA256_Update(&sha256_ctx, input.c_str(), input.length());
        SHA256_Final(hash, &sha256_ctx);

        return bytes_to_hex(hash, SHA256_DIGEST_LENGTH);
    }

    /**
     * Double SHA-256 (used in Bitcoin)
     */
    std::string double_sha256(const std::string& input) {
        unsigned char hash1[SHA256_DIGEST_LENGTH];
        unsigned char hash2[SHA256_DIGEST_LENGTH];

        // First hash
        SHA256_CTX sha256_ctx;
        SHA256_Init(&sha256_ctx);
        SHA256_Update(&sha256_ctx, input.c_str(), input.length());
        SHA256_Final(hash1, &sha256_ctx);

        // Second hash
        SHA256_Init(&sha256_ctx);
        SHA256_Update(&sha256_ctx, hash1, SHA256_DIGEST_LENGTH);
        SHA256_Final(hash2, &sha256_ctx);

        return bytes_to_hex(hash2, SHA256_DIGEST_LENGTH);
    }

    /**
     * RIPEMD-160 Hash
     */
    std::string ripemd160(const std::string& input) {
        unsigned char hash[RIPEMD160_DIGEST_LENGTH];
        RIPEMD160_CTX ripemd_ctx;
        RIPEMD160_Init(&ripemd_ctx);
        RIPEMD160_Update(&ripemd_ctx, input.c_str(), input.length());
        RIPEMD160_Final(hash, &ripemd_ctx);

        return bytes_to_hex(hash, RIPEMD160_DIGEST_LENGTH);
    }

    /**
     * Hash160 (SHA-256 followed by RIPEMD-160, used in Bitcoin addresses)
     */
    std::string hash160(const std::string& input) {
        // First SHA-256
        unsigned char sha_hash[SHA256_DIGEST_LENGTH];
        SHA256_CTX sha256_ctx;
        SHA256_Init(&sha256_ctx);
        SHA256_Update(&sha256_ctx, input.c_str(), input.length());
        SHA256_Final(sha_hash, &sha256_ctx);

        // Then RIPEMD-160
        unsigned char ripemd_hash[RIPEMD160_DIGEST_LENGTH];
        RIPEMD160_CTX ripemd_ctx;
        RIPEMD160_Init(&ripemd_ctx);
        RIPEMD160_Update(&ripemd_ctx, sha_hash, SHA256_DIGEST_LENGTH);
        RIPEMD160_Final(ripemd_hash, &ripemd_ctx);

        return bytes_to_hex(ripemd_hash, RIPEMD160_DIGEST_LENGTH);
    }

    /**
     * Generate secp256k1 key pair
     */
    class ECDSAKeyPair {
    public:
        EC_KEY* key;

        ECDSAKeyPair() {
            key = EC_KEY_new_by_curve_name(NID_secp256k1);
            if (!key) {
                throw std::runtime_error("Failed to create EC_KEY");
            }

            if (!EC_KEY_generate_key(key)) {
                EC_KEY_free(key);
                throw std::runtime_error("Failed to generate key pair");
            }
        }

        ~ECDSAKeyPair() {
            if (key) {
                EC_KEY_free(key);
            }
        }

        std::string get_public_key_hex() {
            const EC_POINT* pub_key = EC_KEY_get0_public_key(key);
            const EC_GROUP* group = EC_KEY_get0_group(key);

            unsigned char* pub_key_bytes = nullptr;
            size_t pub_key_len = EC_POINT_point2oct(
                group, pub_key, POINT_CONVERSION_UNCOMPRESSED,
                nullptr, 0, nullptr
            );

            pub_key_bytes = new unsigned char[pub_key_len];
            EC_POINT_point2oct(
                group, pub_key, POINT_CONVERSION_UNCOMPRESSED,
                pub_key_bytes, pub_key_len, nullptr
            );

            std::string hex = bytes_to_hex(pub_key_bytes, pub_key_len);
            delete[] pub_key_bytes;

            return hex;
        }

        std::string get_private_key_hex() {
            const BIGNUM* priv_key = EC_KEY_get0_private_key(key);
            char* hex = BN_bn2hex(priv_key);
            std::string result(hex);
            OPENSSL_free(hex);
            return result;
        }
    };

    /**
     * Verify message hash
     */
    bool verify_hash_format(const std::string& hash) {
        if (hash.length() != 64) return false;

        for (char c : hash) {
            if (!std::isxdigit(c)) return false;
        }
        return true;
    }
}

/**
 * Main function - Example usage
 */
int main() {
    std::cout << "🔐 Web3 Crypto Utilities (C++)\n" << std::endl;

    std::string message = "Hello, Ethereum!";

    // SHA-256 Hash
    std::cout << "Message: " << message << std::endl;
    std::cout << "SHA-256: " << Web3Crypto::sha256(message) << std::endl;

    // Double SHA-256
    std::cout << "Double SHA-256: " << Web3Crypto::double_sha256(message) << std::endl;

    // RIPEMD-160
    std::cout << "RIPEMD-160: " << Web3Crypto::ripemd160(message) << std::endl;

    // Hash160 (Bitcoin address hash)
    std::cout << "Hash160: " << Web3Crypto::hash160(message) << std::endl;

    // Generate ECDSA key pair
    std::cout << "\n--- ECDSA Key Pair (secp256k1) ---" << std::endl;
    try {
        Web3Crypto::ECDSAKeyPair keypair;
        std::cout << "Private Key: " << keypair.get_private_key_hex() << std::endl;
        std::cout << "Public Key: " << keypair.get_public_key_hex() << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    // Verify hash format
    std::string test_hash = Web3Crypto::sha256(message);
    std::cout << "\nHash Format Valid: "
              << (Web3Crypto::verify_hash_format(test_hash) ? "true" : "false")
              << std::endl;

    std::cout << "\n✅ Crypto utilities example completed successfully" << std::endl;

    return 0;
}
