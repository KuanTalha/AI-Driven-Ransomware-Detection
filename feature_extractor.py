import numpy as np
from collections import deque
from sklearn.preprocessing import MinMaxScaler
import time

class FeatureExtractor:
    """Extracts and normalizes features from system monitoring data for ML models"""
    
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.data_history = deque(maxlen=window_size)
        self.scaler = MinMaxScaler()
        self.is_fitted = False
        
        # Feature ranges for normalization (will be updated dynamically)
        self.feature_ranges = {
            'file_mod_rate': [0, 100],
            'process_creation_rate': [0, 50], 
            'cpu_spike_pct': [0, 100],
            'disk_write_freq': [0, 1000000]  # bytes per second
        }
    
    def add_data(self, monitoring_data):
        """Add new monitoring data to history window"""
        self.data_history.append(monitoring_data)
    
    def extract_features(self):
        """Extract features from current data window"""
        if len(self.data_history) < 2:
            return None
        
        # Calculate time-based rates
        time_span = self.data_history[-1]['timestamp'] - self.data_history[0]['timestamp']
        if time_span == 0:
            return None
        
        # File modification rate (files created + deleted + renamed per second)
        total_file_ops = sum(
            data['file_operations']['created'] + 
            data['file_operations']['deleted'] + 
            data['file_operations']['renamed']
            for data in self.data_history
        )
        file_mod_rate = total_file_ops / time_span
        
        # Process creation rate (change in process count per second)
        process_counts = [data['process_count'] for data in self.data_history]
        process_changes = sum(abs(process_counts[i] - process_counts[i-1]) 
                            for i in range(1, len(process_counts)))
        process_creation_rate = process_changes / time_span
        
        # CPU spike percentage (percentage of time CPU > 80%)
        high_cpu_count = sum(1 for data in self.data_history if data['cpu_usage'] > 80)
        cpu_spike_pct = (high_cpu_count / len(self.data_history)) * 100
        
        # Disk write frequency (average bytes written per second)
        disk_writes = [data['disk_io']['write_bytes_per_sec'] for data in self.data_history]
        disk_write_freq = np.mean(disk_writes)
        
        return {
            'file_mod_rate': file_mod_rate,
            'process_creation_rate': process_creation_rate,
            'cpu_spike_pct': cpu_spike_pct,
            'disk_write_freq': disk_write_freq
        }
    
    def normalize_features(self, features):
        """Normalize features to 0-1 range"""
        if not features:
            return None
        
        # Convert to array for normalization
        feature_array = np.array([
            features['file_mod_rate'],
            features['process_creation_rate'], 
            features['cpu_spike_pct'],
            features['disk_write_freq']
        ]).reshape(1, -1)
        
        # Fit scaler on first use or update ranges
        if not self.is_fitted:
            # Use predefined ranges for initial fitting
            range_array = np.array([
                self.feature_ranges['file_mod_rate'],
                self.feature_ranges['process_creation_rate'],
                self.feature_ranges['cpu_spike_pct'], 
                self.feature_ranges['disk_write_freq']
            ])
            self.scaler.fit(range_array)
            self.is_fitted = True
        
        # Normalize features
        normalized = self.scaler.transform(feature_array)
        return normalized.flatten()
    
    def get_feature_vector(self):
        """Extract and normalize features, return ML-ready vector"""
        raw_features = self.extract_features()
        if raw_features is None:
            return None
        
        normalized_vector = self.normalize_features(raw_features)
        return {
            'raw_features': raw_features,
            'normalized_vector': normalized_vector,
            'feature_names': ['file_mod_rate', 'process_creation_rate', 'cpu_spike_pct', 'disk_write_freq']
        }
    
    def process_monitoring_data(self, monitoring_data):
        """Process new monitoring data and return feature vector"""
        self.add_data(monitoring_data)
        return self.get_feature_vector()

# Example usage
if __name__ == "__main__":
    extractor = FeatureExtractor(window_size=5)
    
    # Simulate monitoring data
    sample_data = {
        'timestamp': time.time(),
        'cpu_usage': 45.2,
        'file_operations': {'created': 2, 'deleted': 1, 'renamed': 0},
        'process_count': 156,
        'disk_io': {'write_bytes_per_sec': 1024000}
    }
    
    # Process data
    result = extractor.process_monitoring_data(sample_data)
    if result:
        print("Raw features:", result['raw_features'])
        print("Normalized vector:", result['normalized_vector'])
        print("Feature names:", result['feature_names'])