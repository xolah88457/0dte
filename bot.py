"""
Simple Trading Bot for 0dte.io
Enhanced version with countdown timer and simulation mode
"""

import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from playwright.async_api import async_playwright, Page, TimeoutError as PlaywrightTimeout
from typing import Optional, Dict, Any, Tuple
import sys

# =================== CONFIGURATION ===================
class Config:
    """Configuration class with all trading parameters"""
    
    # Chrome profile path (for persistent login)
    PROFILE_DIR = r"C:\ChromeProfiles\0dte_profile"
    
    # Trading parameters
    URL = "https://0dte.io"
    INTERVAL = "15M"           # Time interval
    TRADE_MODE = "SELL"         # "BUY" for ABOVE, "SELL" for BELOW
    BET_AMOUNT = 0.01          # Amount in SOL
    LEVERAGE = "4X"            # Leverage multiplier
    
    # Timing settings
    TRADE_FREQUENCY = 15       # Minutes between trades (ALWAYS waits this long)
    PAGE_TIMEOUT = 30000       # 30 seconds
    ACTION_TIMEOUT = 5000      # 5 seconds for button clicks
    CLICK_RETRY = 3           # Number of times to retry clicking
    
    # Features
    SIMULATION_MODE = False    # Set to True for testing without real trades
    CHECK_LOGIN = False        # Set to False to skip login check
    CHECK_BALANCE = True       # Set to False to skip balance checks
    SHOW_COUNTDOWN = True      # Show countdown timer
    
    # Logging
    LOG_FILE = "bot_log.json"
    

