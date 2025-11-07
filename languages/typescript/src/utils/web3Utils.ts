import { ethers } from 'ethers';

/**
 * Web3 Utility Functions
 *
 * Collection of helper functions for common Web3 operations
 */

/**
 * Format Wei to Ether with specified decimals
 */
export const formatEther = (wei: bigint | string, decimals: number = 4): string => {
  const ether = ethers.formatEther(wei);
  return parseFloat(ether).toFixed(decimals);
};

/**
 * Parse Ether to Wei
 */
export const parseEther = (ether: string): bigint => {
  return ethers.parseEther(ether);
};

/**
 * Shorten Ethereum address for display
 */
export const shortenAddress = (address: string, chars: number = 4): string => {
  if (!address) return '';
  return `${address.substring(0, chars + 2)}...${address.substring(address.length - chars)}`;
};

/**
 * Validate Ethereum address
 */
export const isValidAddress = (address: string): boolean => {
  return ethers.isAddress(address);
};

/**
 * Get network name from chain ID
 */
export const getNetworkName = (chainId: number): string => {
  const networks: { [key: number]: string } = {
    1: 'Ethereum Mainnet',
    5: 'Goerli Testnet',
    11155111: 'Sepolia Testnet',
    137: 'Polygon Mainnet',
    80001: 'Mumbai Testnet',
    42161: 'Arbitrum One',
    421613: 'Arbitrum Goerli',
    10: 'Optimism Mainnet',
    420: 'Optimism Goerli',
    56: 'BSC Mainnet',
    97: 'BSC Testnet',
  };

  return networks[chainId] || `Unknown Network (${chainId})`;
};

/**
 * Convert hex to decimal
 */
export const hexToDecimal = (hex: string): number => {
  return parseInt(hex, 16);
};

/**
 * Convert decimal to hex
 */
export const decimalToHex = (decimal: number): string => {
  return '0x' + decimal.toString(16);
};

/**
 * Get explorer URL for address
 */
export const getExplorerUrl = (
  address: string,
  chainId: number,
  type: 'address' | 'tx' | 'token' = 'address'
): string => {
  const explorers: { [key: number]: string } = {
    1: 'https://etherscan.io',
    5: 'https://goerli.etherscan.io',
    11155111: 'https://sepolia.etherscan.io',
    137: 'https://polygonscan.com',
    80001: 'https://mumbai.polygonscan.com',
    42161: 'https://arbiscan.io',
    10: 'https://optimistic.etherscan.io',
    56: 'https://bscscan.com',
  };

  const baseUrl = explorers[chainId] || 'https://etherscan.io';
  return `${baseUrl}/${type}/${address}`;
};

/**
 * Wait for transaction with timeout
 */
export const waitForTransaction = async (
  provider: ethers.Provider,
  txHash: string,
  confirmations: number = 1,
  timeout: number = 120000 // 2 minutes
): Promise<ethers.TransactionReceipt | null> => {
  return Promise.race([
    provider.waitForTransaction(txHash, confirmations),
    new Promise<null>((_, reject) =>
      setTimeout(() => reject(new Error('Transaction timeout')), timeout)
    ),
  ]);
};

/**
 * Estimate gas with buffer
 */
export const estimateGasWithBuffer = async (
  transaction: any,
  bufferPercent: number = 20
): Promise<bigint> => {
  const estimated = await transaction.estimateGas();
  const buffer = (estimated * BigInt(bufferPercent)) / BigInt(100);
  return estimated + buffer;
};

/**
 * Convert timestamp to readable date
 */
export const timestampToDate = (timestamp: number): string => {
  return new Date(timestamp * 1000).toLocaleString();
};

/**
 * Calculate gas cost in ETH
 */
export const calculateGasCost = (gasUsed: bigint, gasPrice: bigint): string => {
  const cost = gasUsed * gasPrice;
  return ethers.formatEther(cost);
};

/**
 * Check if MetaMask is installed
 */
export const isMetaMaskInstalled = (): boolean => {
  return typeof window !== 'undefined' && Boolean(window.ethereum?.isMetaMask);
};

/**
 * Switch network in MetaMask
 */
export const switchNetwork = async (chainId: number): Promise<void> => {
  if (!window.ethereum) {
    throw new Error('MetaMask not installed');
  }

  try {
    await window.ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: decimalToHex(chainId) }],
    });
  } catch (error: any) {
    // Chain not added to MetaMask
    if (error.code === 4902) {
      throw new Error('Please add this network to MetaMask');
    }
    throw error;
  }
};

/**
 * Add token to MetaMask
 */
export const addTokenToWallet = async (
  tokenAddress: string,
  tokenSymbol: string,
  tokenDecimals: number,
  tokenImage?: string
): Promise<boolean> => {
  if (!window.ethereum) {
    throw new Error('MetaMask not installed');
  }

  try {
    const wasAdded = await window.ethereum.request({
      method: 'wallet_watchAsset',
      params: {
        type: 'ERC20',
        options: {
          address: tokenAddress,
          symbol: tokenSymbol,
          decimals: tokenDecimals,
          image: tokenImage,
        },
      },
    });

    return wasAdded;
  } catch (error) {
    console.error('Error adding token:', error);
    return false;
  }
};

export default {
  formatEther,
  parseEther,
  shortenAddress,
  isValidAddress,
  getNetworkName,
  hexToDecimal,
  decimalToHex,
  getExplorerUrl,
  waitForTransaction,
  estimateGasWithBuffer,
  timestampToDate,
  calculateGasCost,
  isMetaMaskInstalled,
  switchNetwork,
  addTokenToWallet,
};
