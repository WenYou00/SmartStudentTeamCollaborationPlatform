"""
main.py - Main Program
"""

import sys

def main():
    """Main function"""
    try:
        print("\n" + "="*70)
        print("SMART STUDENT TEAM COLLABORATION PLATFORM")
        print("="*70)
        
        from ui_system import MainApplication
        app = MainApplication()
        app.run()
        
    except ImportError as e:
        print(f"\nERROR: Failed to import modules")
        print(f"Details: {e}")
        print("\nFiles needed: models.py, ui_system.py, main.py")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nProgram terminated.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()