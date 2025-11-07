# @version ^0.3.9

"""
@title Simple Vault
@author Web3 Examples
@notice A simple ETH vault contract written in Vyper
@dev Demonstrates Vyper syntax and patterns for DeFi applications
"""

# Events
event Deposit:
    sender: indexed(address)
    amount: uint256
    timestamp: uint256

event Withdrawal:
    recipient: indexed(address)
    amount: uint256
    timestamp: uint256

event OwnershipTransferred:
    previous_owner: indexed(address)
    new_owner: indexed(address)

# State variables
owner: public(address)
total_deposits: public(uint256)
total_withdrawals: public(uint256)
balances: public(HashMap[address, uint256])
is_paused: public(bool)

# Constants
MIN_DEPOSIT: constant(uint256) = 10 ** 16  # 0.01 ETH
MAX_DEPOSIT: constant(uint256) = 100 * 10 ** 18  # 100 ETH

@external
def __init__():
    """
    @notice Contract constructor
    @dev Sets the contract deployer as the owner
    """
    self.owner = msg.sender
    self.is_paused = False
    self.total_deposits = 0
    self.total_withdrawals = 0

@external
@payable
def deposit():
    """
    @notice Deposit ETH into the vault
    @dev Requires minimum deposit amount and vault not paused
    """
    assert not self.is_paused, "Vault is paused"
    assert msg.value >= MIN_DEPOSIT, "Deposit too small"
    assert msg.value <= MAX_DEPOSIT, "Deposit too large"

    self.balances[msg.sender] += msg.value
    self.total_deposits += msg.value

    log Deposit(msg.sender, msg.value, block.timestamp)

@external
def withdraw(amount: uint256):
    """
    @notice Withdraw ETH from the vault
    @param amount The amount of ETH to withdraw
    @dev Requires sufficient balance
    """
    assert not self.is_paused, "Vault is paused"
    assert self.balances[msg.sender] >= amount, "Insufficient balance"
    assert amount > 0, "Amount must be greater than 0"

    self.balances[msg.sender] -= amount
    self.total_withdrawals += amount

    send(msg.sender, amount)

    log Withdrawal(msg.sender, amount, block.timestamp)

@external
def withdraw_all():
    """
    @notice Withdraw all ETH from the sender's balance
    @dev Convenience function to withdraw entire balance
    """
    balance: uint256 = self.balances[msg.sender]
    assert balance > 0, "No balance to withdraw"

    self.withdraw(balance)

@view
@external
def get_balance(account: address) -> uint256:
    """
    @notice Get the balance of an account
    @param account The address to query
    @return The balance of the account
    """
    return self.balances[account]

@view
@external
def get_contract_balance() -> uint256:
    """
    @notice Get the total ETH balance of the contract
    @return The contract's ETH balance
    """
    return self.balance

@view
@external
def get_my_balance() -> uint256:
    """
    @notice Get the caller's balance
    @return The caller's balance in the vault
    """
    return self.balances[msg.sender]

@external
def pause():
    """
    @notice Pause the vault (owner only)
    @dev Prevents deposits and withdrawals
    """
    assert msg.sender == self.owner, "Only owner can pause"
    self.is_paused = True

@external
def unpause():
    """
    @notice Unpause the vault (owner only)
    @dev Re-enables deposits and withdrawals
    """
    assert msg.sender == self.owner, "Only owner can unpause"
    self.is_paused = False

@external
def transfer_ownership(new_owner: address):
    """
    @notice Transfer ownership to a new address (owner only)
    @param new_owner The address of the new owner
    """
    assert msg.sender == self.owner, "Only owner can transfer ownership"
    assert new_owner != empty(address), "Invalid new owner address"

    old_owner: address = self.owner
    self.owner = new_owner

    log OwnershipTransferred(old_owner, new_owner)

@external
def emergency_withdraw():
    """
    @notice Emergency withdrawal function (owner only)
    @dev Allows owner to withdraw all funds in case of emergency
    """
    assert msg.sender == self.owner, "Only owner can emergency withdraw"

    send(self.owner, self.balance)
