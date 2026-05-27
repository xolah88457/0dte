# 0dte Hedging + Arb (this bot made me and my part %15,100 combined on BTC/USDT, ETH/USDT, and SOL/USDT, however it got patched)

---

## **By Ryan & Szymon**

---

A professional automated trading bot for 0dte.io with simulation mode, diagnostics, and real-time countdown timer.

## 📋 Table of Contents

- [Features](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)
- [Requirements](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)
- [Installation](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)
- [Quick Start](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)
- [Detailed Script Documentation](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)
- [Configuration Guide](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)
- [Trading Strategies](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)
- [Troubleshooting](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)
- [Safety & Best Practices](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)
- [FAQ](https://www.notion.so/0dte-Hedging-Arb-28431f1473d180879a01c2be3e94a893?pvs=21)

---

## ✨ Features

### Core Features

- 🤖 **Automated Trading** - Executes trades every 15 minutes automatically
- 🎮 **Simulation Mode** - Test strategies without risking real money
- ⏱️ **Live Countdown Timer** - Visual countdown with progress bar
- 📊 **Statistics Tracking** - Win rate, P&L, and performance metrics
- 🔄 **Auto Recovery** - Handles errors and reconnects automatically
- 📝 **Detailed Logging** - JSON logs with all trade history

### Technical Features

- 🌐 **Google Login Support** - No wallet extensions needed
- 💾 **Persistent Sessions** - Saves login state between runs
- 🔧 **Diagnostic Tools** - Test all components before trading
- ⚡ **Retry Logic** - Each action retries 3 times before failing
- 📈 **Balance Tracking** - Monitors balance changes after trades

---

## 💻 Requirements

### System Requirements

- **Operating System**: Windows 10/11 (also works on Mac/Linux)
- **Python**: Version 3.8 or higher
- **Chrome Browser**: Latest version installed
- **RAM**: Minimum 4GB
- **Internet**: Stable connection required

### Python Dependencies

```
playwright>=1.40.0

```

---

## 🚀 Installation

### Step 1: Install Python

1. Download Python from [python.org](https://python.org/)
2. During installation, check "Add Python to PATH"
3. Verify installation:

```bash
python --version

```

### Step 2: Create Project Folder

```bash
# Create a folder for the bot
mkdir C:\TradingBot
cd C:\TradingBot

```

### Step 3: Save the Scripts

Save these three files in your folder:

- `setup.py` - Profile setup script
- `diagnostic.py` - Testing and diagnostics
- `bot.py` - Main trading bot

### Step 4: Install Dependencies

```bash
# Install Playwright
pip install playwright

# Install Chrome driver
playwright install chromium

```

---

## 🎯 Quick Start

### 1️⃣ First Time Setup (5 minutes)

```bash
python setup.py

```

- Opens Chrome browser
- Navigate to 0dte.io
- Login with your account
- Press ENTER when done

### 2️⃣ Test Everything Works

```bash
python diagnostic.py

```

- Choose option 2 for trading simulation
- Verify all components work

### 3️⃣ Start Trading

```bash
# Simulation mode (recommended first)
python bot.py --simulate

# Live trading (real money)
python bot.py

```

---

## 📚 Detailed Script Documentation

## 🔧 setup.py - Initial Setup Script

### Purpose

Creates a Chrome profile and saves your login session so you don't need to login every time.

### Usage

```bash
python setup.py

```

### What It Does

1. **Creates Chrome Profile** at `C:\ChromeProfiles\0dte_profile`
2. **Opens 0dte.io** in Chrome browser
3. **Waits for Manual Login** - you complete the login
4. **Saves Session** - stores cookies and login state
5. **Takes Screenshot** - proof of successful setup

### Step-by-Step Process

```
==================================================
TRADING BOT SETUP - Google Login
==================================================

📁 Profile will be created at: C:\ChromeProfiles\0dte_profile

🚀 Launching Chrome...

🌐 Navigating to https://0dte.io...

==================================================
MANUAL SETUP REQUIRED:
==================================================

1️⃣  Login to the site:
   - Click 'Login' or 'Sign In' button
   - Use Google login OR any other method
   - Complete any 2FA if required

2️⃣  Make sure you can see the trading interface:
   - You should see trading cards
   - Buttons like '15M', '4X' should be visible
   - The page should be fully loaded

3️⃣  Once logged in and ready:
   - The browser will save your session
   - You won't need to login again
==================================================

⏳ Please complete the login process...
   Take your time, the browser will wait

✅ Press ENTER when you're fully logged in and ready...

```

### Important Notes

- ⚠️ **Complete the login fully** before pressing ENTER
- 💡 **One-time process** - only need to do this once
- 🔄 **Re-run if needed** - can clear profile and start fresh
- 📸 **Check screenshot** - `setup_complete.png` shows final state

---

## 🔍 diagnostic.py - Testing & Diagnostics

### Purpose

Tests all bot components and simulates trading without spending money.

### Usage

```bash
python diagnostic.py

```

### Menu Options

```
Choose an option:
1. Standard diagnostics - Check if everything is installed
2. Trading simulation (recommended) - Test trading without money
3. Both - Run all tests

```

### Trading Simulation Output

```
==================================================
TRADING SIMULATION TEST
==================================================

🎮 This will simulate trades without spending money
   We'll test clicking buttons but won't confirm trades

📊 Simulated Trade #1
------------------------------
  1️⃣ Testing interval button (15M)...
     ✅ Clicked 15M
  2️⃣ Testing amount input (0.01)...
     ✅ Entered 0.01
  3️⃣ Testing leverage button (4X)...
     ✅ Clicked 4X
  4️⃣ Testing trade card (BUY/GREEN)...
     ✅ Clicked BUY card
     ✅ YES button is visible (not clicking)
  5️⃣ Simulated result: WIN

==================================================
SIMULATION SUMMARY
==================================================

✅ Successful steps: 12/12 (100%)

🎉 Bot is ready for live trading!
   Run: python bot.py

```

### What Gets Tested

- ✅ **Chrome Profile** - Exists and is valid
- ✅ **Browser Launch** - Chrome opens correctly
- ✅ **Site Navigation** - Can load 0dte.io
- ✅ **UI Elements** - All buttons and inputs present
- ✅ **Trade Simulation** - Goes through trade steps (except final YES)

### Results File

Creates `simulation_results.json` with detailed test results.

---

## 🤖 bot.py - Main Trading Bot

### Purpose

The main trading bot that executes trades automatically every 15 minutes.

### Usage

```bash
# Simulation mode (no real money)
python bot.py --simulate
# or
python bot.py -s

# Live trading (real money)
python bot.py

```

### Features

### 1. **Countdown Timer**

```
⏱️ Next trade in: 14:32 [██░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 3%

```

- Shows time until next trade
- Visual progress bar
- Updates every second

### 2. **Trade Execution**

```
✅ [SUCCESS] === Starting Trade #1 ===
ℹ️ [INFO] Time: 14:30:00
ℹ️ [INFO] Step 1/5: Selecting interval 15M
ℹ️ [INFO] Step 2/5: Entering amount 0.01
ℹ️ [INFO] Step 3/5: Selecting leverage 4X
ℹ️ [INFO] Step 4/5: Selecting BUY direction
ℹ️ [INFO] Step 5/5: Confirming trade
✅ [SUCCESS] ✅ Executed BUY (ABOVE) trade
💰 [TRADE] Result: WIN (+0.0300 SOL)

```

### 3. **Statistics Tracking**

```
==================================================
📊 TRADING STATISTICS
==================================================
Total Trades: 10
Successful: 9
Failed: 1
Wins: 5
Losses: 4
Win Rate: 55.6%
Total P&L: +0.0500 SOL
==================================================

```

### Configuration

Edit the `Config` class in `bot.py`:

```python
class Config:
    # Chrome profile path
    PROFILE_DIR = r"C:\ChromeProfiles\0dte_profile"

    # Trading parameters
    URL = "https://0dte.io"
    INTERVAL = "15M"           # Options: "5M", "15M", "1H", "4H"
    TRADE_MODE = "BUY"         # Options: "BUY" (ABOVE), "SELL" (BELOW)
    BET_AMOUNT = 0.01          # Amount in SOL
    LEVERAGE = "4X"            # Options: "2X", "4X", "10X", "20X"

    # Timing
    TRADE_FREQUENCY = 15       # Minutes between trades

    # Features
    SIMULATION_MODE = False    # Set True for testing
    CHECK_BALANCE = True       # Monitor balance changes
    SHOW_COUNTDOWN = True      # Show countdown timer

```

### Log Files

- **bot_log.json** - Contains all trades, statistics, and events
- **Format**:

```json
{
  "stats": {
    "total_trades": 10,
    "wins": 5,
    "losses": 4,
    "win_rate": 55.6,
    "total_pnl": 0.05
  },
  "logs": [...]
}

```

---

## ⚙️ Configuration Guide

### Trading Parameters

| Parameter | Options | Description |
| --- | --- | --- |
| `INTERVAL` | "5M", "15M", "1H", "4H" | Time interval for trades |
| `TRADE_MODE` | "BUY", "SELL" | BUY = ABOVE (green), SELL = BELOW (red) |
| `BET_AMOUNT` | 0.01 - 1.0 | Amount to bet in SOL |
| `LEVERAGE` | "2X", "4X", "10X", "20X" | Multiplier for wins |
| `TRADE_FREQUENCY` | 1 - 60 | Minutes between trades |

### Risk Levels

### 🟢 Conservative (Recommended for beginners)

```python
INTERVAL = "1H"
TRADE_MODE = "BUY"
BET_AMOUNT = 0.01
LEVERAGE = "2X"
TRADE_FREQUENCY = 60

```

### 🟡 Moderate

```python
INTERVAL = "15M"
TRADE_MODE = "BUY"
BET_AMOUNT = 0.01
LEVERAGE = "4X"
TRADE_FREQUENCY = 15

```

### 🔴 Aggressive (High risk)

```python
INTERVAL = "5M"
TRADE_MODE = "SELL"
BET_AMOUNT = 0.05
LEVERAGE = "10X"
TRADE_FREQUENCY = 5

```

---

## 📊 Trading Strategies

### Strategy 1: Trend Following

```python
# Trade with the trend
TRADE_MODE = "BUY"  # During uptrend
INTERVAL = "15M"
LEVERAGE = "4X"

```

### Strategy 2: Counter-Trend

```python
# Trade against the trend
TRADE_MODE = "SELL"  # During uptrend
INTERVAL = "5M"
LEVERAGE = "2X"

```

### Strategy 3: Conservative Long

```python
# Slow and steady
TRADE_MODE = "BUY"
INTERVAL = "1H"
LEVERAGE = "2X"
TRADE_FREQUENCY = 60

```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

### 1. "Profile not found"

```bash
# Solution: Run setup first
python setup.py

```

### 2. "Cannot find buttons"

```bash
# Solution: Re-run setup to refresh login
python setup.py

# Or run diagnostics to check
python diagnostic.py

```

### 3. "Trade failed"

- Check internet connection
- Verify you have balance in your account
- Run diagnostic.py to test components
- Check if site layout changed

### 4. "Browser won't open"

```bash
# Reinstall Chrome driver
playwright install chromium --force

```

### 5. "Module not found"

```bash
# Reinstall dependencies
pip install playwright --upgrade

```

### Debug Mode

Add debug output by editing bot.py:

```python
# Change log level in SmartLogger
self.logger.log("DEBUG", "Detailed message", data)

```

---

## 🛡️ Safety & Best Practices

### Before Trading

1. **Test with Simulation**

```bash
python bot.py --simulate

```

Run for at least 10 trades to verify everything works.

1. **Start Small**

```python
BET_AMOUNT = 0.01  # Minimum amount

```

1. **Monitor Initially**
- Watch the first 5-10 trades
- Check logs regularly
- Verify balance changes

### Risk Management

### Daily Limits

```python
# Add to Config class
MAX_DAILY_TRADES = 20
MAX_DAILY_LOSS = 0.1  # SOL

```

### Stop Loss

```python
# Stop if balance drops below threshold
MIN_BALANCE = 0.05  # SOL

```

### Security

1. **Never share your profile folder** - Contains login session
2. **Keep scripts private** - Don't upload with credentials
3. **Use separate account** - For trading only
4. **Regular backups** - Save your logs

---

## ❓ FAQ

### Q: How do I stop the bot?

**A:** Press `Ctrl + C` in the terminal. The bot will finish the current action and shut down cleanly.

### Q: Can I run multiple bots?

**A:** Yes, but use different profile directories:

```python
PROFILE_DIR = r"C:\ChromeProfiles\0dte_profile2"

```

### Q: How do I change from BUY to SELL?

**A:** Edit `bot.py`:

```python
TRADE_MODE = "SELL"  # Instead of "BUY"

```

### Q: What does 4X leverage mean?

**A:** If you win with 4X leverage:

- Bet: 0.01 SOL
- Win: 0.04 SOL (4x return)
- Profit: 0.03 SOL

### Q: How do I see my statistics?

**A:** Check `bot_log.json` or wait for the bot to print stats every 5 trades.

### Q: Can I change the countdown timer?

**A:** Yes, in `bot.py`:

```python
SHOW_COUNTDOWN = False  # To disable

```

### Q: Is this legal?

**A:** Check your local regulations regarding automated trading and online gambling.

### Q: What if the site changes?

**A:** The bot may need updates. Run `diagnostic.py` to identify issues.

---

## 📝 Command Reference

### Quick Commands

```bash
# Setup (first time only)
python setup.py

# Test everything
python diagnostic.py

# Simulation trading
python bot.py -s

# Live trading
python bot.py

# With custom config
python bot.py --interval 5M --amount 0.02

```

### Windows Batch Files

Create `start_bot.bat`:

```
@echo off
echo Starting Trading Bot...
cd C:\TradingBot
python bot.py
pause

```

Create `simulate.bat`:

```
@echo off
echo Starting Simulation Mode...
cd C:\TradingBot
python bot.py --simulate
pause

```

---

## 📈 Performance Tracking

### View Statistics

```python
# Add this function to bot.py
def print_detailed_stats():
    print(f"Session Duration: {time_elapsed}")
    print(f"Trades per Hour: {trades_per_hour}")
    print(f"Best Win Streak: {best_streak}")
    print(f"Average Trade Time: {avg_time}")

```

### Export Results

```python
# Export to CSV
import csv
with open('trades.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Time', 'Result', 'PnL', 'Balance'])
    # Write trade data

```

---

## 🚨 Emergency Procedures

### Stop Immediately

1. Press `Ctrl + C` multiple times
2. Close Chrome browser window
3. Kill Python process in Task Manager

### Reset Everything

```bash
# 1. Clear profile
rmdir /s "C:\ChromeProfiles\0dte_profile"

# 2. Re-run setup
python setup.py

# 3. Test before trading
python diagnostic.py

```

---

## 📞 Support & Updates

### Getting Help

1. Check this documentation first
2. Run `diagnostic.py` to identify issues
3. Check `bot_log.json` for error messages
4. Review the troubleshooting section

### Updating the Bot

```bash
# Update Playwright
pip install playwright --upgrade

# Update Chrome driver
playwright install chromium

```

---

## ⚖️ Disclaimer

**IMPORTANT**: This bot is for educational purposes. Trading involves risk of loss.

- Only trade what you can afford to lose
- Past performance doesn't guarantee future results
- The authors are not responsible for any losses
- Always test with simulation mode first
- Check local laws regarding automated trading

---

## 🎉 Good Luck!

Remember to:

- Start with simulation mode
- Use small amounts initially
- Monitor your trades
- Keep your scripts updated
- Trade responsibly

---

### 📁 Files

[bot.py](0dte%20Hedging%20+%20Arb/bot.py)

[diagnostic.py](0dte%20Hedging%20+%20Arb/diagnostic.py)

[requirements.txt](0dte%20Hedging%20+%20Arb/requirements.txt)

[setup.py](0dte%20Hedging%20+%20Arb/setup.py)

---

Happy Trading! 🚀
