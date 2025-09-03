# Phase 4 workflow
# phases/phase4.py
import logging
from ..services.face_service import FaceService

def run_phase4():
    print("=== Phase 4: Face Detection and Tagging ===")
    service = FaceService()
    
    # Process all images for face detection and recognition
    service.process_all_images()
    
    # Display statistics
    stats = service.get_face_statistics()
    if stats:
        print("\n=== Face Detection Statistics ===")
        print(f"Total images: {stats['total_images']}")
        print(f"Images with faces: {stats['images_with_faces']}")
        print(f"Total faces detected: {stats['total_faces_detected']}")
        print(f"Known faces recognized: {stats['known_faces_recognized']}")
        print(f"Unknown faces: {stats['unknown_faces']}")
        print("=" * 50)
    
    print("Phase 4 complete.")
