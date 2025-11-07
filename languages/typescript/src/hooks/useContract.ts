import { useState, useEffect } from 'react';
import { ethers, Contract, BrowserProvider } from 'ethers';

/**
 * Custom React Hook for interacting with smart contracts
 *
 * Features:
 * - Connect to contract with ABI
 * - Call read functions
 * - Execute write functions with transaction management
 * - Handle loading and error states
 * - Event listening
 */

interface UseContractReturn {
  contract: Contract | null;
  loading: boolean;
  error: string | null;
  callFunction: (functionName: string, ...args: any[]) => Promise<any>;
  sendTransaction: (functionName: string, ...args: any[]) => Promise<any>;
  addEventListener: (eventName: string, callback: (...args: any[]) => void) => void;
  removeEventListener: (eventName: string, callback: (...args: any[]) => void) => void;
}

export const useContract = (
  contractAddress: string,
  contractABI: any[]
): UseContractReturn => {
  const [contract, setContract] = useState<Contract | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    initializeContract();
  }, [contractAddress, contractABI]);

  const initializeContract = async () => {
    try {
      setLoading(true);
      setError(null);

      if (!window.ethereum) {
        throw new Error('Ethereum provider not found');
      }

      const provider = new BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();

      const contractInstance = new Contract(
        contractAddress,
        contractABI,
        signer
      );

      setContract(contractInstance);
    } catch (err: any) {
      setError(err.message || 'Failed to initialize contract');
      console.error('Contract initialization error:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Call a read-only contract function
   */
  const callFunction = async (functionName: string, ...args: any[]): Promise<any> => {
    if (!contract) {
      throw new Error('Contract not initialized');
    }

    try {
      setLoading(true);
      setError(null);

      const result = await contract[functionName](...args);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Function call failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Send a transaction to a contract function
   */
  const sendTransaction = async (functionName: string, ...args: any[]): Promise<any> => {
    if (!contract) {
      throw new Error('Contract not initialized');
    }

    try {
      setLoading(true);
      setError(null);

      // Send transaction
      const tx = await contract[functionName](...args);

      console.log('Transaction sent:', tx.hash);

      // Wait for confirmation
      const receipt = await tx.wait();

      console.log('Transaction confirmed:', receipt.hash);

      return receipt;
    } catch (err: any) {
      const errorMessage = err.message || 'Transaction failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Add event listener to contract
   */
  const addEventListener = (eventName: string, callback: (...args: any[]) => void) => {
    if (!contract) {
      console.error('Contract not initialized');
      return;
    }

    contract.on(eventName, callback);
  };

  /**
   * Remove event listener from contract
   */
  const removeEventListener = (eventName: string, callback: (...args: any[]) => void) => {
    if (!contract) {
      console.error('Contract not initialized');
      return;
    }

    contract.off(eventName, callback);
  };

  return {
    contract,
    loading,
    error,
    callFunction,
    sendTransaction,
    addEventListener,
    removeEventListener,
  };
};

/**
 * Example usage:
 *
 * const ERC20_ABI = [...];
 * const { contract, loading, callFunction, sendTransaction } = useContract(
 *   '0x...',
 *   ERC20_ABI
 * );
 *
 * // Read function
 * const balance = await callFunction('balanceOf', userAddress);
 *
 * // Write function
 * await sendTransaction('transfer', recipientAddress, amount);
 */

export default useContract;
