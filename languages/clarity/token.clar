;; SIP-010 Fungible Token Implementation
;; A standard fungible token contract for Stacks blockchain

(impl-trait 'SP3FBR2AGK5H9QBDH3EEN6DF8EK8JY7RX8QJ5SVTE.sip-010-trait-ft-standard.sip-010-trait)

;; Define the token
(define-fungible-token stack-token)

;; Constants
(define-constant contract-owner tx-sender)
(define-constant err-owner-only (err u100))
(define-constant err-not-token-owner (err u101))
(define-constant err-insufficient-balance (err u102))

;; Token metadata
(define-data-var token-name (string-ascii 32) "StackToken")
(define-data-var token-symbol (string-ascii 10) "STK")
(define-data-var token-decimals uint u8)
(define-data-var token-uri (optional (string-utf8 256)) none)

;; SIP-010 Functions

;; Transfer tokens
(define-public (transfer (amount uint) (sender principal) (recipient principal) (memo (optional (buff 34))))
  (begin
    (asserts! (is-eq tx-sender sender) err-not-token-owner)
    (try! (ft-transfer? stack-token amount sender recipient))
    (match memo to-print (print to-print) 0x)
    (ok true)
  )
)

;; Get token name
(define-read-only (get-name)
  (ok (var-get token-name))
)

;; Get token symbol
(define-read-only (get-symbol)
  (ok (var-get token-symbol))
)

;; Get decimals
(define-read-only (get-decimals)
  (ok (var-get token-decimals))
)

;; Get balance of account
(define-read-only (get-balance (account principal))
  (ok (ft-get-balance stack-token account))
)

;; Get total supply
(define-read-only (get-total-supply)
  (ok (ft-get-supply stack-token))
)

;; Get token URI
(define-read-only (get-token-uri)
  (ok (var-get token-uri))
)

;; Mint tokens (owner only)
(define-public (mint (amount uint) (recipient principal))
  (begin
    (asserts! (is-eq tx-sender contract-owner) err-owner-only)
    (ft-mint? stack-token amount recipient)
  )
)

;; Burn tokens
(define-public (burn (amount uint) (sender principal))
  (begin
    (asserts! (is-eq tx-sender sender) err-not-token-owner)
    (ft-burn? stack-token amount sender)
  )
)

;; Set token URI (owner only)
(define-public (set-token-uri (new-uri (string-utf8 256)))
  (begin
    (asserts! (is-eq tx-sender contract-owner) err-owner-only)
    (ok (var-set token-uri (some new-uri)))
  )
)

;; Initialize with supply
(begin
  (try! (ft-mint? stack-token u1000000000000 contract-owner))
)
