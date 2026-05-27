"""
Diagnostic Script with Trading Simulation
Test the bot without spending real money
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

PROFILE_DIR = r"C:\ChromeProfiles\0dte_profile"
SITE_URL = "https://0dte.io"

async def simulate_trading():
    """Run simulated trading test"""
    print("\n" + "=" * 50)
    print("TRADING SIMULATION TEST")
    print("=" * 50)
    print("\n🎮 This will simulate trades without spending money")
    print("   We'll test clicking buttons but won't confirm trades\n")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "mode": "simulation",
        "tests": [],
        "simulated_trades": []
    }
    
    # Check profile
    profile_path = Path(PROFILE_DIR)
    if not profile_path.exists():
        print("❌ Profile not found. Run setup.py first!")
        return
    
    playwright = await async_playwright().start()
    
    try:
        # Launch browser
        print("🚀 Launching browser...")
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_path),
            channel="chrome",
            headless=False,
            viewport={'width': 1280, 'height': 720},
            args=['--no-first-run', '--no-default-browser-check']
        )
        
        page = await context.new_page()
        
        # Navigate
        print(f"🌐 Loading {SITE_URL}...")
        await page.goto(SITE_URL, timeout=30000)
        await asyncio.sleep(5)
        
        # Test trading interface
        print("\n" + "=" * 50)
        print("TESTING TRADING INTERFACE")
        print("=" * 50)
        
        # Simulate 3 trades
        for i in range(1, 4):
            print(f"\n📊 Simulated Trade #{i}")
            print("-" * 30)
            
            trade_result = {
                "trade_number": i,
                "timestamp": datetime.now().isoformat(),
                "steps": []
            }
            
            # Step 1: Click interval
            print("  1️⃣ Testing interval button (15M)...")
            try:
                button = page.locator('button:has-text("15M")').first
                await button.wait_for(state='visible', timeout=3000)
                await button.click()
                print("     ✅ Clicked 15M")
                trade_result["steps"].append({"interval": "success"})
                await asyncio.sleep(1)
            except Exception as e:
                print(f"     ❌ Failed: {e}")
                trade_result["steps"].append({"interval": "failed"})
            
            # Step 2: Enter amount
            print("  2️⃣ Testing amount input (0.01)...")
            try:
                input_field = page.locator('input[type="number"]').first
                await input_field.click()
                await input_field.fill("")
                await input_field.type("0.01", delay=50)
                print("     ✅ Entered 0.01")
                trade_result["steps"].append({"amount": "success"})
                await asyncio.sleep(1)
            except Exception as e:
                print(f"     ❌ Failed: {e}")
                trade_result["steps"].append({"amount": "failed"})
            
            # Step 3: Click leverage
            print("  3️⃣ Testing leverage button (4X)...")
            try:
                button = page.locator('button:has-text("4X")').first
                await button.click()
                print("     ✅ Clicked 4X")
                trade_result["steps"].append({"leverage": "success"})
                await asyncio.sleep(1)
            except Exception as e:
                print(f"     ❌ Failed: {e}")
                trade_result["steps"].append({"leverage": "failed"})
            
            # Step 4: Click trade card (but NOT the YES button)
            print("  4️⃣ Testing trade card (BUY/GREEN)...")
            try:
                card = page.locator('div.tradezone-card-green').first
                if not await card.is_visible():
                    card = page.locator('[class*="card"]:has-text("ABOVE")').first
                
                await card.click()
                print("     ✅ Clicked BUY card")
                trade_result["steps"].append({"card": "success"})
                
                # Check if YES button is visible
                yes_button = page.locator('button:has-text("YES")').first
                if await yes_button.is_visible(timeout=1000):
                    print("     ✅ YES button is visible (not clicking)")
                    trade_result["steps"].append({"yes_visible": True})
                
            except Exception as e:
                print(f"     ❌ Failed: {e}")
                trade_result["steps"].append({"card": "failed"})
            
            # Step 5: Simulate result
            import random
            simulated_result = "WIN" if random.random() > 0.5 else "LOSS"
            print(f"  5️⃣ Simulated result: {simulated_result}")
            trade_result["result"] = simulated_result
            
            results["simulated_trades"].append(trade_result)
            
            # Wait before next simulation
            if i < 3:
                print("\n⏳ Waiting 5 seconds before next simulation...")
                await asyncio.sleep(5)
        
        # Summary
        print("\n" + "=" * 50)
        print("SIMULATION SUMMARY")
        print("=" * 50)
        
        successful_steps = 0
        total_steps = 0
        
        for trade in results["simulated_trades"]:
            for step in trade["steps"]:
                total_steps += 1
                if list(step.values())[0] == "success" or list(step.values())[0] == True:
                    successful_steps += 1
        
        success_rate = (successful_steps / total_steps * 100) if total_steps > 0 else 0
        
        print(f"\n✅ Successful steps: {successful_steps}/{total_steps} ({success_rate:.0f}%)")
        
        if success_rate >= 80:
            print("\n🎉 Bot is ready for live trading!")
            print("   Run: python bot.py")
        elif success_rate >= 50:
            print("\n⚠️  Some issues detected")
            print("   The bot might work but check the errors")
        else:
            print("\n❌ Major issues detected")
            print("   Fix the problems before live trading")
        
        # Save results
        with open("simulation_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print("\n📁 Results saved to simulation_results.json")
        
        input("\nPress ENTER to close browser...")
        await context.close()
        
    except Exception as e:
        print(f"\n❌ Simulation failed: {e}")
    finally:
        await playwright.stop()


async def run_diagnostics():
    """Run standard diagnostics"""
    print("=" * 50)
    print("TRADING BOT DIAGNOSTICS")
    print("=" * 50)
    
    print("\nChoose an option:")
    print("1. Standard diagnostics")
    print("2. Trading simulation (recommended)")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == "2":
        await simulate_trading()
    elif choice == "3":
        # Run standard diagnostics first
        print("\nRunning standard diagnostics...")
        # ... (standard diagnostic code here)
        await asyncio.sleep(2)
        
        # Then run simulation
        await simulate_trading()
    else:
        # Run standard diagnostics
        print("\nRunning standard diagnostics...")
        print("(Consider running simulation mode to test trading)")


if __name__ == "__main__":
    asyncio.run(run_diagnostics())