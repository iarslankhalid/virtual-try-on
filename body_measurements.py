"""
Body Measurements Prediction Module

This module provides functionality to predict various body measurements
based on user height and weight using anthropometric formulas and statistical models.
"""

import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    UNISEX = "unisex"


@dataclass
class BodyMeasurements:
    """Data class to store all predicted body measurements"""
    # Basic inputs
    height_cm: float
    weight_kg: float
    gender: Gender
    
    # Calculated measurements
    chest_cm: float
    waist_cm: float
    hip_cm: float
    shoulder_width_cm: float
    neck_cm: float
    arm_length_cm: float
    inseam_cm: float
    thigh_cm: float
    calf_cm: float
    
    # Clothing sizes
    shirt_size: str
    pant_size: str
    dress_size: str
    shoe_size_estimate: str
    
    # Additional metrics
    bmi: float
    body_fat_percentage: float
    ideal_weight_range: Tuple[float, float]


class BodyMeasurementPredictor:
    """
    Predicts body measurements based on height, weight, and gender.
    Uses anthropometric formulas and statistical correlations.
    """
    
    def __init__(self):
        # Standard anthropometric ratios (based on research data)
        self.male_ratios = {
            'chest_to_height': 0.52,
            'waist_to_height': 0.47,
            'hip_to_height': 0.53,
            'shoulder_to_height': 0.25,
            'neck_to_height': 0.20,
            'arm_to_height': 0.44,
            'inseam_to_height': 0.47,
            'thigh_to_height': 0.32,
            'calf_to_height': 0.23
        }
        
        self.female_ratios = {
            'chest_to_height': 0.49,
            'waist_to_height': 0.42,
            'hip_to_height': 0.55,
            'shoulder_to_height': 0.23,
            'neck_to_height': 0.18,
            'arm_to_height': 0.43,
            'inseam_to_height': 0.46,
            'thigh_to_height': 0.34,
            'calf_to_height': 0.24
        }
        
        # Size conversion charts
        self.male_shirt_sizes = [
            (86, 'XS'), (91, 'S'), (97, 'M'), (102, 'L'), 
            (107, 'XL'), (112, 'XXL'), (117, 'XXXL')
        ]
        
        self.female_shirt_sizes = [
            (81, 'XS'), (86, 'S'), (91, 'M'), (97, 'L'), 
            (102, 'XL'), (107, 'XXL'), (112, 'XXXL')
        ]
        
        self.male_pant_sizes = [
            (71, '28'), (76, '30'), (81, '32'), (86, '34'), 
            (91, '36'), (97, '38'), (102, '40'), (107, '42')
        ]
        
        self.female_dress_sizes = [
            (81, '6'), (84, '8'), (89, '10'), (94, '12'), 
            (99, '14'), (104, '16'), (109, '18'), (114, '20')
        ]

    def predict_measurements(self, height_cm: float, weight_kg: float, 
                           gender: str = "unisex") -> BodyMeasurements:
        """
        Predict comprehensive body measurements from height and weight.
        
        Args:
            height_cm: Height in centimeters
            weight_kg: Weight in kilograms  
            gender: Gender ('male', 'female', or 'unisex')
            
        Returns:
            BodyMeasurements object with all predicted measurements
        """
        
        # Convert gender string to enum
        gender_enum = Gender(gender.lower()) if gender.lower() in ['male', 'female'] else Gender.UNISEX
        
        # Select appropriate ratios based on gender
        if gender_enum == Gender.MALE:
            ratios = self.male_ratios
        elif gender_enum == Gender.FEMALE:
            ratios = self.female_ratios
        else:  # UNISEX - average of male and female
            ratios = {k: (self.male_ratios[k] + self.female_ratios[k]) / 2 
                     for k in self.male_ratios.keys()}
        
        # Calculate BMI
        bmi = weight_kg / ((height_cm / 100) ** 2)
        
        # BMI adjustment factor for measurements (accounts for body composition)
        bmi_factor = self._calculate_bmi_adjustment(bmi)
        
        # Calculate basic measurements using anthropometric ratios
        chest_cm = height_cm * ratios['chest_to_height'] * bmi_factor
        waist_cm = height_cm * ratios['waist_to_height'] * bmi_factor
        hip_cm = height_cm * ratios['hip_to_height'] * bmi_factor
        shoulder_width_cm = height_cm * ratios['shoulder_to_height']
        neck_cm = height_cm * ratios['neck_to_height'] * (bmi_factor * 0.8 + 0.2)
        arm_length_cm = height_cm * ratios['arm_to_height']
        inseam_cm = height_cm * ratios['inseam_to_height']
        thigh_cm = height_cm * ratios['thigh_to_height'] * bmi_factor
        calf_cm = height_cm * ratios['calf_to_height'] * bmi_factor
        
        # Determine clothing sizes
        shirt_size = self._determine_shirt_size(chest_cm, gender_enum)
        pant_size = self._determine_pant_size(waist_cm, gender_enum)
        dress_size = self._determine_dress_size(chest_cm, gender_enum)
        shoe_size_estimate = self._estimate_shoe_size(height_cm, gender_enum)
        
        # Calculate body fat percentage (rough estimate)
        body_fat_percentage = self._estimate_body_fat(bmi, gender_enum)
        
        # Calculate ideal weight range
        ideal_weight_range = self._calculate_ideal_weight_range(height_cm)
        
        return BodyMeasurements(
            height_cm=height_cm,
            weight_kg=weight_kg,
            gender=gender_enum,
            chest_cm=round(chest_cm, 1),
            waist_cm=round(waist_cm, 1),
            hip_cm=round(hip_cm, 1),
            shoulder_width_cm=round(shoulder_width_cm, 1),
            neck_cm=round(neck_cm, 1),
            arm_length_cm=round(arm_length_cm, 1),
            inseam_cm=round(inseam_cm, 1),
            thigh_cm=round(thigh_cm, 1),
            calf_cm=round(calf_cm, 1),
            shirt_size=shirt_size,
            pant_size=pant_size,
            dress_size=dress_size,
            shoe_size_estimate=shoe_size_estimate,
            bmi=round(bmi, 1),
            body_fat_percentage=round(body_fat_percentage, 1),
            ideal_weight_range=ideal_weight_range
        )
    
    def _calculate_bmi_adjustment(self, bmi: float) -> float:
        """
        Calculate adjustment factor based on BMI.
        Accounts for the fact that measurements scale with body composition.
        """
        # Normal BMI range is 18.5-24.9
        if bmi < 18.5:
            # Underweight - slightly smaller measurements
            return 0.85 + (bmi - 15) * 0.04
        elif bmi <= 24.9:
            # Normal weight - standard measurements
            return 0.95 + (bmi - 18.5) * 0.015
        elif bmi <= 29.9:
            # Overweight - larger measurements
            return 1.05 + (bmi - 25) * 0.02
        else:
            # Obese - significantly larger measurements
            return 1.15 + min((bmi - 30) * 0.025, 0.3)
    
    def _determine_shirt_size(self, chest_cm: float, gender: Gender) -> str:
        """Determine shirt size based on chest measurement"""
        sizes = self.male_shirt_sizes if gender == Gender.MALE else self.female_shirt_sizes
        
        for measurement, size in sizes:
            if chest_cm <= measurement:
                return size
        return sizes[-1][1]  # Return largest size if over maximum
    
    def _determine_pant_size(self, waist_cm: float, gender: Gender) -> str:
        """Determine pant size based on waist measurement"""
        if gender == Gender.FEMALE:
            # For women, use dress sizes as pant sizes often correspond
            for measurement, size in self.female_dress_sizes:
                if waist_cm <= measurement:
                    return f"Size {size}"
            return f"Size {self.female_dress_sizes[-1][1]}"
        else:
            # For men, use traditional inch-based sizing
            for measurement, size in self.male_pant_sizes:
                if waist_cm <= measurement:
                    return size
            return self.male_pant_sizes[-1][1]
    
    def _determine_dress_size(self, chest_cm: float, gender: Gender) -> str:
        """Determine dress size based on chest/bust measurement"""
        if gender == Gender.MALE:
            return "N/A"
        
        for measurement, size in self.female_dress_sizes:
            if chest_cm <= measurement:
                return size
        return self.female_dress_sizes[-1][1]
    
    def _estimate_shoe_size(self, height_cm: float, gender: Gender) -> str:
        """Estimate shoe size based on height (rough approximation)"""
        # Foot length is approximately 15% of height
        foot_length_cm = height_cm * 0.15
        
        if gender == Gender.MALE:
            # Men's US shoe size approximation
            us_size = (foot_length_cm - 22) / 0.847
            return f"US {max(6, min(15, round(us_size)))} (approx)"
        else:
            # Women's US shoe size approximation
            us_size = (foot_length_cm - 21) / 0.847
            return f"US {max(5, min(12, round(us_size)))} (approx)"
    
    def _estimate_body_fat(self, bmi: float, gender: Gender) -> float:
        """Estimate body fat percentage based on BMI and gender"""
        if gender == Gender.MALE:
            # Deurenberg formula for men
            body_fat = (1.20 * bmi) + (0.23 * 30) - 16.2  # Assuming average age of 30
        else:
            # Deurenberg formula for women  
            body_fat = (1.20 * bmi) + (0.23 * 30) - 5.4   # Assuming average age of 30
        
        return max(3, min(50, body_fat))  # Clamp to reasonable range
    
    def _calculate_ideal_weight_range(self, height_cm: float) -> Tuple[float, float]:
        """Calculate ideal weight range based on BMI 18.5-24.9"""
        height_m = height_cm / 100
        min_weight = 18.5 * (height_m ** 2)
        max_weight = 24.9 * (height_m ** 2)
        return (round(min_weight, 1), round(max_weight, 1))


