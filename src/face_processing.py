# core/face_processing.py
import face_recognition
import numpy as np
import json
from typing import List, Dict, Tuple, Optional

class FaceProcessor:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """Load known faces from database for comparison"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
            from src.data_access.database import DatabaseManager
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
        """Get face encoding for a single face (existing method)"""
        try:
            image = face_recognition.load_image_file(image_path)

            # First detect all face locations
            face_locations = face_recognition.face_locations(image)

            if len(face_locations) == 0:
                return None

            # Encode faces using the detected locations
            encodings = face_recognition.face_encodings(image, face_locations)

            if len(encodings) > 0:
                # Convert numpy array to list for JSON storage
                return encodings[0].tolist()

            return None
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None

    def detect_and_recognize_faces(self, image_path: str) -> Tuple[int, List[Dict]]:
        """
        Detect faces in image and recognize them against known faces
        
        Returns:
            Tuple of (face_count, detected_faces_list)
            detected_faces_list contains dicts with 'name' and 'confidence'
        """
        try:
            image = face_recognition.load_image_file(image_path)
            
            # Detect face locations
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                return 0, []
            
            # Encode all detected faces
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            detected_faces = []
            
            for face_encoding in face_encodings:
                # Compare with known faces
                if self.known_face_encodings:
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, 
                        face_encoding,
                        tolerance=0.6  # Adjust tolerance as needed
                    )
                    
                    # Calculate face distances for confidence
                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings, 
                        face_encoding
                    )
                    
                    if True in matches:
                        # Find the best match
                        best_match_index = np.argmin(face_distances)
                        confidence = 1.0 - face_distances[best_match_index]
                        name = self.known_face_names[best_match_index]
                    else:
                        name = "unknown"
                        confidence = 0.0
                else:
                    name = "unknown"
                    confidence = 0.0
                
                detected_faces.append({
                    "name": name,
                    "confidence": round(confidence, 3)
                })
            
            return len(face_locations), detected_faces
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return 0, []

    def get_all_face_encodings(self, image_path: str) -> List[List[float]]:
        """Get all face encodings from an image"""
        try:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                return []
            
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            # Convert numpy arrays to lists for JSON storage
            return [encoding.tolist() for encoding in face_encodings]
            
        except Exception as e:
            print(f"Error getting face encodings from {image_path}: {e}")
            return []

    def get_person_encodings(self, person_name: str) -> List[List[float]]:
        """Get all encodings for a specific person"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
            from src.data_access.database import DatabaseManager
            db = DatabaseManager()
            
            conn = db._connect()
            cursor = conn.cursor()
            cursor.execute('SELECT encoding FROM known_faces WHERE name = ?', (person_name,))
            results = cursor.fetchall()
            conn.close()
            
            encodings = []
            for encoding_str, in results:
                try:
                    encoding = json.loads(encoding_str)
                    encodings.append(encoding)
                except:
                    continue
            
            return encodings
            
        except Exception as e:
            print(f"Error getting encodings for {person_name}: {e}")
            return []


