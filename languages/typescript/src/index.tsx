import React from 'react';
import ReactDOM from 'react-dom/client';
import WalletConnect from './WalletConnect';

// Export components for library usage
export { default as WalletConnect } from './WalletConnect';
export { useContract } from './hooks/useContract';
export * from './utils/web3Utils';

// Demo app (only runs when used as standalone)
if (typeof document !== 'undefined') {
  const rootElement = document.getElementById('root');
  if (rootElement) {
    const root = ReactDOM.createRoot(rootElement);
    root.render(
      <React.StrictMode>
        <div style={{ padding: '20px' }}>
          <h1>Web3 TypeScript Components Demo</h1>
          <WalletConnect />
        </div>
      </React.StrictMode>
    );
  }
}