def get_size_recommendations(measurements: BodyMeasurements) -> Dict[str, str]:
    """
    Get clothing size recommendations based on measurements.
    
    Args:
        measurements: BodyMeasurements object
        
    Returns:
        Dictionary with clothing recommendations
    """
    recommendations = {
        "shirt_size": measurements.shirt_size,
        "pant_size": measurements.pant_size,
        "dress_size": measurements.dress_size,
        "shoe_size": measurements.shoe_size_estimate,
        "chest_measurement": f"{measurements.chest_cm} cm",
        "waist_measurement": f"{measurements.waist_cm} cm",
        "hip_measurement": f"{measurements.hip_cm} cm",
        "bmi_category": _get_bmi_category(measurements.bmi),
        "ideal_weight": f"{measurements.ideal_weight_range[0]}-{measurements.ideal_weight_range[1]} kg"
    }
    
    return recommendations


def _get_bmi_category(bmi: float) -> str:
    """Get BMI category description"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# Example usage and testing
if __name__ == "__main__":
    predictor = BodyMeasurementPredictor()
    
    # Test with example data
    test_cases = [
        (175, 70, "male"),    # Average male
        (165, 60, "female"),  # Average female
        (180, 80, "male"),    # Taller, heavier male
        (160, 55, "female"),  # Smaller female
    ]
    
    for height, weight, gender in test_cases:
        measurements = predictor.predict_measurements(height, weight, gender)
        recommendations = get_size_recommendations(measurements)
        
        print(f"\n{gender.title()} - {height}cm, {weight}kg:")
        print(f"  BMI: {measurements.bmi} ({recommendations['bmi_category']})")
        print(f"  Chest: {measurements.chest_cm}cm")
        print(f"  Waist: {measurements.waist_cm}cm") 
        print(f"  Hip: {measurements.hip_cm}cm")
        print(f"  Shirt Size: {measurements.shirt_size}")
        print(f"  Pant Size: {measurements.pant_size}")
        print(f"  Dress Size: {measurements.dress_size}")
        print(f"  Shoe Size: {measurements.shoe_size_estimate}")
