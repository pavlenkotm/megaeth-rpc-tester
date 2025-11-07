# 🎨 HTML/CSS Web3 DApp Landing Page

A professional, responsive landing page for Web3 decentralized applications with MetaMask integration.

## 📋 Contents

- **index.html** - Main HTML structure
  - Responsive navigation
  - Hero section with statistics
  - Features showcase
  - Wallet connection interface
  - Professional footer

- **styles.css** - Modern CSS styling
  - Dark theme design
  - Gradient effects
  - Smooth animations
  - Mobile responsive
  - Glassmorphism effects

- **app.js** - Web3 functionality
  - MetaMask connection
  - Balance display
  - Network detection
  - Account change handling
  - Event listeners

## 🚀 Quick Start

### No Build Required!

Simply open `index.html` in a web browser:

```bash
cd languages/html-css

# Option 1: Open directly
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows

# Option 2: Use a local server (recommended)
python -m http.server 8000
# Then visit: http://localhost:8000

# Option 3: Use Node.js
npx http-server
```

### With VS Code Live Server

1. Install "Live Server" extension
2. Right-click `index.html`
3. Select "Open with Live Server"

## 🎨 Features

### Design

- **Modern Dark Theme**: Professional dark mode design
- **Gradient Accents**: Eye-catching gradient text and buttons
- **Smooth Animations**: Hover effects and transitions
- **Glassmorphism**: Modern frosted glass effects
- **Responsive Layout**: Mobile, tablet, and desktop support
- **Accessibility**: Semantic HTML and proper contrast

### Functionality

- **MetaMask Integration**: Connect and interact with MetaMask
- **Balance Display**: Show ETH balance in real-time
- **Network Detection**: Display current blockchain network
- **Auto-Connect**: Remember connected wallet
- **Account Switching**: Handle account changes automatically
- **Network Switching**: Detect network changes

### Sections

- **Hero**: Eye-catching introduction with CTA buttons
- **Stats**: Display key metrics (users, volume, uptime)
- **Features**: Showcase 6 key features with icons
- **Wallet Connection**: Interactive wallet connection interface
- **Footer**: Links and resources

## 📚 Customization

### Change Colors

Edit CSS variables in `styles.css`:

```css
:root {
    --primary-color: #3b82f6;  /* Your primary brand color */
    --secondary-color: #8b5cf6; /* Secondary accent */
    --dark-bg: #0f172a;        /* Background */
}
```

### Update Content

Edit text in `index.html`:

```html
<h1 class="hero-title">Your DApp Name</h1>
<p class="hero-subtitle">Your custom description</p>
```

### Add Contract Interaction

In `app.js`:

```javascript
// Add your contract ABI and address
const contractAddress = "0x...";
const contractABI = [...];

const contract = new ethers.Contract(
    contractAddress,
    contractABI,
    signer
);
```

## 🔧 Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive

## 📱 Mobile Responsive

Breakpoints:
- Desktop: > 768px
- Tablet: 768px - 480px
- Mobile: < 480px

## 🎯 Use Cases

- **DApp Landing Pages**: Showcase your decentralized app
- **NFT Marketplaces**: Display NFT collections
- **DeFi Platforms**: Present DeFi products
- **DAO Websites**: Community and governance portals
- **Token Sales**: ICO/IDO landing pages
- **Web3 Projects**: Any blockchain project

## 🔐 Security Notes

- Never expose private keys in frontend code
- Validate all user inputs
- Use HTTPS in production
- Implement rate limiting for contract calls
- Add transaction confirmation dialogs

## 📖 Dependencies

- **Ethers.js**: v5.7 (CDN loaded)
- No build tools required
- Pure HTML/CSS/JavaScript

## 🚀 Deployment

### GitHub Pages

```bash
# Push to GitHub
git add languages/html-css/
git commit -m "Add landing page"
git push

# Enable GitHub Pages in repository settings
# Select main branch and /languages/html-css folder
```

### Netlify

1. Drag and drop the `html-css` folder to Netlify
2. Site is live instantly!

### Vercel

```bash
npm i -g vercel
cd languages/html-css
vercel
```

## 📄 License

MIT License - See LICENSE file for details
