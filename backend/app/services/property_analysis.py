import numpy as np
from PIL import Image
import io
from typing import Dict, List
from app.core.config import settings

# Optional TensorFlow import
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    tf = None


class PropertyAnalysisService:
    """Computer vision service for property analysis using ResNet50"""
    
    def __init__(self):
        self.model = self._load_model()
        self.issue_categories = [
            "water_damage",
            "roof_damage",
            "structural_issues",
            "electrical_issues",
            "plumbing_issues",
            "hvac_issues",
            "pest_damage",
            "mold",
            "foundation_issues",
            "exterior_damage"
        ]
        self.cost_estimates = {
            "water_damage": 5000,
            "roof_damage": 8000,
            "structural_issues": 15000,
            "electrical_issues": 3000,
            "plumbing_issues": 4000,
            "hvac_issues": 6000,
            "pest_damage": 2000,
            "mold": 3500,
            "foundation_issues": 12000,
            "exterior_damage": 2500
        }
    
    def _load_model(self):
        """Load pre-trained ResNet50 model"""
        if not TENSORFLOW_AVAILABLE:
            print("Warning: TensorFlow not available. Using fallback detection methods.")
            return None
        
        try:
            # Load pre-trained ResNet50
            base_model = tf.keras.applications.ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=(224, 224, 3)
            )
            
            # Add custom classification head for property issues
            x = base_model.output
            x = tf.keras.layers.GlobalAveragePooling2D()(x)
            x = tf.keras.layers.Dense(512, activation='relu')(x)
            x = tf.keras.layers.Dropout(0.5)(x)
            predictions = tf.keras.layers.Dense(len(self.issue_categories), activation='sigmoid')(x)
            
            model = tf.keras.Model(inputs=base_model.input, outputs=predictions)
            
            # For production, load trained weights here
            # model.load_weights('path/to/trained/weights.h5')
            
            return model
        except Exception as e:
            print(f"Warning: Could not load ResNet50 model: {e}")
            return None
    
    async def analyze_image(self, image_bytes: bytes) -> Dict:
        """Analyze property image for issues"""
        try:
            # Preprocess image
            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert('RGB')
            image = image.resize((224, 224))
            
            # Convert to array
            img_array = np.array(image) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            if self.model:
                # Predict issues
                predictions = self.model.predict(img_array, verbose=0)[0]
                
                # Threshold for detection (0.5)
                detected_issues = []
                total_cost = 0.0
                
                for i, category in enumerate(self.issue_categories):
                    confidence = float(predictions[i])
                    if confidence > 0.5:
                        detected_issues.append({
                            "category": category,
                            "confidence": confidence,
                            "estimated_cost": self.cost_estimates[category]
                        })
                        total_cost += self.cost_estimates[category]
            else:
                # Fallback: simple heuristic-based detection
                detected_issues = self._fallback_detection(image)
                total_cost = sum(issue["estimated_cost"] for issue in detected_issues)
            
            return {
                "issues": detected_issues,
                "estimated_cost": total_cost,
                "image_processed": True
            }
        except Exception as e:
            return {
                "issues": [],
                "estimated_cost": 0.0,
                "image_processed": False,
                "error": str(e)
            }
    
    def _fallback_detection(self, image: Image.Image) -> List[Dict]:
        """Fallback detection using simple heuristics"""
        issues = []
        
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        # Simple color-based detection (mock implementation)
        # In production, this would use more sophisticated CV techniques
        
        # Check for dark areas (potential water damage)
        dark_pixels = np.sum(img_array < 50) / img_array.size
        if dark_pixels > 0.1:
            issues.append({
                "category": "water_damage",
                "confidence": min(0.8, dark_pixels * 5),
                "estimated_cost": self.cost_estimates["water_damage"]
            })
        
        # Check for brown/red areas (potential roof issues)
        brown_mask = (img_array[:, :, 0] > 100) & (img_array[:, :, 1] < 100) & (img_array[:, :, 2] < 100)
        brown_ratio = np.sum(brown_mask) / img_array.size
        if brown_ratio > 0.15:
            issues.append({
                "category": "roof_damage",
                "confidence": min(0.7, brown_ratio * 3),
                "estimated_cost": self.cost_estimates["roof_damage"]
            })
        
        return issues

