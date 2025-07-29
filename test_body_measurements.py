#!/usr/bin/env python3
"""
Test script for body measurements prediction functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from body_measurements import BodyMeasurementPredictor, get_size_recommendations

def test_body_measurements():
    """Test the body measurements prediction functionality"""
    
    print("🧪 Testing Body Measurements Prediction")
    print("=" * 50)
    
    predictor = BodyMeasurementPredictor()
    
    # Test cases with different body types
    test_cases = [
        {
            "name": "Average Male",
            "height": 175,
            "weight": 70,
            "gender": "male"
        },
        {
            "name": "Average Female", 
            "height": 165,
            "weight": 60,
            "gender": "female"
        },
        {
            "name": "Tall Male",
            "height": 190,
            "weight": 85,
            "gender": "male"
        },
        {
            "name": "Petite Female",
            "height": 155,
            "weight": 50,
            "gender": "female"
        },
        {
            "name": "Unisex/Unknown",
            "height": 170,
            "weight": 65,
            "gender": "unisex"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📏 Testing: {test_case['name']}")
        print(f"   Input: {test_case['height']}cm, {test_case['weight']}kg, {test_case['gender']}")
        
        try:
            # Predict measurements
            measurements = predictor.predict_measurements(
                test_case['height'], 
                test_case['weight'], 
                test_case['gender']
            )
            
            # Get size recommendations
            recommendations = get_size_recommendations(measurements)
            
            # Display results
            print(f"   BMI: {measurements.bmi} ({recommendations['bmi_category']})")
            print(f"   Chest: {measurements.chest_cm}cm")
            print(f"   Waist: {measurements.waist_cm}cm")
            print(f"   Hip: {measurements.hip_cm}cm")
            print(f"   Shirt Size: {recommendations['shirt_size']}")
            print(f"   Pant Size: {recommendations['pant_size']}")
            print(f"   Dress Size: {recommendations['dress_size']}")
            print(f"   Shoe Size: {recommendations['shoe_size']}")
            print(f"   Body Fat: {measurements.body_fat_percentage}%")
            print(f"   Ideal Weight Range: {recommendations['ideal_weight']}")
            print("   ✅ Test passed")
            
        except Exception as e:
            print(f"   ❌ Test failed: {str(e)}")
    
    print("\n🔍 Testing Edge Cases")
    print("-" * 30)
    
    # Test edge cases
    edge_cases = [
        {"height": 120, "weight": 30, "gender": "female", "description": "Minimum values"},
        {"height": 250, "weight": 300, "gender": "male", "description": "Maximum values"},
        {"height": 180, "weight": 60, "gender": "male", "description": "Underweight"},
        {"height": 160, "weight": 90, "gender": "female", "description": "Overweight"}
    ]
    
    for case in edge_cases:
        print(f"\n📐 Testing: {case['description']}")
        print(f"   Input: {case['height']}cm, {case['weight']}kg, {case['gender']}")
        
        try:
            measurements = predictor.predict_measurements(
                case['height'], 
                case['weight'], 
                case['gender']
            )
            
            print(f"   BMI: {measurements.bmi}")
            print(f"   Chest: {measurements.chest_cm}cm")
            print(f"   Waist: {measurements.waist_cm}cm")
            print("   ✅ Edge case handled")
            
        except Exception as e:
            print(f"   ❌ Edge case failed: {str(e)}")
    
    print("\n🎉 Body Measurements Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_body_measurements()
