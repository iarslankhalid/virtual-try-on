#!/usr/bin/env python3
"""
Test script for body measurements functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from body_measurements import BodyMeasurementPredictor, get_size_recommendations

def test_body_measurements():
    """Test the body measurements prediction functionality"""
    print("🧪 Testing Body Measurements Prediction")
    print("=" * 50)
    
    try:
        # Initialize predictor
        predictor = BodyMeasurementPredictor()
        print("✅ Predictor initialized successfully")
        
        # Test cases
        test_cases = [
            (175, 70, "male", "Average male"),
            (165, 60, "female", "Average female"),
            (180, 85, "unisex", "Taller person"),
            (160, 55, "female", "Smaller female"),
        ]
        
        for height, weight, gender, description in test_cases:
            print(f"\n🧑‍⚕️ Testing: {description} ({height}cm, {weight}kg, {gender})")
            print("-" * 40)
            
            # Predict measurements
            measurements = predictor.predict_measurements(height, weight, gender)
            recommendations = get_size_recommendations(measurements)
            
            # Display results
            print(f"BMI: {measurements.bmi} ({recommendations['bmi_category']})")
            print(f"Chest: {measurements.chest_cm}cm")
            print(f"Waist: {measurements.waist_cm}cm")
            print(f"Hip: {measurements.hip_cm}cm")
            print(f"Shirt Size: {measurements.shirt_size}")
            print(f"Pant Size: {measurements.pant_size}")
            print(f"Dress Size: {measurements.dress_size}")
            print(f"Shoe Size: {measurements.shoe_size_estimate}")
            print(f"Body Fat: {measurements.body_fat_percentage}%")
            print(f"Ideal Weight: {recommendations['ideal_weight']}")
            
        print(f"\n🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_body_measurements()
    sys.exit(0 if success else 1)
