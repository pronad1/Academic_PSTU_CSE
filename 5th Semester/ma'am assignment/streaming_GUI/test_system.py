"""
System Check and Test Script
Verifies all components are ready for the streaming application
Author: Your Name
Date: November 21, 2025
"""

import sys
import os
import importlib.util

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check if Python version is adequate"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✓ Python version is adequate (3.7+)")
        return True
    else:
        print("✗ Python 3.7 or higher is required")
        return False

def check_modules():
    """Check if all required modules are available"""
    print_header("Checking Required Modules")
    
    required_modules = [
        'tkinter',
        'socket',
        'threading',
        'os',
        'subprocess',
        'datetime',
        'random',
        'time'
    ]
    
    all_present = True
    for module in required_modules:
        try:
            if module == 'tkinter':
                import tkinter
            else:
                __import__(module)
            print(f"✓ {module:15} - Available")
        except ImportError:
            print(f"✗ {module:15} - Missing")
            all_present = False
    
    return all_present

def check_project_files():
    """Check if all project files exist"""
    print_header("Checking Project Files")
    
    required_files = [
        'main_gui.py',
        'server.py',
        'client.py',
        'config.py',
        'README.md',
        'QUICK_START.md',
        'requirements.txt'
    ]
    
    all_present = True
    for filename in required_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✓ {filename:20} - {size:,} bytes")
        else:
            print(f"✗ {filename:20} - Not found")
            all_present = False
    
    return all_present

def check_gui_support():
    """Check if GUI is supported"""
    print_header("Checking GUI Support")
    
    try:
        import tkinter as tk
        # Try to create a hidden window
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        print("✓ GUI (Tkinter) is fully functional")
        return True
    except Exception as e:
        print(f"✗ GUI Error: {str(e)}")
        return False

def test_socket():
    """Test socket functionality"""
    print_header("Testing Socket Functionality")
    
    try:
        import socket
        # Create a test UDP socket
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.close()
        print("✓ UDP socket creation successful")
        return True
    except Exception as e:
        print(f"✗ Socket Error: {str(e)}")
        return False

def create_downloads_folder():
    """Create downloads folder if it doesn't exist"""
    print_header("Setting Up Downloads Folder")
    
    try:
        downloads_dir = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(downloads_dir, exist_ok=True)
        print(f"✓ Downloads folder ready: {downloads_dir}")
        return True
    except Exception as e:
        print(f"✗ Error creating downloads folder: {str(e)}")
        return False

def main():
    """Run all checks"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║   UDP Media Streaming Application - System Check         ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Required Modules", check_modules()))
    results.append(("Project Files", check_project_files()))
    results.append(("GUI Support", check_gui_support()))
    results.append(("Socket Functionality", test_socket()))
    results.append(("Downloads Folder", create_downloads_folder()))
    
    # Summary
    print_header("Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}\n")
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {test_name}")
    
    print("\n" + "="*60)
    
    if passed == total:
        print("\n✓ All checks passed! The application is ready to run.")
        print("\n  To start the application, run:")
        print("  → python main_gui.py")
        print("\n  Or launch components individually:")
        print("  → python server.py")
        print("  → python client.py")
    else:
        print("\n✗ Some checks failed. Please resolve the issues above.")
        print("\n  Common solutions:")
        print("  • Install Python 3.7 or higher")
        print("  • Install tkinter: sudo apt-get install python3-tk (Linux)")
        print("  • Ensure all project files are in the same directory")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {str(e)}")
