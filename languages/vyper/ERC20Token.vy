# @version ^0.3.9

"""
@title ERC20 Token
@author Web3 Examples
@notice A standard ERC20 token implementation in Vyper
@dev Implements the ERC20 interface with mint and burn functionality
"""

from vyper.interfaces import ERC20

implements: ERC20

# Events
event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    amount: uint256

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    amount: uint256

event Mint:
    to: indexed(address)
    amount: uint256

event Burn:
    from_address: indexed(address)
    amount: uint256

# State variables
name: public(String[64])
symbol: public(String[32])
decimals: public(uint8)
totalSupply: public(uint256)
balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])
owner: public(address)
max_supply: public(uint256)

@external
def __init__(
    _name: String[64],
    _symbol: String[32],
    _decimals: uint8,
    _initial_supply: uint256,
    _max_supply: uint256
):
    """
    @notice Contract constructor
    @param _name Token name
    @param _symbol Token symbol
    @param _decimals Number of decimals
    @param _initial_supply Initial token supply
    @param _max_supply Maximum token supply
    """
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals
    self.owner = msg.sender
    self.max_supply = _max_supply

    # Mint initial supply to deployer
    self.totalSupply = _initial_supply
    self.balanceOf[msg.sender] = _initial_supply

    log Transfer(empty(address), msg.sender, _initial_supply)

@external
def transfer(_to: address, _value: uint256) -> bool:
    """
    @notice Transfer tokens to another address
    @param _to The recipient address
    @param _value The amount to transfer
    @return Success boolean
    """
    assert _to != empty(address), "Invalid recipient"
    assert self.balanceOf[msg.sender] >= _value, "Insufficient balance"

    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value

    log Transfer(msg.sender, _to, _value)
    return True

@external
def approve(_spender: address, _value: uint256) -> bool:
    """
    @notice Approve an address to spend tokens
    @param _spender The address authorized to spend
    @param _value The maximum amount they can spend
    @return Success boolean
    """
    assert _spender != empty(address), "Invalid spender"

    self.allowance[msg.sender][_spender] = _value

    log Approval(msg.sender, _spender, _value)
    return True

@external
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    """
    @notice Transfer tokens from one address to another
    @param _from The sender address
    @param _to The recipient address
    @param _value The amount to transfer
    @return Success boolean
    """
    assert _to != empty(address), "Invalid recipient"
    assert self.balanceOf[_from] >= _value, "Insufficient balance"
    assert self.allowance[_from][msg.sender] >= _value, "Insufficient allowance"

    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
    self.allowance[_from][msg.sender] -= _value

    log Transfer(_from, _to, _value)
    return True

@external
def mint(_to: address, _value: uint256):
    """
    @notice Mint new tokens (owner only)
    @param _to The address to receive minted tokens
    @param _value The amount to mint
    """
    assert msg.sender == self.owner, "Only owner can mint"
    assert self.totalSupply + _value <= self.max_supply, "Max supply exceeded"

    self.totalSupply += _value
    self.balanceOf[_to] += _value

    log Mint(_to, _value)
    log Transfer(empty(address), _to, _value)

@external
def burn(_value: uint256):
    """
    @notice Burn tokens from caller's balance
    @param _value The amount to burn
    """
    assert self.balanceOf[msg.sender] >= _value, "Insufficient balance"

    self.totalSupply -= _value
    self.balanceOf[msg.sender] -= _value

    log Burn(msg.sender, _value)
    log Transfer(msg.sender, empty(address), _value)

@view
@external
def remaining_supply() -> uint256:
    """
    @notice Get remaining mintable supply
    @return The amount of tokens that can still be minted
    """
    return self.max_supply - self.totalSupply
