#!/usr/bin/env python3
"""
Model Optimization Script
========================

This script optimizes the existing large model to reduce file size
and make it compatible with GitHub's file size limits.
"""

import os
import shutil
from personalized_predictor import PersonalizedPredictor

def optimize_model():
    """Optimize the existing model to reduce file size"""
    print("=== Model Optimization Script ===\n")
    
    # Check if large model exists
    if os.path.exists('personalized_model.pkl'):
        old_size = os.path.getsize('personalized_model.pkl') / (1024 * 1024)  # MB
        print(f"Found existing model: {old_size:.2f} MB")
        
        if old_size > 100:
            print("⚠️  Model exceeds GitHub's 100 MB limit!")
            
            # Backup old model
            backup_path = 'personalized_model_backup.pkl'
            shutil.copy2('personalized_model.pkl', backup_path)
            print(f"✅ Backed up old model to {backup_path}")
            
            # Delete old model
            os.remove('personalized_model.pkl')
            print("✅ Deleted old large model")
            
            # Train new optimized model
            print("\n🔄 Training new optimized model...")
            train_optimized_model()
            
        else:
            print("✅ Model is already within size limits")
            return True
    else:
        print("❌ No existing model found")
        print("🔄 Training new optimized model...")
        train_optimized_model()
    
    return True

def train_optimized_model():
    """Train a new optimized model"""
    try:
        # Initialize predictor
        predictor = PersonalizedPredictor()
        
        # Load and preprocess data
        print("1. Loading and preprocessing data...")
        X, y = predictor.load_and_preprocess()
        
        # Train optimized model
        print("2. Training optimized model...")
        r2, rmse = predictor.train_optimized_model(X, y)
        
        # Save optimized model
        print("3. Saving optimized model...")
        predictor.save_optimized_model()
        
        # Check final sizes
        print("\n=== Model Size Analysis ===")
        check_model_sizes()
        
        print(f"\n✅ Optimized model training completed!")
        print(f"Performance - R²: {r2:.4f}, RMSE: {rmse:.4f}")
        
    except Exception as e:
        print(f"❌ Error training optimized model: {e}")
        return False
    
    return True

def check_model_sizes():
    """Check the sizes of all model files"""
    model_files = [
        'personalized_model.pkl',
        'personalized_model.pkl.gz',
        'personalized_model.pkl.ultra.gz'
    ]
    
    for file_path in model_files:
        if os.path.exists(file_path):
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"📁 {file_path}: {size_mb:.2f} MB")
            
            if size_mb > 100:
                print(f"   ⚠️  Still too large for GitHub!")
            elif size_mb > 50:
                print(f"   ⚠️  Large but manageable")
            else:
                print(f"   ✅ Good size for GitHub")

def cleanup_old_files():
    """Clean up old model files"""
    print("\n🧹 Cleaning up old files...")
    
    files_to_remove = [
        'personalized_model_backup.pkl',
        'personalized_model.pkl.gz',
        'personalized_model.pkl.ultra.gz'
    ]
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ Removed {file_path}")

if __name__ == "__main__":
    try:
        # Optimize the model
        if optimize_model():
            print("\n🎉 Model optimization completed successfully!")
            
            # Ask user if they want to clean up
            response = input("\nDo you want to clean up backup files? (y/n): ").lower()
            if response == 'y':
                cleanup_old_files()
                print("✅ Cleanup completed!")
        else:
            print("\n❌ Model optimization failed!")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
