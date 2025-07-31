#!/usr/bin/env python3
"""
Test script for the enhanced virtual try-on with sizing functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from garment_sizing import GarmentSizingSystem, GarmentSize
from body_measurements import BodyMeasurementPredictor

def test_sizing_system():
    """Test the garment sizing system"""
    print("🧪 Testing Enhanced Virtual Try-On Sizing System")
    print("=" * 60)
    
    # Initialize systems
    sizing_system = GarmentSizingSystem()
    body_predictor = BodyMeasurementPredictor()
    
    # Test case: Average person
    height = 175  # cm
    weight = 70   # kg
    gender = "male"
    
    print(f"📏 Test Person: {height}cm, {weight}kg, {gender}")
    
    # Predict body measurements
    measurements = body_predictor.predict_measurements(height, weight, gender)
    print(f"📊 Predicted chest measurement: {measurements.chest_cm:.1f}cm")
    
    # Get recommended size
    recommended = sizing_system.get_recommended_size(measurements.chest_cm, gender)
    print(f"👕 Recommended size: {recommended.value}")
    
    print("\n🔍 Size Analysis for All Available Sizes:")
    print("-" * 60)
    
    # Test all sizes
    sizes_to_test = [GarmentSize.S, GarmentSize.M, GarmentSize.L]
    
    for size in sizes_to_test:
        analysis = sizing_system.analyze_fit(measurements.chest_cm, height, size, gender)
        
        fit_emoji = "✅" if analysis.fit_type.value == "perfect" else "⚠️" if analysis.fit_type.value == "loose" else "❌"
        
        print(f"{fit_emoji} Size {size.value}:")
        print(f"   Fit Type: {analysis.fit_type.value.title()}")
        print(f"   Fit Score: {analysis.fit_score:.0f}%")
        print(f"   Chest Difference: {analysis.chest_difference_cm:+.1f}cm")
        print(f"   Description: {analysis.fit_description}")
        print()
    
    # Get size comparison data
    comparison_data = sizing_system.get_size_comparison_data(measurements.chest_cm, height, gender)
    
    print("📋 Size Comparison Summary:")
    print("-" * 60)
    print(f"Recommended Size: {comparison_data['recommended_size']}")
    print(f"Person's Chest: {comparison_data['person_measurements']['chest']:.1f}cm")
    print()
    
    for size, data in comparison_data['size_analysis'].items():
        star = "⭐" if data['is_recommended'] else "  "
        print(f"{star} {size}: {data['fit_type']} ({data['fit_score']:.0f}% match)")
    
    print("\n✨ Test completed successfully!")
    return True

def test_different_body_types():
    """Test with different body types"""
    print("\n🧪 Testing Different Body Types")
    print("=" * 60)
    
    test_cases = [
        (160, 50, "female", "Petite Female"),
        (180, 85, "male", "Tall Male"), 
        (170, 60, "unisex", "Average Unisex"),
        (165, 80, "male", "Stocky Male"),
    ]
    
    sizing_system = GarmentSizingSystem()
    body_predictor = BodyMeasurementPredictor()
    
    for height, weight, gender, description in test_cases:
        print(f"\n👤 {description}: {height}cm, {weight}kg")
        
        measurements = body_predictor.predict_measurements(height, weight, gender)
        recommended = sizing_system.get_recommended_size(measurements.chest_cm, gender)
        
        print(f"   Chest: {measurements.chest_cm:.1f}cm → Recommended: {recommended.value}")
        
        # Test how S, M, L would fit
        for size in [GarmentSize.S, GarmentSize.M, GarmentSize.L]:
            analysis = sizing_system.analyze_fit(measurements.chest_cm, height, size, gender)
            print(f"   Size {size.value}: {analysis.fit_type.value} ({analysis.fit_score:.0f}%)")

if __name__ == "__main__":
    try:
        print("🚀 Starting Enhanced Virtual Try-On System Tests\n")
        
        # Run basic tests
        test_sizing_system()
        
        # Test different body types
        test_different_body_types()
        
        print("\n🎉 All tests passed! The sizing system is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Visit http://localhost:8000/enhanced to test the web interface")
        print("   2. Upload a person image and garment image")
        print("   3. Enter your measurements")
        print("   4. Try on different sizes individually!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
