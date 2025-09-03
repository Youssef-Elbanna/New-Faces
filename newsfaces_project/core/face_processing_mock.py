# core/face_processing_mock.py
# Mock version for testing when face_recognition is not available
import json
from typing import List, Dict, Tuple, Optional

class FaceProcessorMock:
    """Mock face processor for testing without heavy dependencies"""
    
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """Load known faces from database for comparison"""
        try:
            from data_access.database import DatabaseManager
            db = DatabaseManager()
            
            conn = db._connect()
            cursor = conn.cursor()
            cursor.execute('SELECT name, encoding FROM known_faces')
            results = cursor.fetchall()
            
            for name, encoding_str in results:
                encoding = json.loads(encoding_str)
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(name)
            
            conn.close()
            print(f"Loaded {len(self.known_face_names)} known faces")
        except Exception as e:
            print(f"Error loading known faces: {e}")
            # Initialize empty lists if database is not available
            self.known_face_encodings = []
            self.known_face_names = []

    def get_face_encoding(self, image_path):
        """Mock face encoding - returns a dummy encoding"""
        print(f"[MOCK] Getting face encoding for {image_path}")
        # Return a dummy encoding for testing
        return [0.1, 0.2, 0.3, 0.4, 0.5] * 128  # 128-dimensional vector

    def detect_and_recognize_faces(self, image_path: str) -> Tuple[int, List[Dict]]:
        """
        Mock face detection and recognition
        
        Returns:
            Tuple of (face_count, detected_faces_list)
        """
        print(f"[MOCK] Detecting faces in {image_path}")
        
        # Simulate face detection with mock results
        if "test" in image_path.lower() or "sample" in image_path.lower():
            # Simulate finding 2 faces
            detected_faces = [
                {
                    "name": "John Doe" if self.known_face_names else "unknown",
                    "confidence": 0.85
                },
                {
                    "name": "Jane Smith" if len(self.known_face_names) > 1 else "unknown",
                    "confidence": 0.78
                }
            ]
            return 2, detected_faces
        else:
            # Simulate no faces found
            return 0, []

    def get_all_face_encodings(self, image_path: str) -> List[List[float]]:
        """Mock method to get all face encodings"""
        print(f"[MOCK] Getting all face encodings from {image_path}")
        # Return dummy encodings
        return [[0.1, 0.2, 0.3, 0.4, 0.5] * 128]

# Create an alias for easy import
FaceProcessor = FaceProcessorMock
