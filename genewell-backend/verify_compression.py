#!/usr/bin/env python3
"""
Compression Verification Script
==============================

This script verifies that all files are now below GitHub's 100MB limit.
"""

import os
import glob

def get_file_size_mb(file_path):
    """Get file size in MB"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    return 0

def verify_compression():
    """Verify all files are below GitHub's size limit"""
    print("=== Compression Verification ===\n")
    
    # Check all files in the directory
    all_files = []
    for file_path in os.listdir('.'):
        if os.path.isfile(file_path):
            size_mb = get_file_size_mb(file_path)
            all_files.append((file_path, size_mb))
    
    # Sort by size (largest first)
    all_files.sort(key=lambda x: x[1], reverse=True)
    
    print("📊 File Size Analysis:")
    print("-" * 60)
    
    large_files = []
    total_size = 0
    
    for file_path, size_mb in all_files:
        total_size += size_mb
        
        if size_mb > 100:
            status = "❌ EXCEEDS LIMIT"
            large_files.append((file_path, size_mb))
        elif size_mb > 10:
            status = "⚠️  LARGE"
        elif size_mb > 1:
            status = "✅ GOOD"
        else:
            status = "✅ EXCELLENT"
        
        print(f"{file_path:<50} {size_mb:>8.2f} MB {status}")
    
    print("-" * 60)
    print(f"Total repository size: {total_size:.2f} MB")
    
    # Check for any files that still exceed limits
    if large_files:
        print(f"\n❌ Found {len(large_files)} files that still exceed GitHub's 100MB limit:")
        for file_path, size_mb in large_files:
            print(f"  - {file_path}: {size_mb:.2f} MB")
        return False
    else:
        print(f"\n✅ All files are below GitHub's 100MB limit!")
        return True

def check_compressed_files():
    """Check compressed file sizes"""
    print("\n📦 Compressed File Analysis:")
    print("-" * 40)
    
    compressed_files = glob.glob("*.gz")
    if not compressed_files:
        print("No compressed files found")
        return
    
    total_compressed_size = 0
    for file_path in compressed_files:
        size_mb = get_file_size_mb(file_path)
        total_compressed_size += size_mb
        print(f"{file_path:<40} {size_mb:>8.2f} MB")
    
    print("-" * 40)
    print(f"Total compressed size: {total_compressed_size:.2f} MB")

if __name__ == "__main__":
    try:
        # Verify compression
        if verify_compression():
            print("\n🎉 Repository is ready for GitHub!")
            print("💡 You can now commit and push your code.")
        else:
            print("\n⚠️  Some files still need attention before pushing to GitHub.")
        
        # Check compressed files
        check_compressed_files()
        
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
