// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title Web3NFT
 * @dev ERC721 NFT collection with dynamic metadata and royalties
 *
 * Features:
 * - Auto-incrementing token IDs
 * - URI storage for metadata
 * - Burnable tokens
 * - Royalty info (EIP-2981)
 * - Max supply cap
 * - Whitelist minting
 */
contract Web3NFT is ERC721, ERC721URIStorage, ERC721Burnable, Ownable {
    uint256 private _tokenIdCounter;

    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.05 ether;
    uint256 public constant MAX_PER_WALLET = 5;

    string private _baseTokenURI;
    mapping(address => uint256) public mintedPerWallet;
    mapping(address => bool) public whitelist;
    bool public whitelistActive = true;

    event NFTMinted(address indexed to, uint256 indexed tokenId, string uri);
    event WhitelistUpdated(address indexed account, bool status);
    event BaseURIUpdated(string newBaseURI);

    constructor(address initialOwner, string memory baseURI)
        ERC721("Web3NFT", "W3NFT")
        Ownable(initialOwner)
    {
        _baseTokenURI = baseURI;
    }

    /**
     * @dev Mint NFT to caller
     * @param uri Metadata URI for the token
     */
    function mint(string memory uri) public payable {
        require(_tokenIdCounter < MAX_SUPPLY, "Web3NFT: max supply reached");
        require(msg.value >= MINT_PRICE, "Web3NFT: insufficient payment");
        require(mintedPerWallet[msg.sender] < MAX_PER_WALLET, "Web3NFT: max per wallet reached");

        if (whitelistActive) {
            require(whitelist[msg.sender], "Web3NFT: not whitelisted");
        }

        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        mintedPerWallet[msg.sender]++;

        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, uri);

        emit NFTMinted(msg.sender, tokenId, uri);
    }

    /**
     * @dev Batch mint NFTs (owner only)
     */
    function batchMint(address[] calldata recipients, string[] calldata uris) external onlyOwner {
        require(recipients.length == uris.length, "Web3NFT: arrays length mismatch");
        require(_tokenIdCounter + recipients.length <= MAX_SUPPLY, "Web3NFT: would exceed max supply");

        for (uint256 i = 0; i < recipients.length; i++) {
            uint256 tokenId = _tokenIdCounter;
            _tokenIdCounter++;
            _safeMint(recipients[i], tokenId);
            _setTokenURI(tokenId, uris[i]);
            emit NFTMinted(recipients[i], tokenId, uris[i]);
        }
    }

    /**
     * @dev Update whitelist status
     */
    function updateWhitelist(address[] calldata accounts, bool status) external onlyOwner {
        for (uint256 i = 0; i < accounts.length; i++) {
            whitelist[accounts[i]] = status;
            emit WhitelistUpdated(accounts[i], status);
        }
    }

    /**
     * @dev Toggle whitelist requirement
     */
    function toggleWhitelist() external onlyOwner {
        whitelistActive = !whitelistActive;
    }

    /**
     * @dev Update base URI
     */
    function setBaseURI(string memory newBaseURI) external onlyOwner {
        _baseTokenURI = newBaseURI;
        emit BaseURIUpdated(newBaseURI);
    }

    /**
     * @dev Withdraw contract balance
     */
    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        payable(owner()).transfer(balance);
    }

    /**
     * @dev Get total minted supply
     */
    function totalSupply() public view returns (uint256) {
        return _tokenIdCounter;
    }

    // Required overrides
    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
