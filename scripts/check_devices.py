import subprocess
import platform

def check_battery():
    """Check laptop battery status"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        try:
            result = subprocess.run(
                ["pmset", "-g", "batt"],
                capture_output=True,
                text=True
            )
            output = result.stdout
            
            if "%" in output:
                battery_line = [l for l in output.split('\n') if '%' in l][0]
                print(f"🔋 Battery Status: {battery_line.strip()}")
                
                if "100%" in battery_line:
                    print("✅ Fully charged")
                elif "charging" in battery_line.lower():
                    print("⚡ Charging...")
                else:
                    print("⚠️  Not at 100% - plug in charger!")
                
        except Exception as e:
            print(f"❌ Could not check battery: {e}")
    
    elif system == "Linux":
        try:
            with open("/sys/class/power_supply/BAT0/capacity", "r") as f:
                capacity = f.read().strip()
                print(f"🔋 Battery: {capacity}%")
                
                if int(capacity) == 100:
                    print("✅ Fully charged")
                else:
                    print("⚠️  Not at 100% - plug in charger!")
        except:
            print("⚠️  Could not read battery status")
    
    else:
        print("⚠️  Battery check not supported on Windows via script")
        print("   Please check manually: Settings > System > Battery")

if __name__ == "__main__":
    print("=== Device Check ===\n")
    check_battery()
    print("\n📱 Manual Checks:")
    print("   [ ] Phone fully charged")
    print("   [ ] Power bank charged")
    print("   [ ] All adapters packed (HDMI, USB-C)")