# =================== LOGGER WITH STATISTICS ===================
class SmartLogger:
    """Enhanced logger with statistics tracking"""
    
    def __init__(self, filename: str, simulation: bool = False):
        self.filename = filename
        self.simulation = simulation
        self.logs = []
        self.stats = {
            "total_trades": 0,
            "successful_trades": 0,
            "failed_trades": 0,
            "wins": 0,
            "losses": 0,
            "pushes": 0,
            "total_pnl": 0.0,
            "start_balance": None,
            "current_balance": None,
            "start_time": datetime.now().isoformat()
        }
        
        if simulation:
            self.stats["simulation"] = True
            self.stats["simulated_balance"] = 1.0  # Start with 1 SOL in simulation
    
    def log(self, level: str, message: str, data: Dict = None, skip_file: bool = False):
        """Log a message with optional data"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        if self.simulation:
            entry["simulation"] = True
        
        # Don't save countdown messages to file
        if not skip_file:
            self.logs.append(entry)
        
        # Console output with icons
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "DEBUG": "🔍",
            "TRADE": "💰",
            "SIMULATION": "🎮",
            "COUNTDOWN": "⏱️"
        }
        
        icon = icons.get(level, "")
        sim_prefix = "[SIM] " if self.simulation else ""
        
        # Special formatting for countdown
        if level == "COUNTDOWN":
            # Clear line and print countdown
            print(f"\r{icon} {sim_prefix}{message}", end="", flush=True)
        else:
            print(f"{icon} {sim_prefix}[{level}] {message}")
            if data and level != "COUNTDOWN":
                print(f"  Data: {json.dumps(data, indent=2)}")
        
        if not skip_file:
            self._save()
    
    def update_stats(self, trade_result: str, pnl: float = 0):
        """Update trading statistics"""
        self.stats["total_trades"] += 1
        
        if trade_result == "WIN":
            self.stats["wins"] += 1
            self.stats["successful_trades"] += 1
        elif trade_result == "LOSS":
            self.stats["losses"] += 1
            self.stats["successful_trades"] += 1
        elif trade_result == "PUSH":
            self.stats["pushes"] += 1
            self.stats["successful_trades"] += 1
        else:
            self.stats["failed_trades"] += 1
        
        self.stats["total_pnl"] += pnl
        
        # Calculate win rate
        if self.stats["successful_trades"] > 0:
            self.stats["win_rate"] = (self.stats["wins"] / self.stats["successful_trades"]) * 100
        
        self._save()
    
    def print_stats(self):
        """Print current statistics"""
        print("\n" + "=" * 50)
        print("📊 TRADING STATISTICS")
        print("=" * 50)
        
        if self.simulation:
            print("🎮 SIMULATION MODE")
        
        print(f"Total Trades: {self.stats['total_trades']}")
        print(f"Successful: {self.stats['successful_trades']}")
        print(f"Failed: {self.stats['failed_trades']}")
        print(f"Wins: {self.stats['wins']}")
        print(f"Losses: {self.stats['losses']}")
        print(f"Win Rate: {self.stats.get('win_rate', 0):.1f}%")
        print(f"Total P&L: {self.stats['total_pnl']:+.4f} SOL")
        print("=" * 50)
    
    def _save(self):
        """Save logs and stats to file"""
        try:
            output = {
                "stats": self.stats,
                "logs": self.logs
            }
            with open(self.filename, 'w') as f:
                json.dump(output, f, indent=2)
        except Exception as e:
            print(f"Failed to save log: {e}")


# =================== COUNTDOWN TIMER ===================
class CountdownTimer:
    """Manages countdown display between trades"""
    
    def __init__(self, logger: SmartLogger):
        self.logger = logger
        self.is_counting = False
    
    async def countdown(self, target_time: datetime):
        """Display countdown until target time"""
        self.is_counting = True
        
        try:
            while self.is_counting:
                now = datetime.now()
                
                if now >= target_time:
                    # Clear the countdown line
                    print("\r" + " " * 80 + "\r", end="", flush=True)
                    break
                
                remaining = target_time - now
                total_seconds = int(remaining.total_seconds())
                
                if total_seconds <= 0:
                    break
                
                # Calculate time components
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                
                # Format countdown message
                if hours > 0:
                    countdown_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    countdown_str = f"{minutes:02d}:{seconds:02d}"
                
                # Create progress bar
                total_wait = 15 * 60  # 15 minutes in seconds (or use config)
                elapsed = total_wait - total_seconds
                progress = min(elapsed / total_wait, 1.0)
                bar_length = 30
                filled = int(bar_length * progress)
                bar = "█" * filled + "░" * (bar_length - filled)
                
                # Display countdown with progress bar
                message = f"Next trade in: {countdown_str} [{bar}] {progress*100:.0f}%"
                self.logger.log("COUNTDOWN", message, skip_file=True)
                
                # Update every second
                await asyncio.sleep(1)
                
        except asyncio.CancelledError:
            # Clear the countdown line when cancelled
            print("\r" + " " * 80 + "\r", end="", flush=True)
            self.is_counting = False
        except Exception as e:
            self.is_counting = False
    
    def stop(self):
        """Stop the countdown"""
        self.is_counting = False


# =================== ENHANCED BOT CLASS ===================
class TradingBot:
    """Enhanced trading bot with countdown timer"""
    
    def __init__(self, simulation_mode: bool = False):
        self.config = Config()
        self.config.SIMULATION_MODE = simulation_mode
        self.logger = SmartLogger(
            self.config.LOG_FILE,
            simulation=simulation_mode
        )
        self.countdown = CountdownTimer(self.logger)
        self.playwright = None
        self.context = None
        self.page = None
        self.trade_count = 0
        self.last_trade_time = None
        self.simulated_balance = 1.0 if simulation_mode else None
        self.countdown_task = None
    
    async def setup_browser(self) -> bool:
        """Initialize browser with saved profile"""
        try:
            self.logger.log("INFO", "Starting browser setup")
            
            # Check profile
            profile_path = Path(self.config.PROFILE_DIR)
            if not profile_path.exists():
                self.logger.log("ERROR", f"Profile not found at {profile_path}")
                self.logger.log("INFO", "Run setup.py first")
                return False
            
            # Start Playwright
            self.playwright = await async_playwright().start()
            
            # Launch Chrome
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=str(profile_path),
                channel="chrome",
                headless=False,
                viewport={'width': 1280, 'height': 720},
                args=[
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            
            self.page = await self.context.new_page()
            
            # Navigate
            self.logger.log("INFO", f"Navigating to {self.config.URL}")
            await self.page.goto(
                self.config.URL,
                wait_until='domcontentloaded',
                timeout=self.config.PAGE_TIMEOUT
            )
            
            # Wait for stability
            await asyncio.sleep(5)
            
            if self.config.SIMULATION_MODE:
                self.logger.log("SIMULATION", "Running in SIMULATION MODE - no real trades!")
            
            self.logger.log("SUCCESS", "Browser setup complete")
            return True
            
        except Exception as e:
            self.logger.log("ERROR", f"Browser setup failed: {e}")
            return False
    
    async def read_balance(self) -> Optional[float]:
        """Read balance (real or simulated)"""
        if self.config.SIMULATION_MODE:
            return self.simulated_balance
        
        if not self.config.CHECK_BALANCE:
            return None
        
        try:
            # Try multiple selectors
            selectors = [
                'span:has-text("SOL")',
                '[class*="balance"]:has-text("SOL")',
                'text=/\\d+\\.\\d+\\s*SOL/i',
                'button:has-text("SOL")',
            ]
            
            for selector in selectors:
                try:
                    element = await self.page.wait_for_selector(selector, timeout=2000)
                    if element:
                        text = await element.text_content()
                        import re
                        match = re.search(r'(\d+\.?\d*)', text.replace(',', ''))
                        if match:
                            balance = float(match.group(1))
                            self.logger.log("INFO", f"Balance: {balance} SOL")
                            
                            # Update stats
                            if self.logger.stats["start_balance"] is None:
                                self.logger.stats["start_balance"] = balance
                            self.logger.stats["current_balance"] = balance
                            
                            return balance
                except:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.log("DEBUG", f"Balance read failed: {e}")
            return None
    
    async def _click_with_retry(self, selector: str, description: str) -> bool:
        """Click a button with retry logic"""
        for attempt in range(self.config.CLICK_RETRY):
            try:
                if isinstance(selector, str):
                    element = self.page.locator(selector).first
                else:
                    element = selector
                
                await element.wait_for(state='visible', timeout=self.config.ACTION_TIMEOUT)
                await element.click()
                
                self.logger.log("DEBUG", f"Clicked {description} (attempt {attempt + 1})")
                return True
                
            except Exception as e:
                if attempt == self.config.CLICK_RETRY - 1:
                    self.logger.log("ERROR", f"Failed to click {description} after {self.config.CLICK_RETRY} attempts: {e}")
                    return False
                await asyncio.sleep(0.5)
        
        return False
    
    async def _enter_amount_with_retry(self, amount: float) -> bool:
        """Enter amount with better error handling"""
        selectors = [
            'input[placeholder="BET AMOUNT"]',
            'input[type="number"]',
            'input[name*="amount"]',
            'input:visible'
        ]
        
        for selector in selectors:
            try:
                elements = self.page.locator(selector)
                count = await elements.count()
                
                for i in range(count):
                    elem = elements.nth(i)
                    if await elem.is_visible():
                        await elem.click()
                        await elem.fill("")
                        await elem.type(str(amount), delay=50)
                        
                        # Verify the value was entered
                        value = await elem.input_value()
                        if str(amount) in value:
                            self.logger.log("DEBUG", f"Successfully entered amount: {amount}")
                            return True
            except:
                continue
        
        self.logger.log("ERROR", "Could not enter amount")
        return False
    
    async def place_trade(self) -> Tuple[bool, str]:
        """Execute trade with enhanced error handling"""
        # Stop countdown if running
        if self.countdown_task and not self.countdown_task.done():
            self.countdown_task.cancel()
            self.countdown.stop()
            # Clear countdown line
            print("\r" + " " * 80 + "\r", end="", flush=True)
        
        try:
            self.trade_count += 1
            trade_id = f"Trade #{self.trade_count}"
            
            print()  # New line after countdown
            self.logger.log("SUCCESS", f"=== Starting {trade_id} ===")
            self.logger.log("INFO", f"Time: {datetime.now().strftime('%H:%M:%S')}")
            
            if self.config.SIMULATION_MODE:
                self.logger.log("SIMULATION", "Simulating trade execution...")
            
            # Read initial balance
            balance_before = await self.read_balance()
            
            # Step 1: Interval
            self.logger.log("INFO", f"Step 1/5: Selecting interval {self.config.INTERVAL}")
            if not await self._click_with_retry(
                f'button:has-text("{self.config.INTERVAL}")',
                f"interval {self.config.INTERVAL}"
            ):
                return False, "FAILED"
            await asyncio.sleep(1)
            
            # Step 2: Amount
            self.logger.log("INFO", f"Step 2/5: Entering amount {self.config.BET_AMOUNT}")
            if not await self._enter_amount_with_retry(self.config.BET_AMOUNT):
                return False, "FAILED"
            await asyncio.sleep(1)
            
            # Step 3: Leverage
            self.logger.log("INFO", f"Step 3/5: Selecting leverage {self.config.LEVERAGE}")
            if not await self._click_with_retry(
                f'button:has-text("{self.config.LEVERAGE}")',
                f"leverage {self.config.LEVERAGE}"
            ):
                return False, "FAILED"
            await asyncio.sleep(1)
            
            # Step 4: Trade direction
            self.logger.log("INFO", f"Step 4/5: Selecting {self.config.TRADE_MODE} direction")
            if self.config.TRADE_MODE == "BUY":
                card_selectors = [
                    'div.tradezone-card-green',
                    '[class*="card-green"]',
                    'div:has-text("ABOVE"):has(button)'
                ]
                trade_type = "BUY (ABOVE)"
            else:
                card_selectors = [
                    'div.tradezone-card-red',
                    '[class*="card-red"]',
                    'div:has-text("BELOW"):has(button)'
                ]
                trade_type = "SELL (BELOW)"
            
            # Click card
            card_clicked = False
            for selector in card_selectors:
                try:
                    card = self.page.locator(selector).first
                    if await card.is_visible(timeout=1000):
                        await card.click()
                        card_clicked = True
                        self.logger.log("DEBUG", f"Clicked {trade_type} card")
                        break
                except:
                    continue
            
            if not card_clicked:
                self.logger.log("ERROR", f"Could not find {trade_type} card")
                return False, "FAILED"
            
            await asyncio.sleep(0.5)
            
            # Step 5: Confirm (YES button)
            self.logger.log("INFO", "Step 5/5: Confirming trade")
            if self.config.SIMULATION_MODE:
                self.logger.log("SIMULATION", "Skipping YES button click (simulation mode)")
                
                # Simulate win/loss randomly
                import random
                if random.random() > 0.5:
                    self.simulated_balance += (self.config.BET_AMOUNT * 3)  # Win
                    result = "WIN"
                    pnl = self.config.BET_AMOUNT * 3
                else:
                    self.simulated_balance -= self.config.BET_AMOUNT  # Loss
                    result = "LOSS"
                    pnl = -self.config.BET_AMOUNT
                
                self.logger.log("SIMULATION", f"Simulated {result}: Balance {self.simulated_balance:.4f} SOL")
                self.logger.update_stats(result, pnl)
                
            else:
                # Real trade - click YES
                yes_clicked = await self._click_with_retry(
                    f'button:has-text("YES {self.config.LEVERAGE}")',
                    "YES button"
                )
                
                if not yes_clicked:
                    # Try generic YES button
                    yes_clicked = await self._click_with_retry(
                        'button:has-text("YES")',
                        "YES button (generic)"
                    )
                
                if yes_clicked:
                    self.logger.log("SUCCESS", f"✅ Executed {trade_type} trade")
                    
                    # Check balance change
                    await asyncio.sleep(5)
                    balance_after = await self.read_balance()
                    
                    if balance_before is not None and balance_after is not None:
                        pnl = balance_after - balance_before
                        if pnl > 0:
                            result = "WIN"
                        elif pnl < 0:
                            result = "LOSS"
                        else:
                            result = "PUSH"
                        
                        self.logger.log("TRADE", f"Result: {result} ({pnl:+.4f} SOL)")
                        self.logger.update_stats(result, pnl)
                    else:
                        result = "UNKNOWN"
                else:
                    return False, "FAILED"
            
            # Record trade time
            self.last_trade_time = datetime.now()
            
            return True, result
            
        except Exception as e:
            self.logger.log("ERROR", f"Trade execution error: {e}")
            self.logger.update_stats("FAILED", 0)
            return False, "FAILED"
    
    async def wait_with_countdown(self, target_time: datetime):
        """Wait until target time with countdown display"""
        if self.config.SHOW_COUNTDOWN:
            # Start countdown in background
            self.countdown_task = asyncio.create_task(self.countdown.countdown(target_time))
            
            # Wait until target time
            while datetime.now() < target_time:
                await asyncio.sleep(0.5)
            
            # Stop countdown
            if self.countdown_task and not self.countdown_task.done():
                self.countdown_task.cancel()
                self.countdown.stop()
        else:
            # Simple wait without countdown
            wait_seconds = (target_time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                self.logger.log("INFO", f"Waiting {wait_seconds/60:.1f} minutes until next trade")
                await asyncio.sleep(wait_seconds)
    
    async def run(self):
        """Main trading loop with countdown timer"""
        try:
            if not await self.setup_browser():
                return
            
            mode = "SIMULATION" if self.config.SIMULATION_MODE else "LIVE"
            self.logger.log("SUCCESS", f"Bot started in {mode} mode!")
            self.logger.log("INFO", f"Trading every {self.config.TRADE_FREQUENCY} minutes")
            
            # Main loop
            trade_errors = 0
            max_errors = 5
            
            while True:
                try:
                    # Calculate next trade time
                    if self.last_trade_time is None:
                        # First trade - execute immediately
                        next_trade_time = datetime.now()
                    else:
                        next_trade_time = self.last_trade_time + timedelta(minutes=self.config.TRADE_FREQUENCY)
                    
                    # Wait if not time yet (with countdown)
                    if next_trade_time > datetime.now():
                        await self.wait_with_countdown(next_trade_time)
                    
                    # Execute trade
                    success, result = await self.place_trade()
                    
                    if not success:
                        trade_errors += 1
                        self.logger.log("WARNING", f"Trade failed ({trade_errors}/{max_errors} errors)")
                        
                        if trade_errors >= max_errors:
                            self.logger.log("ERROR", "Too many trade errors, stopping bot")
                            break
                        
                        # Reload page to recover
                        try:
                            await self.page.reload()
                            await asyncio.sleep(5)
                        except:
                            pass
                    else:
                        trade_errors = 0  # Reset error counter on success
                    
                    # Print statistics periodically
                    if self.trade_count % 5 == 0:
                        self.logger.print_stats()
                    
                    # Set up next trade time
                    next_trade_time = datetime.now() + timedelta(minutes=self.config.TRADE_FREQUENCY)
                    self.logger.log("INFO", f"Next trade scheduled for: {next_trade_time.strftime('%H:%M:%S')}")
                    
                except KeyboardInterrupt:
                    self.logger.log("INFO", "Stopped by user")
                    break
                except Exception as e:
                    self.logger.log("ERROR", f"Loop error: {e}")
                    # Still wait full cycle on error
                    next_trade_time = datetime.now() + timedelta(minutes=self.config.TRADE_FREQUENCY)
                    await self.wait_with_countdown(next_trade_time)
            
            # Final statistics
            self.logger.print_stats()
            
        finally:
            # Cancel countdown if running
            if self.countdown_task and not self.countdown_task.done():
                self.countdown_task.cancel()
            await self.cleanup()
    
    async def cleanup(self):
        """Clean up resources"""
        self.logger.log("INFO", "Shutting down...")
        
        for resource in [self.page, self.context, self.playwright]:
            if resource:
                try:
                    if resource == self.page:
                        await resource.close()
                    elif resource == self.context:
                        await resource.close()
                    elif resource == self.playwright:
                        await resource.stop()
                except:
                    pass
        
        self.logger.log("SUCCESS", "Shutdown complete")


# =================== MAIN ENTRY POINT ===================
async def main():
    """Main entry point with simulation option"""
    
    # Check for simulation mode flag
    simulation = "--simulate" in sys.argv or "-s" in sys.argv
    
    print("=" * 50)
    print("SIMPLE TRADING BOT FOR 0DTE.IO")
    print("=" * 50)
    
    if simulation:
        print("🎮 SIMULATION MODE - No real trades!")
    else:
        print("💰 LIVE TRADING MODE")
    
    print(f"⏱️  Trading every 15 minutes")
    print(f"📊 Trade settings: 15M | 4X | 0.01 SOL")
    print("=" * 50)
    
    if not simulation:
        response = input("\n⚠️  This will trade with REAL money. Continue? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    print("\nStarting bot...\n")
    bot = TradingBot(simulation_mode=simulation)
    
    try:
        await bot.run()
    except KeyboardInterrupt:
        print("\n\n[INFO] Bot stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")


if __name__ == "__main__":
    asyncio.run(main())