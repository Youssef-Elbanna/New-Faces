# services/face_service.py
import os
import zipfile
import logging
import json
from datetime import datetime
from typing import Dict
try:
    from core.face_processing import FaceProcessor
except ImportError:
    # Fallback to mock version if face_recognition is not available
    from core.face_processing_mock import FaceProcessor
    print("Using mock face processor (face_recognition not available)")
from data_access.database import DatabaseManager
from config import settings

class FaceService:
    def __init__(self):
        self.processor = FaceProcessor()
        self.db = DatabaseManager()

    # Extract any LFW zip found in datasets dir if not yet extr
    def _extract_lfw_zip_if_needed(self):

        if os.path.exists(settings.LFW_DATASET_PATH) and any(os.scandir(settings.LFW_DATASET_PATH)):
            logging.info("LFW dataset already extracted.")
            return

        datasets_dir = os.path.dirname(settings.LFW_DATASET_PATH)
        for file in os.listdir(datasets_dir):
            if file.lower().endswith(".zip"):
                zip_path = os.path.join(datasets_dir, file)
                logging.info(f"Extracting LFW dataset from {zip_path} ...")
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(settings.LFW_DATASET_PATH)
                logging.info("LFW dataset extraction complete.")
                return

    # Returns the folder that contains the person subdirectories.
    def _find_people_root(self):
        root = settings.LFW_DATASET_PATH
        while True:
            subdirs = [
                os.path.join(root, d) for d in os.listdir(root)
                if os.path.isdir(os.path.join(root, d))
            ]
            if len(subdirs) == 1 and not subdirs[0].lower().endswith(('.jpg', '.jpeg', '.png')):
                root = subdirs[0]
            else:
                break

        return root

    def enroll_faces(self):
        logging.info("=== Phase 3: Enrolling faces from LFW dataset ===")

        self._extract_lfw_zip_if_needed()

        people_root = self._find_people_root()
        if not os.path.exists(people_root):
            logging.error("LFW dataset not found after extraction.")
            return

        people = sorted([
            d for d in os.listdir(people_root)
            if os.path.isdir(os.path.join(people_root, d))
        ])[:settings.MAX_PEOPLE]

        logging.info(f"Found {len(people)} people in LFW dataset.")

        enrolled_count = 0
        failed_count = 0

        for person in people:
            person_dir = os.path.join(people_root, person)
            image_files = []
            for root, _, files in os.walk(person_dir):
                for file in files:
                    if file.lower().endswith((".jpg", ".jpeg", ".png")):
                        image_files.append(os.path.join(root, file))

            if not image_files:
                logging.warning(f"No images found for {person}")
                continue

            person_encodings = []
            for img_path in image_files:
                encoding = self.processor.get_face_encoding(img_path)
                if encoding is not None:
                    #  to ens Store one encoding at a time
                    self.db.insert_face_encoding(person.replace("_", " "), encoding)
                    person_encodings.append(encoding)

            if person_encodings:
                enrolled_count += 1
                logging.info(f"✓ Enrolled {person} with {len(person_encodings)} encodings")
            else:
                failed_count += 1
                logging.warning(f"✗ No valid encodings found for {person}")

        logging.info("=" * 50)
        logging.info(f"Enrollment complete: {enrolled_count} people enrolled, {failed_count} failed.")
        logging.info("=" * 50)

    def process_image_faces(self, image_path: str, image_id: int) -> bool:
        """
        Process an image to detect and recognize faces, then store results in database
        
        Args:
            image_path: Path to the image file
            image_id: Database ID of the image record
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logging.info(f"Processing faces in image: {image_path}")
            
            # Detect and recognize faces
            face_count, detected_faces = self.processor.detect_and_recognize_faces(image_path)
            
            # Update database with results
            success = self.db.update_image_face_detection(image_id, face_count, detected_faces)
            
            if success:
                logging.info(f"✓ Processed image {image_id}: {face_count} faces detected")
                if detected_faces:
                    names = [face['name'] for face in detected_faces]
                    logging.info(f"  Detected faces: {', '.join(names)}")
                return True
            else:
                logging.error(f"✗ Failed to update database for image {image_id}")
                return False
                
        except Exception as e:
            logging.error(f"Error processing faces in image {image_path}: {e}")
            return False

    def process_all_images(self):
        """
        Process all images in the database for face detection and recognition
        """
        logging.info("=== Processing all images for face detection ===")
        
        try:
            conn = self.db._connect()
            cursor = conn.cursor()
            
            # Get all images that haven't been processed yet (face_count = 0)
            cursor.execute('''
                SELECT id, image_path FROM images 
                WHERE face_count = 0 OR face_count IS NULL
            ''')
            
            unprocessed_images = cursor.fetchall()
            conn.close()
            
            if not unprocessed_images:
                logging.info("No unprocessed images found.")
                return
            
            logging.info(f"Found {len(unprocessed_images)} images to process.")
            
            processed_count = 0
            failed_count = 0
            
            for image_id, image_path in unprocessed_images:
                if os.path.exists(image_path):
                    if self.process_image_faces(image_path, image_id):
                        processed_count += 1
                    else:
                        failed_count += 1
                else:
                    logging.warning(f"Image file not found: {image_path}")
                    failed_count += 1
            
            logging.info("=" * 50)
            logging.info(f"Face processing complete: {processed_count} processed, {failed_count} failed.")
            logging.info("=" * 50)
            
        except Exception as e:
            logging.error(f"Error processing all images: {e}")

    def get_face_statistics(self) -> Dict:
        """
        Get statistics about face detection results
        """
        try:
            conn = self.db._connect()
            cursor = conn.cursor()
            
            # Total images
            cursor.execute('SELECT COUNT(*) FROM images')
            total_images = cursor.fetchone()[0]
            
            # Images with faces
            cursor.execute('SELECT COUNT(*) FROM images WHERE face_count > 0')
            images_with_faces = cursor.fetchone()[0]
            
            # Total faces detected
            cursor.execute('SELECT SUM(face_count) FROM images WHERE face_count > 0')
            total_faces = cursor.fetchone()[0] or 0
            
            # Known vs unknown faces
            cursor.execute('''
                SELECT detected_faces FROM images 
                WHERE face_count > 0 AND detected_faces IS NOT NULL
            ''')
            all_detected_faces = cursor.fetchall()
            
            known_faces = 0
            unknown_faces = 0
            
            for (detected_faces_str,) in all_detected_faces:
                try:
                    detected_faces = json.loads(detected_faces_str)
                    for face in detected_faces:
                        if face['name'] == 'unknown':
                            unknown_faces += 1
                        else:
                            known_faces += 1
                except:
                    continue
            
            conn.close()
            
            return {
                'total_images': total_images,
                'images_with_faces': images_with_faces,
                'total_faces_detected': total_faces,
                'known_faces_recognized': known_faces,
                'unknown_faces': unknown_faces
            }
            
        except Exception as e:
            logging.error(f"Error getting face statistics: {e}")
            return {}
