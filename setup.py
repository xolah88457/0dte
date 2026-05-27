"""
Setup Script - Create Chrome profile and login with Google
Run this once before using the bot
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

PROFILE_DIR = r"C:\ChromeProfiles\0dte_profile"
SITE_URL = "https://0dte.io"

async def setup_profile():
    """Create Chrome profile and login with Google"""
    print("=" * 50)
    print("TRADING BOT SETUP - Google Login")
    print("=" * 50)
    print(f"\n📁 Profile will be created at: {PROFILE_DIR}")
    
    # Create profile directory
    profile_path = Path(PROFILE_DIR)
    profile_path.mkdir(parents=True, exist_ok=True)
    
    playwright = await async_playwright().start()
    
    try:
        print("\n🚀 Launching Chrome...")
        
        # Launch Chrome with persistent profile
        context = await playwright.chromium.launch_persistent_context(
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
        
        page = await context.new_page()
        
        print(f"\n🌐 Navigating to {SITE_URL}...")
        await page.goto(SITE_URL)
        await asyncio.sleep(3)  # Wait for page to load
        
        print("\n" + "=" * 50)
        print("MANUAL SETUP REQUIRED:")
        print("=" * 50)
        print("\n1️⃣  Login to the site:")
        print("   - Click 'Login' or 'Sign In' button")
        print("   - Use Google login OR any other method")
        print("   - Complete any 2FA if required")
        
        print("\n2️⃣  Make sure you can see the trading interface:")
        print("   - You should see trading cards")
        print("   - Buttons like '15M', '4X' should be visible")
        print("   - The page should be fully loaded")
        
        print("\n3️⃣  Once logged in and ready:")
        print("   - The browser will save your session")
        print("   - You won't need to login again")
        print("\n" + "=" * 50)
        
        print("\n⏳ Please complete the login process...")
        print("   Take your time, the browser will wait")
        
        input("\n✅ Press ENTER when you're fully logged in and ready...")
        
        # Simple check - just make sure we're still on the right site
        current_url = page.url
        if "0dte.io" in current_url:
            print("\n✅ Still on 0dte.io - good!")
        else:
            print(f"\n⚠️  Current URL: {current_url}")
            print("   Make sure you're on the right site")
        
        # Try to take a screenshot for verification
        try:
            screenshot_path = "setup_complete.png"
            await page.screenshot(path=screenshot_path)
            print(f"\n📸 Screenshot saved as {screenshot_path}")
            print("   You can check this to verify the setup worked")
        except:
            pass
        
        print("\n" + "=" * 50)
        print("✨ Setup completed!")
        print("\n📝 Your login session has been saved")
        print("🚀 You can now run the trading bot: python bot.py")
        print("\n⚠️  Note: If the bot can't trade, run setup.py again")
        print("=" * 50)
        
        await context.close()
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("   Please try again")
    finally:
        await playwright.stop()


async def clear_profile():
    """Clear existing profile if needed"""
    profile_path = Path(PROFILE_DIR)
    if profile_path.exists():
        print(f"\n⚠️  Profile already exists at {PROFILE_DIR}")
        response = input("Do you want to clear it and start fresh? (y/n): ")
        if response.lower() == 'y':
            import shutil
            try:
                shutil.rmtree(profile_path)
                print("✅ Profile cleared")
                return True
            except Exception as e:
                print(f"❌ Could not clear profile: {e}")
                print("   Close all Chrome windows and try again")
                return False
    return True


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("0DTE.IO BOT SETUP")
    print("=" * 50)
    print("\nThis will:")
    print("1. Create/update a Chrome profile")
    print("2. Open 0dte.io")
    print("3. Let you login (Google or any method)")
    print("4. Save your session for the bot\n")
    
    # Check if we should clear existing profile
    if asyncio.run(clear_profile()):
        # Run setup
        asyncio.run(setup_profile())
    else:
        print("\nSetup cancelled")