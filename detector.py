import joblib
import numpy as np
import os

class RansomwareDetector:
    def __init__(self, model_path='model/ransomware_model.pkl', threshold=0.7):
        self.model = self.load_model(model_path)
        self.threshold = threshold
    
    def load_model(self, model_path):
        """Load the trained ransomware detection model"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        return joblib.load(model_path)
    
    def predict(self, feature_vector):
        """
        Predict ransomware probability from feature vector
        
        Args:
            feature_vector: List or array of features [file_rate, extension_count, 
                          avg_cpu, avg_memory, avg_disk_read, avg_disk_write, 
                          suspicious_count, file_ratio, max_extension_count, temp_files]
        
        Returns:
            float: Threat score between 0 and 1
        """
        features = np.array(feature_vector).reshape(1, -1)
        probability = self.model.predict_proba(features)[0][1]
        return probability
    
    def detect_threat(self, feature_vector):
        """
        Detect ransomware threat with threshold logic
        
        Args:
            feature_vector: List or array of features
            
        Returns:
            dict: Detection result with threat score and alert status
        """
        threat_score = self.predict(feature_vector)
        
        return {
            'threat_score': threat_score,
            'is_threat': threat_score >= self.threshold,
            'alert_level': self.get_alert_level(threat_score)
        }
    
    def get_alert_level(self, score):
        """Get alert level based on threat score"""
        if score >= 0.8:
            return 'HIGH'
        elif score >= 0.5:
            return 'MEDIUM'
        elif score >= 0.3:
            return 'LOW'
        return 'NORMAL'

# Example usage
if __name__ == "__main__":
    detector = RansomwareDetector()
    
    # Example feature vector (high ransomware activity)
    test_features = [150, 5, 85, 70, 1000, 2000, 25, 0.8, 10, 50]
    
    result = detector.detect_threat(test_features)
    print(f"Threat Score: {result['threat_score']:.3f}")
    print(f"Is Threat: {result['is_threat']}")
    print(f"Alert Level: {result['alert_level']}")