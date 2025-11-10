const hre = require("hardhat");

async function main() {
  console.log("Starting deployment...\n");

  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);

  // Get account balance
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "ETH\n");

  // Deploy Web3Token
  console.log("Deploying Web3Token...");
  const Web3Token = await hre.ethers.getContractFactory("Web3Token");
  const initialSupply = hre.ethers.parseEther("1000000"); // 1M tokens
  const maxSupply = hre.ethers.parseEther("10000000"); // 10M tokens

  const token = await Web3Token.deploy(
    deployer.address,
    initialSupply,
    maxSupply
  );
  await token.waitForDeployment();
  const tokenAddress = await token.getAddress();

  console.log("✓ Web3Token deployed to:", tokenAddress);
  console.log("  - Initial Supply:", hre.ethers.formatEther(initialSupply));
  console.log("  - Max Supply:", hre.ethers.formatEther(maxSupply));
  console.log();

  // Deploy Web3NFT
  console.log("Deploying Web3NFT...");
  const Web3NFT = await hre.ethers.getContractFactory("Web3NFT");
  const baseURI = "ipfs://QmYourBaseURI/";

  const nft = await Web3NFT.deploy(deployer.address, baseURI);
  await nft.waitForDeployment();
  const nftAddress = await nft.getAddress();

  console.log("✓ Web3NFT deployed to:", nftAddress);
  console.log("  - Base URI:", baseURI);
  console.log("  - Max Supply:", await nft.MAX_SUPPLY());
  console.log("  - Mint Price:", hre.ethers.formatEther(await nft.MINT_PRICE()), "ETH");
  console.log();

  // Deployment summary
  console.log("=".repeat(60));
  console.log("DEPLOYMENT SUMMARY");
  console.log("=".repeat(60));
  console.log("Network:", hre.network.name);
  console.log("Deployer:", deployer.address);
  console.log();
  console.log("Web3Token:", tokenAddress);
  console.log("Web3NFT:", nftAddress);
  console.log("=".repeat(60));
  console.log();

  // Save deployment info
  const fs = require('fs');
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      Web3Token: {
        address: tokenAddress,
        initialSupply: hre.ethers.formatEther(initialSupply),
        maxSupply: hre.ethers.formatEther(maxSupply)
      },
      Web3NFT: {
        address: nftAddress,
        baseURI: baseURI,
        maxSupply: (await nft.MAX_SUPPLY()).toString(),
        mintPrice: hre.ethers.formatEther(await nft.MINT_PRICE())
      }
    }
  };

  fs.writeFileSync(
    'deployment.json',
    JSON.stringify(deploymentInfo, null, 2)
  );

  console.log("Deployment info saved to deployment.json");

  // Verification instructions
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("\nTo verify contracts on Etherscan, run:");
    console.log(`npx hardhat verify --network ${hre.network.name} ${tokenAddress} "${deployer.address}" "${initialSupply}" "${maxSupply}"`);
    console.log(`npx hardhat verify --network ${hre.network.name} ${nftAddress} "${deployer.address}" "${baseURI}"`);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
