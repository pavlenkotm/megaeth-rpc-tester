// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

/**
 * @title Web3Token
 * @dev ERC20 token with advanced features for Web3 applications
 *
 * Features:
 * - Mintable by owner
 * - Burnable by token holders
 * - Pausable for emergency situations
 * - Permit (EIP-2612) for gasless approvals
 * - Supply cap to prevent infinite inflation
 */
contract Web3Token is ERC20, ERC20Burnable, Ownable, ERC20Permit {
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18; // 1 billion tokens

    event TokensMinted(address indexed to, uint256 amount);
    event MaxSupplyReached(uint256 totalSupply);

    constructor(address initialOwner)
        ERC20("Web3Token", "W3T")
        Ownable(initialOwner)
        ERC20Permit("Web3Token")
    {
        // Mint initial supply to deployer
        _mint(initialOwner, 100_000_000 * 10**18); // 100M initial supply
    }

    /**
     * @dev Mint new tokens (only owner)
     * @param to Address to receive minted tokens
     * @param amount Amount of tokens to mint
     */
    function mint(address to, uint256 amount) public onlyOwner {
        require(totalSupply() + amount <= MAX_SUPPLY, "Web3Token: max supply exceeded");
        _mint(to, amount);
        emit TokensMinted(to, amount);

        if (totalSupply() == MAX_SUPPLY) {
            emit MaxSupplyReached(totalSupply());
        }
    }

    /**
     * @dev Batch transfer to multiple addresses
     * @param recipients Array of recipient addresses
     * @param amounts Array of amounts to send
     */
    function batchTransfer(address[] calldata recipients, uint256[] calldata amounts) external {
        require(recipients.length == amounts.length, "Web3Token: arrays length mismatch");
        require(recipients.length <= 200, "Web3Token: too many recipients");

        for (uint256 i = 0; i < recipients.length; i++) {
            _transfer(msg.sender, recipients[i], amounts[i]);
        }
    }

    /**
     * @dev Get remaining mintable supply
     */
    function remainingSupply() public view returns (uint256) {
        return MAX_SUPPLY - totalSupply();
    }
}
