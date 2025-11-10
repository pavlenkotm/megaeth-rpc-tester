// Web3 DApp JavaScript

let provider;
let signer;
let userAddress;

// Connect Wallet Function
async function connectWallet() {
    try {
        if (typeof window.ethereum === 'undefined') {
            alert('Please install MetaMask!');
            return;
        }

        // Request account access
        const accounts = await window.ethereum.request({
            method: 'eth_requestAccounts'
        });

        userAddress = accounts[0];

        // Initialize provider and signer (ethers.js v6)
        provider = new ethers.BrowserProvider(window.ethereum);
        signer = await provider.getSigner();

        // Get balance
        const balance = await provider.getBalance(userAddress);
        const balanceInEth = ethers.formatEther(balance);

        // Get network
        const network = await provider.getNetwork();

        // Update UI
        document.getElementById('walletAddress').textContent =
            userAddress.substring(0, 6) + '...' + userAddress.substring(userAddress.length - 4);
        document.getElementById('walletBalance').textContent =
            parseFloat(balanceInEth).toFixed(4) + ' ETH';
        document.getElementById('walletNetwork').textContent =
            getNetworkName(network.chainId);

        document.getElementById('walletInfo').style.display = 'block';
        document.getElementById('walletConnect').style.display = 'none';
        document.getElementById('connectButton').textContent = 'Connected';
        document.getElementById('connectButton').disabled = true;

        console.log('Wallet connected:', userAddress);

    } catch (error) {
        console.error('Error connecting wallet:', error);
        alert('Failed to connect wallet');
    }
}

// Disconnect Wallet Function
function disconnectWallet() {
    userAddress = null;
    provider = null;
    signer = null;

    document.getElementById('walletInfo').style.display = 'none';
    document.getElementById('walletConnect').style.display = 'block';
    document.getElementById('connectButton').textContent = 'Connect Wallet';
    document.getElementById('connectButton').disabled = false;
}

// Get Network Name
function getNetworkName(chainId) {
    const networks = {
        1: 'Ethereum Mainnet',
        5: 'Goerli Testnet',
        11155111: 'Sepolia Testnet',
        137: 'Polygon Mainnet',
        80001: 'Mumbai Testnet',
        42161: 'Arbitrum One',
        10: 'Optimism',
        56: 'BSC Mainnet'
    };

    return networks[chainId] || `Chain ID: ${chainId}`;
}

// Listen for account changes
if (window.ethereum) {
    window.ethereum.on('accountsChanged', (accounts) => {
        if (accounts.length === 0) {
            disconnectWallet();
        } else {
            connectWallet();
        }
    });

    window.ethereum.on('chainChanged', () => {
        window.location.reload();
    });
}

// Check if wallet is already connected
window.addEventListener('load', async () => {
    if (typeof window.ethereum !== 'undefined') {
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        if (accounts.length > 0) {
            connectWallet();
        }
    }
});
