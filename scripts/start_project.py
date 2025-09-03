#!/usr/bin/env python3
"""
NewsFaces Project Startup Script
Run this to start the complete pipeline or launch the dashboard
"""

import os
import sys
import subprocess

def main():
    print("NewsFaces Project Startup")
    print("=" * 40)
    print("Choose an option:")
    print("1. Run Complete Pipeline (main.py)")
    print("2. Launch Streamlit Dashboard")
    print("3. Check Project Status")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\nStarting complete pipeline...")
            print("This will process WARC files and extract articles/images")
            print("May take several minutes...")
            
            confirm = input("Continue? (y/n): ").strip().lower()
            if confirm == 'y':
                try:
                    subprocess.run([sys.executable, "main.py"], check=True)
                    print("\nPipeline completed successfully!")
                except subprocess.CalledProcessError as e:
                    print(f"\nPipeline failed: {e}")
                except KeyboardInterrupt:
                    print("\n⏹️ Pipeline interrupted by user")
            break
            
        elif choice == "2":
            print("\nLaunching Streamlit dashboard...")
            try:
                subprocess.run([sys.executable, "apps/run_streamlit.py"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"\nFailed to launch dashboard: {e}")
            break
            
        elif choice == "3":
            print("\nProject Status:")
            print("-" * 20)
            
            # Check database
            if os.path.exists("data/database/newsfaces.db"):
                print("Database: Found")
            else:
                print("❌ Database: Not found")
            
            # Check extracted data
            if os.path.exists("data/extracted_data/html"):
                html_files = len([f for f in os.listdir("data/extracted_data/html") if f.endswith('.html')])
                print(f"HTML Files: {html_files}")
            else:
                print("HTML Files: None")
            
            if os.path.exists("data/extracted_data/images"):
                img_files = len([f for f in os.listdir("data/extracted_data/images") if f.endswith(('.jpg', '.png', '.jpeg'))])
                print(f"Images: {img_files}")
            else:
                print("Images: None")
            
            # Check WARC files
            if os.path.exists("data/extracted_data"):
                warc_files = [f for f in os.listdir("data/extracted_data") if f.endswith('.warc.gz')]
                print(f"WARC Files: {len(warc_files)}")
            else:
                print("WARC Files: None")
            
            print("\n" + "=" * 40)
            continue
            
        elif choice == "4":
            print("\nGoodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
