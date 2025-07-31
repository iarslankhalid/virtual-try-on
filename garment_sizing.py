"""
Garment Sizing and Virtual Try-On Module

This module handles garment sizing logic, fit analysis, and virtual try-on visualization.
It works with the body measurements module to provide accurate sizing recommendations
and simulate how different sizes would look on a person.
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64
import io


class GarmentSize(Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class FitType(Enum):
    TIGHT = "tight"
    PERFECT = "perfect"
    LOOSE = "loose"


@dataclass
class GarmentMeasurements:
    """Standard measurements for different garment sizes"""
    size: GarmentSize
    chest_cm: float
    length_cm: float
    shoulder_width_cm: float
    sleeve_length_cm: float
    
    
@dataclass
class FitAnalysis:
    """Analysis of how a garment fits on a person"""
    recommended_size: GarmentSize
    selected_size: GarmentSize
    fit_type: FitType
    chest_difference_cm: float
    length_difference_cm: float
    fit_score: float  # 0-100, where 100 is perfect fit
    fit_description: str


class GarmentSizingSystem:
    """
    Handles garment sizing, fit analysis, and virtual try-on visualization
    """
    
    def __init__(self):
        # Standard shirt measurements (in cm) for different sizes
        self.shirt_measurements = {
            GarmentSize.XS: GarmentMeasurements(GarmentSize.XS, 86, 66, 42, 59),
            GarmentSize.S: GarmentMeasurements(GarmentSize.S, 91, 68, 44, 61),
            GarmentSize.M: GarmentMeasurements(GarmentSize.M, 97, 70, 46, 63),
            GarmentSize.L: GarmentMeasurements(GarmentSize.L, 102, 72, 48, 65),
            GarmentSize.XL: GarmentMeasurements(GarmentSize.XL, 107, 74, 50, 67),
            GarmentSize.XXL: GarmentMeasurements(GarmentSize.XXL, 112, 76, 52, 69),
        }
        
        # Fit tolerance ranges (in cm)
        self.fit_tolerance = {
            'perfect_range': 2.0,  # +/- 2cm is perfect fit
            'loose_threshold': 8.0,  # More than 8cm larger is loose
            'tight_threshold': -3.0,  # More than 3cm smaller is tight
        }
    
    def get_recommended_size(self, chest_measurement: float, gender: str = "unisex") -> GarmentSize:
        """
        Get recommended garment size based on chest measurement
        
        Args:
            chest_measurement: Person's chest measurement in cm
            gender: Person's gender (affects sizing slightly)
        
        Returns:
            Recommended GarmentSize
        """
        # Adjust for gender-specific fit preferences
        target_chest = chest_measurement
        if gender.lower() == "female":
            target_chest += 2  # Slightly more room for comfort
        elif gender.lower() == "male":
            target_chest += 4  # More room for typical male fit preference
        else:
            target_chest += 3  # Unisex default
        
        # Find closest size
        best_size = GarmentSize.M
        min_difference = float('inf')
        
        for size, measurements in self.shirt_measurements.items():
            difference = abs(measurements.chest_cm - target_chest)
            if difference < min_difference:
                min_difference = difference
                best_size = size
        
        return best_size
    
    def analyze_fit(self, person_chest: float, person_height: float, 
                   selected_size: GarmentSize, gender: str = "unisex") -> FitAnalysis:
        """
        Analyze how a selected garment size fits a person
        
        Args:
            person_chest: Person's chest measurement in cm
            person_height: Person's height in cm
            selected_size: The garment size to analyze
            gender: Person's gender
        
        Returns:
            FitAnalysis object with detailed fit information
        """
        recommended_size = self.get_recommended_size(person_chest, gender)
        garment_measurements = self.shirt_measurements[selected_size]
        
        # Calculate differences
        chest_difference = garment_measurements.chest_cm - person_chest
        length_difference = garment_measurements.length_cm - (person_height * 0.40)  # Typical shirt length ratio
        
        # Determine fit type
        if chest_difference <= self.fit_tolerance['tight_threshold']:
            fit_type = FitType.TIGHT
            fit_description = "This size will be tight and may restrict movement"
        elif chest_difference >= self.fit_tolerance['loose_threshold']:
            fit_type = FitType.LOOSE
            fit_description = "This size will be loose and may look oversized"
        elif abs(chest_difference) <= self.fit_tolerance['perfect_range']:
            fit_type = FitType.PERFECT
            fit_description = "This size provides an excellent fit"
        elif chest_difference > 0:
            fit_type = FitType.LOOSE
            fit_description = "This size will be somewhat loose but comfortable"
        else:
            fit_type = FitType.TIGHT
            fit_description = "This size will be somewhat snug but wearable"
        
        # Calculate fit score (0-100)
        chest_penalty = min(abs(chest_difference) * 10, 50)  # Max 50 point penalty for chest fit
        length_penalty = min(abs(length_difference) * 5, 20)  # Max 20 point penalty for length
        fit_score = max(0, 100 - chest_penalty - length_penalty)
        
        return FitAnalysis(
            recommended_size=recommended_size,
            selected_size=selected_size,
            fit_type=fit_type,
            chest_difference_cm=chest_difference,
            length_difference_cm=length_difference,
            fit_score=fit_score,
            fit_description=fit_description
        )
    
    def get_available_sizes(self) -> List[GarmentSize]:
        """Get list of available garment sizes"""
        return list(self.shirt_measurements.keys())
    
    def get_size_comparison_data(self, person_chest: float, person_height: float, 
                               gender: str = "unisex") -> Dict[str, Any]:
        """
        Get comparison data for all available sizes
        
        Args:
            person_chest: Person's chest measurement in cm
            person_height: Person's height in cm
            gender: Person's gender
        
        Returns:
            Dictionary with size comparison data
        """
        recommended_size = self.get_recommended_size(person_chest, gender)
        size_data = {}
        
        for size in self.get_available_sizes():
            analysis = self.analyze_fit(person_chest, person_height, size, gender)
            measurements = self.shirt_measurements[size]
            
            size_data[size.value] = {
                'is_recommended': size == recommended_size,
                'fit_type': analysis.fit_type.value,
                'fit_score': analysis.fit_score,
                'fit_description': analysis.fit_description,
                'chest_difference': analysis.chest_difference_cm,
                'length_difference': analysis.length_difference_cm,
                'measurements': {
                    'chest': measurements.chest_cm,
                    'length': measurements.length_cm,
                    'shoulder_width': measurements.shoulder_width_cm,
                    'sleeve_length': measurements.sleeve_length_cm
                }
            }
        
        return {
            'recommended_size': recommended_size.value,
            'person_measurements': {
                'chest': person_chest,
                'height': person_height
            },
            'size_analysis': size_data
        }


class VirtualTryOnVisualizer:
    """
    Handles visual representation of how different garment sizes would look
    """
    
    def __init__(self):
        self.sizing_system = GarmentSizingSystem()
    
    def apply_garment_overlay(self, person_image: np.ndarray, garment_image: np.ndarray, 
                            fit_analysis: FitAnalysis, pose_landmarks: Optional[List] = None) -> np.ndarray:
        """
        Apply garment overlay to person image based on fit analysis with realistic size visualization
        
        Args:
            person_image: Person's image as numpy array
            garment_image: Garment image as numpy array
            fit_analysis: FitAnalysis object
            pose_landmarks: Optional pose landmarks for better positioning
        
        Returns:
            Combined image with garment overlay showing realistic size differences
        """
        # Get image dimensions
        person_h, person_w = person_image.shape[:2]
        garment_h, garment_w = garment_image.shape[:2]
        
        # Calculate realistic scaling and positioning based on actual size differences
        chest_diff = fit_analysis.chest_difference_cm
        
        # More realistic scaling based on actual measurements
        if fit_analysis.fit_type == FitType.TIGHT:
            # For tight fit: garment appears stretched and compressed
            scale_factor = 0.75 + (chest_diff / 20.0)  # More dramatic for very tight
            alpha = 0.95  # Very opaque to show stretched material
            width_adjustment = 0.9  # Slightly narrower to show compression
            height_adjustment = 1.05  # Slightly taller due to stretching
        elif fit_analysis.fit_type == FitType.LOOSE:
            # For loose fit: garment appears billowy and oversized
            scale_factor = 1.0 + (chest_diff / 15.0)  # Proportional to looseness
            alpha = 0.65  # More transparent to show flowing fabric
            width_adjustment = 1.2  # Wider to show bagginess
            height_adjustment = 1.1   # Longer due to draping
        else:  # Perfect fit
            scale_factor = 1.0
            alpha = 0.8
            width_adjustment = 1.0
            height_adjustment = 1.0
        
        # Apply realistic size adjustments
        new_garment_w = int(garment_w * scale_factor * width_adjustment)
        new_garment_h = int(garment_h * scale_factor * height_adjustment)
        
        # Create the resized garment with appropriate distortion for fit type
        if fit_analysis.fit_type == FitType.TIGHT:
            # For tight fit: compress and stretch the garment
            resized_garment = cv2.resize(garment_image, (new_garment_w, new_garment_h))
            # Add slight horizontal compression effect
            kernel = np.array([[-0.1, -0.1, -0.1],
                              [-0.1,  1.8, -0.1],
                              [-0.1, -0.1, -0.1]])
            resized_garment = cv2.filter2D(resized_garment, -1, kernel)
            
        elif fit_analysis.fit_type == FitType.LOOSE:
            # For loose fit: create a more flowing, draped appearance
            resized_garment = cv2.resize(garment_image, (new_garment_w, new_garment_h))
            # Add slight blur to simulate fabric movement
            resized_garment = cv2.GaussianBlur(resized_garment, (3, 3), 0.5)
            
        else:  # Perfect fit
            resized_garment = cv2.resize(garment_image, (new_garment_w, new_garment_h))
        
        # Position garment on person with size-specific adjustments
        if pose_landmarks and len(pose_landmarks) > 11:  # Check if shoulder landmarks exist
            # Use shoulder landmarks for positioning
            left_shoulder_x = int(pose_landmarks[11]['x'])
            right_shoulder_x = int(pose_landmarks[12]['x'])
            shoulder_y = int((pose_landmarks[11]['y'] + pose_landmarks[12]['y']) / 2)
            
            center_x = (left_shoulder_x + right_shoulder_x) // 2
            
            # Adjust starting position based on fit type
            if fit_analysis.fit_type == FitType.TIGHT:
                start_y = shoulder_y - 10  # Higher placement for tight fit
            elif fit_analysis.fit_type == FitType.LOOSE:
                start_y = shoulder_y - 30  # Lower placement for loose, draped fit
            else:
                start_y = shoulder_y - 20  # Normal placement
        else:
            # Default positioning with fit adjustments
            center_x = person_w // 2
            if fit_analysis.fit_type == FitType.TIGHT:
                start_y = person_h // 4 + 20  # Slightly lower for tight
            elif fit_analysis.fit_type == FitType.LOOSE:
                start_y = person_h // 4 - 20  # Higher for loose draping
            else:
                start_y = person_h // 4
        
        start_x = center_x - new_garment_w // 2
        
        # Ensure garment fits within image bounds
        start_x = max(0, min(start_x, person_w - new_garment_w))
        start_y = max(0, min(start_y, person_h - new_garment_h))
        end_x = min(start_x + new_garment_w, person_w)
        end_y = min(start_y + new_garment_h, person_h)
        
        # Adjust garment size if it doesn't fit
        actual_w = end_x - start_x
        actual_h = end_y - start_y
        if actual_w != new_garment_w or actual_h != new_garment_h:
            resized_garment = cv2.resize(resized_garment, (actual_w, actual_h))
        
        # Create result image with fit-specific blending
        result = person_image.copy()
        
        # Apply size-specific visual effects
        if fit_analysis.fit_type == FitType.TIGHT:
            # For tight fit: use additive blending to show tension
            garment_area = result[start_y:end_y, start_x:end_x]
            # Create tension effect by brightening edges
            edges = cv2.Canny(resized_garment, 50, 150)
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            edges_colored = edges_colored * 0.3  # Subtle edge highlighting
            
            blended = cv2.addWeighted(garment_area, 1-alpha, resized_garment, alpha, 0)
            blended = cv2.add(blended, edges_colored.astype(np.uint8))
            result[start_y:end_y, start_x:end_x] = blended
            
        elif fit_analysis.fit_type == FitType.LOOSE:
            # For loose fit: create shadow/draping effect
            garment_area = result[start_y:end_y, start_x:end_x]
            
            # Create shadow effect for loose clothing
            shadow = resized_garment.copy()
            shadow = cv2.GaussianBlur(shadow, (5, 5), 2)
            shadow = (shadow * 0.3).astype(np.uint8)  # Darker shadow
            
            # Apply shadow first (behind the garment)
            shadow_blended = cv2.addWeighted(garment_area, 0.9, shadow, 0.1, 0)
            # Then apply the main garment
            blended = cv2.addWeighted(shadow_blended, 1-alpha, resized_garment, alpha, 0)
            result[start_y:end_y, start_x:end_x] = blended
            
        else:  # Perfect fit - normal blending
            garment_area = result[start_y:end_y, start_x:end_x]
            blended = cv2.addWeighted(garment_area, 1-alpha, resized_garment, alpha, 0)
            result[start_y:end_y, start_x:end_x] = blended
        
        # Add fit indicator text
        self._add_fit_indicator(result, fit_analysis)
        
        return result
    
    def _add_fit_indicator(self, image: np.ndarray, fit_analysis: FitAnalysis):
        """Add visual indicators showing fit type"""
        height, width = image.shape[:2]
        
        # Choose color based on fit type
        if fit_analysis.fit_type == FitType.PERFECT:
            color = (0, 255, 0)  # Green
            text = f"Perfect Fit (Score: {fit_analysis.fit_score:.0f})"
        elif fit_analysis.fit_type == FitType.TIGHT:
            color = (0, 0, 255)  # Red
            text = f"Tight Fit (Score: {fit_analysis.fit_score:.0f})"
        else:  # Loose
            color = (0, 165, 255)  # Orange
            text = f"Loose Fit (Score: {fit_analysis.fit_score:.0f})"
        
        # Add text overlay
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        
        # Get text size
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Position text at top-left
        x = 10
        y = 30
        
        # Add background rectangle for better readability
        cv2.rectangle(image, (x-5, y-text_height-5), (x+text_width+5, y+5), (0, 0, 0), -1)
        
        # Add text
        cv2.putText(image, text, (x, y), font, font_scale, color, thickness)
        
        # Add size information
        size_text = f"Size: {fit_analysis.selected_size.value} (Recommended: {fit_analysis.recommended_size.value})"
        cv2.putText(image, size_text, (x, y+30), font, 0.6, (255, 255, 255), 2)
    
    def create_size_comparison_grid(self, person_image: np.ndarray, garment_image: np.ndarray,
                                  person_chest: float, person_height: float, 
                                  gender: str = "unisex", pose_landmarks: Optional[List] = None) -> np.ndarray:
        """
        Create a grid showing how different sizes would look
        
        Args:
            person_image: Person's image
            garment_image: Garment image
            person_chest: Person's chest measurement
            person_height: Person's height
            gender: Person's gender
            pose_landmarks: Optional pose landmarks
        
        Returns:
            Grid image showing different size fits
        """
        sizes_to_show = [GarmentSize.S, GarmentSize.M, GarmentSize.L]
        images = []
        
        for size in sizes_to_show:
            fit_analysis = self.sizing_system.analyze_fit(person_chest, person_height, size, gender)
            try_on_result = self.apply_garment_overlay(person_image, garment_image, fit_analysis, pose_landmarks)
            images.append(try_on_result)
        
        # Resize images to same size for grid
        target_height = 400
        target_width = 300
        resized_images = []
        
        for img in images:
            resized = cv2.resize(img, (target_width, target_height))
            resized_images.append(resized)
        
        # Create horizontal grid
        grid = np.hstack(resized_images)
        
        return grid


def process_virtual_tryon_with_sizing(person_image_path: str, garment_image_path: str,
                                    person_chest: float, person_height: float,
                                    selected_size: str = "M", gender: str = "unisex",
                                    pose_landmarks: Optional[List] = None) -> Dict[str, Any]:
    """
    Main function to process virtual try-on with sizing analysis
    
    Args:
        person_image_path: Path to person's image
        garment_image_path: Path to garment image
        person_chest: Person's chest measurement in cm
        person_height: Person's height in cm
        selected_size: Selected garment size
        gender: Person's gender
        pose_landmarks: Optional pose landmarks
    
    Returns:
        Dictionary with try-on results and sizing analysis
    """
    # Initialize systems
    sizing_system = GarmentSizingSystem()
    visualizer = VirtualTryOnVisualizer()
    
    # Load images
    person_image = cv2.imread(person_image_path)
    garment_image = cv2.imread(garment_image_path)
    
    if person_image is None or garment_image is None:
        raise ValueError("Could not load one or both images")
    
    # Convert size string to enum
    try:
        size_enum = GarmentSize(selected_size.upper())
    except ValueError:
        size_enum = GarmentSize.M  # Default fallback
    
    # Analyze fit
    fit_analysis = sizing_system.analyze_fit(person_chest, person_height, size_enum, gender)
    
    # Create try-on visualization
    try_on_result = visualizer.apply_garment_overlay(person_image, garment_image, fit_analysis, pose_landmarks)
    
    # Create size comparison grid
    comparison_grid = visualizer.create_size_comparison_grid(
        person_image, garment_image, person_chest, person_height, gender, pose_landmarks
    )
    
    # Get size comparison data
    size_data = sizing_system.get_size_comparison_data(person_chest, person_height, gender)
    
    # Convert images to base64 for web display
    def image_to_base64(img):
        _, buffer = cv2.imencode('.jpg', img)
        img_str = base64.b64encode(buffer).decode()
        return f"data:image/jpeg;base64,{img_str}"
    
    return {
        'success': True,
        'try_on_result': image_to_base64(try_on_result),
        'comparison_grid': image_to_base64(comparison_grid),
        'fit_analysis': {
            'selected_size': fit_analysis.selected_size.value,
            'recommended_size': fit_analysis.recommended_size.value,
            'fit_type': fit_analysis.fit_type.value,
            'fit_score': fit_analysis.fit_score,
            'fit_description': fit_analysis.fit_description,
            'chest_difference': fit_analysis.chest_difference_cm,
            'length_difference': fit_analysis.length_difference_cm
        },
        'size_data': size_data
    }
