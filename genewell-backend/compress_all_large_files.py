#!/usr/bin/env python3
"""
Comprehensive Large File Compression Script
==========================================

This script compresses all large files in the repository to make them
compatible with GitHub's file size limits.
"""

import os
import gzip
import shutil
import pandas as pd
from pathlib import Path

def get_file_size_mb(file_path):
    """Get file size in MB"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    return 0

def compress_csv_file(csv_path, compression='gzip'):
    """Compress CSV file and return compressed path"""
    if not os.path.exists(csv_path):
        return None
    
    # Read CSV with pandas for better compression
    try:
        df = pd.read_csv(csv_path)
        
        # Create compressed version
        compressed_path = csv_path + '.gz'
        df.to_csv(compressed_path, compression='gzip', index=False)
        
        original_size = get_file_size_mb(csv_path)
        compressed_size = get_file_size_mb(compressed_path)
        
        print(f"  📁 {os.path.basename(csv_path)}: {original_size:.2f} MB → {compressed_size:.2f} MB")
        
        return compressed_path
        
    except Exception as e:
        print(f"  ❌ Error compressing {csv_path}: {e}")
        return None

def compress_pickle_file(pkl_path):
    """Compress pickle file"""
    if not os.path.exists(pkl_path):
        return None
    
    try:
        compressed_path = pkl_path + '.gz'
        
        # Read and compress
        with open(pkl_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb', compresslevel=9) as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        original_size = get_file_size_mb(pkl_path)
        compressed_size = get_file_size_mb(compressed_path)
        
        print(f"  📁 {os.path.basename(pkl_path)}: {original_size:.2f} MB → {compressed_size:.2f} MB")
        
        return compressed_path
        
    except Exception as e:
        print(f"  ❌ Error compressing {pkl_path}: {e}")
        return None

def analyze_and_compress_files():
    """Analyze all files and compress large ones"""
    print("=== Large File Analysis & Compression ===\n")
    
    # Define files to check and compress
    files_to_check = [
        'personalized_model_backup.pkl',
        'ml_training_dataset_20250823_003021.csv',
        'personalized_gene_disease_dataset_20250823_003017.csv',
        'personalized_gene_disease_dataset_20250823_002959.csv'
    ]
    
    large_files = []
    compressed_files = []
    
    print("📊 Analyzing file sizes...")
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size_mb = get_file_size_mb(file_path)
            print(f"  📁 {file_path}: {size_mb:.2f} MB")
            
            if size_mb > 10:  # Files larger than 10MB
                large_files.append((file_path, size_mb))
    
    if not large_files:
        print("\n✅ No large files found!")
        return
    
    print(f"\n⚠️  Found {len(large_files)} large files to compress")
    
    # Compress large files
    print("\n🔄 Compressing large files...")
    for file_path, size_mb in large_files:
        print(f"\nCompressing: {file_path}")
        
        if file_path.endswith('.csv'):
            compressed_path = compress_csv_file(file_path)
        elif file_path.endswith('.pkl'):
            compressed_path = compress_pickle_file(file_path)
        else:
            print(f"  ⚠️  Unknown file type: {file_path}")
            continue
        
        if compressed_path:
            compressed_files.append((file_path, compressed_path))
            
            # Check if compression was successful
            compressed_size = get_file_size_mb(compressed_path)
            if compressed_size < 100:
                print(f"  ✅ Successfully compressed below 100MB limit")
            else:
                print(f"  ⚠️  Still large after compression: {compressed_size:.2f} MB")
    
    return compressed_files

def cleanup_original_large_files(compressed_files):
    """Remove original large files after successful compression"""
    print("\n🧹 Cleaning up original large files...")
    
    for original_path, compressed_path in compressed_files:
        if os.path.exists(compressed_path):
            compressed_size = get_file_size_mb(compressed_path)
            
            if compressed_size < 100:
                # Safe to remove original
                try:
                    os.remove(original_path)
                    print(f"  ✅ Removed: {os.path.basename(original_path)}")
                except Exception as e:
                    print(f"  ❌ Error removing {original_path}: {e}")
            else:
                print(f"  ⚠️  Keeping original: {os.path.basename(original_path)} (compressed still too large)")

def create_compression_report():
    """Create a report of all compressed files"""
    print("\n📋 Compression Report")
    print("=" * 50)
    
    compressed_files = [
        'personalized_model.pkl.gz',
        'ml_training_dataset_20250823_003021.csv.gz',
        'personalized_gene_disease_dataset_20250823_003017.csv.gz',
        'personalized_gene_disease_dataset_20250823_002959.csv.gz'
    ]
    
    total_original_size = 0
    total_compressed_size = 0
    
    for file_path in compressed_files:
        if os.path.exists(file_path):
            size_mb = get_file_size_mb(file_path)
            print(f"📁 {file_path}: {size_mb:.2f} MB")
            total_compressed_size += size_mb
    
    print(f"\n📊 Total compressed size: {total_compressed_size:.2f} MB")
    
    if total_compressed_size < 100:
        print("✅ All files are now below GitHub's 100MB limit!")
    else:
        print("⚠️  Some files are still too large for GitHub")

def main():
    """Main compression function"""
    try:
        # Analyze and compress files
        compressed_files = analyze_and_compress_files()
        
        if compressed_files:
            # Clean up original files
            cleanup_original_large_files(compressed_files)
            
            # Create report
            create_compression_report()
            
            print("\n🎉 File compression completed!")
            print("\n💡 Next steps:")
            print("1. Commit the compressed files to Git")
            print("2. Update your code to load compressed files")
            print("3. Push to GitHub (should work now!)")
        else:
            print("\n✅ No compression needed!")
            
    except Exception as e:
        print(f"\n❌ Error during compression: {e}")

if __name__ == "__main__":
    main()
