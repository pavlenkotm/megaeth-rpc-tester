// Gas-Optimized ERC-20 Token in Pure Yul
object "Token" {
    code {
        // Constructor
        datacopy(0, dataoffset("runtime"), datasize("runtime"))
        return(0, datasize("runtime"))
    }

    object "runtime" {
        code {
            // Function selector dispatcher
            switch selector()

            // balanceOf(address)
            case 0x70a08231 {
                returnUint(balanceOf(decodeAsAddress(0)))
            }

            // transfer(address,uint256)
            case 0xa9059cbb {
                transfer(decodeAsAddress(0), decodeAsUint(1))
                returnTrue()
            }

            // totalSupply()
            case 0x18160ddd {
                returnUint(sload(0))
            }

            // mint(address,uint256)
            case 0x40c10f19 {
                mint(decodeAsAddress(0), decodeAsUint(1))
                returnTrue()
            }

            default {
                revert(0, 0)
            }

            // Helper functions
            function selector() -> s {
                s := div(calldataload(0), 0x100000000000000000000000000000000000000000000000000000000)
            }

            function decodeAsAddress(offset) -> v {
                v := decodeAsUint(offset)
                if iszero(iszero(and(v, not(0xffffffffffffffffffffffffffffffffffffffff)))) {
                    revert(0, 0)
                }
            }

            function decodeAsUint(offset) -> v {
                let pos := add(4, mul(offset, 0x20))
                if lt(calldatasize(), add(pos, 0x20)) {
                    revert(0, 0)
                }
                v := calldataload(pos)
            }

            function returnUint(v) {
                mstore(0, v)
                return(0, 0x20)
            }

            function returnTrue() {
                mstore(0, 1)
                return(0, 0x20)
            }

            // Storage layout
            // slot 0: total supply
            // keccak256(address, 1): balance of address

            function balanceOf(account) -> bal {
                let slot := accountToStorageSlot(account)
                bal := sload(slot)
            }

            function addToBalance(account, amount) {
                let slot := accountToStorageSlot(account)
                let bal := sload(slot)
                sstore(slot, safeAdd(bal, amount))
            }

            function deductFromBalance(account, amount) {
                let slot := accountToStorageSlot(account)
                let bal := sload(slot)
                require(gte(bal, amount))
                sstore(slot, sub(bal, amount))
            }

            function accountToStorageSlot(account) -> slot {
                mstore(0, account)
                mstore(0x20, 1)
                slot := keccak256(0, 0x40)
            }

            function transfer(to, amount) {
                let from := caller()
                deductFromBalance(from, amount)
                addToBalance(to, amount)
                emitTransfer(from, to, amount)
            }

            function mint(to, amount) {
                // In production, add access control here
                addToBalance(to, amount)

                // Update total supply
                let supply := sload(0)
                sstore(0, safeAdd(supply, amount))

                emitTransfer(0, to, amount)
            }

            function emitTransfer(from, to, amount) {
                mstore(0, amount)
                log3(0, 0x20,
                    // Transfer(address,address,uint256)
                    0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef,
                    from,
                    to
                )
            }

            function require(condition) {
                if iszero(condition) { revert(0, 0) }
            }

            function safeAdd(a, b) -> r {
                r := add(a, b)
                if lt(r, a) { revert(0, 0) }
            }

            function gte(a, b) -> r {
                r := iszero(lt(a, b))
            }
        }
    }
}
