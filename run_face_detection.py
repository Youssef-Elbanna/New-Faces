#!/usr/bin/env python3
"""
Run Face Detection on Aaron Peirsol Images
This will process the new images and detect faces
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def run_face_detection_on_aaron():
    """Run face detection on Aaron Peirsol images"""
    
    print("🔍 Running Face Detection on Aaron Peirsol Images")
    print("=" * 55)
    
    try:
        # Import face service
        from services.face_service import FaceService
        face_service = FaceService()
        
        print("✅ Face service initialized")
        
        # Get Aaron Peirsol images
        from data_access.database import DatabaseManager
        db = DatabaseManager()
        conn = db._connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.id, i.image_path 
            FROM images i 
            JOIN articles a ON i.article_id = a.article_id 
            WHERE a.title LIKE '%Aaron%' AND a.title LIKE '%Peirsol%'
            ORDER BY i.id
        """)
        aaron_images = cursor.fetchall()
        
        print(f"📸 Found {len(aaron_images)} Aaron Peirsol images to process")
        
        # Process each image for face detection
        for img_id, img_path in aaron_images:
            try:
                print(f"\n🖼️ Processing image {img_id}: {os.path.basename(img_path)}")
                
                # Check if image file exists
                if not os.path.exists(img_path):
                    print(f"   ⚠️ Image file not found: {img_path}")
                    continue
                
                # Run face detection
                face_count, detected_faces = face_service.processor.detect_and_recognize_faces(img_path)
                
                print(f"   ✅ Face detection completed:")
                print(f"      Faces detected: {face_count}")
                print(f"      Face details: {detected_faces}")
                
                # Update database with face count
                cursor.execute("""
                    UPDATE images 
                    SET face_count = ?, detected_faces = ? 
                    WHERE id = ?
                """, (face_count, str(detected_faces), img_id))
                
                print(f"   💾 Database updated with face count: {face_count}")
                
            except Exception as e:
                print(f"   ❌ Error processing image {img_id}: {e}")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print(f"\n🎯 Face Detection Summary:")
        print(f"   Images processed: {len(aaron_images)}")
        print(f"   Database updated with face counts")
        print(f"   🚀 Refresh your Streamlit app to see the results!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in face detection: {e}")
        return False

if __name__ == "__main__":
    print("Starting face detection on Aaron Peirsol images...")
    success = run_face_detection_on_aaron()
    
    if success:
        print("\n🎉 Face detection completed successfully!")
        print("Now the Aaron Peirsol portrait should show the correct face count!")
    else:
        print("\n❌ Face detection failed")
