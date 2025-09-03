import sqlite3
import json
import traceback
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import settings


class DatabaseManager:
    def __init__(self, db_path=settings.DB_PATH):
        self.db_path = db_path
        self.init_database()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # Initialize tables for database
    def init_database(self):

        try:
            conn = self._connect()
            cursor = conn.cursor()

            # Articles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_uri TEXT,
                    title TEXT,
                    cleaned_text TEXT,
                    language TEXT,
                    sentiment_label TEXT,
                    sentiment_score REAL,
                    topic_category TEXT,
                    keywords TEXT,
                    person_entities TEXT,
                    org_entities TEXT,
                    location_entities TEXT,
                    publication_date TEXT,
                    source_domain TEXT,
                    author TEXT,
                    word_count INTEGER,
                    reading_time_minutes REAL
                )
            ''')

            # Images table with face detection results
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article_id INTEGER,
                    image_path TEXT,
                    face_count INTEGER DEFAULT 0,
                    detected_faces TEXT DEFAULT '[]',
                    image_url TEXT,
                    image_alt_text TEXT,
                    image_caption TEXT,
                    image_width INTEGER,
                    image_height INTEGER,
                    image_size_bytes INTEGER,
                    FOREIGN KEY(article_id) REFERENCES articles(article_id)
                )
            ''')

            # Enhanced known faces table with news metadata
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS known_faces (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    encoding TEXT,
                    profession TEXT,
                    organization TEXT,
                    political_party TEXT,
                    country TEXT,
                    birth_date TEXT,
                    death_date TEXT,
                    wikipedia_url TEXT,
                    news_mentions_count INTEGER DEFAULT 0,
                    first_seen_date TEXT,
                    last_seen_date TEXT,
                    confidence_score REAL DEFAULT 0.0,
                    face_image_path TEXT,
                    metadata TEXT DEFAULT '{}'
                )
            ''')

            # News sources table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS news_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain TEXT UNIQUE,
                    name TEXT,
                    country TEXT,
                    language TEXT,
                    category TEXT,
                    reliability_score REAL,
                    political_bias TEXT,
                    fact_checking_status TEXT
                )
            ''')

            # Face recognition history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS face_recognition_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    face_id INTEGER,
                    image_id INTEGER,
                    article_id INTEGER,
                    recognition_date TEXT,
                    confidence_score REAL,
                    context TEXT,
                    FOREIGN KEY(face_id) REFERENCES known_faces(id),
                    FOREIGN KEY(image_id) REFERENCES images(id),
                    FOREIGN KEY(article_id) REFERENCES articles(article_id)
                )
            ''')

            # News categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS news_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    description TEXT,
                    parent_category TEXT,
                    color_code TEXT
                )
            ''')

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing database: {e}")
            traceback.print_exc()

    # Insert article into enhanced schema
    def insert_article(self, article_data):

        try:
            conn = self._connect()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO articles (
                    target_uri, title, cleaned_text, language, sentiment_label,
                    sentiment_score, topic_category, keywords,
                    person_entities, org_entities, location_entities,
                    publication_date, source_domain, author, word_count, reading_time_minutes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article_data.get('target_uri'),
                article_data.get('title'),
                article_data.get('cleaned_text'),
                article_data.get('language'),
                article_data.get('sentiment_label'),
                article_data.get('sentiment_score'),
                article_data.get('topic_category'),
                json.dumps(article_data.get('keywords', []), ensure_ascii=False)
                    if not isinstance(article_data.get('keywords'), str)
                    else article_data.get('keywords'),
                json.dumps(article_data.get('person_entities', []), ensure_ascii=False)
                    if not isinstance(article_data.get('person_entities'), str)
                    else article_data.get('person_entities'),
                json.dumps(article_data.get('org_entities', []), ensure_ascii=False)
                    if not isinstance(article_data.get('org_entities'), str)
                    else article_data.get('org_entities'),
                json.dumps(article_data.get('location_entities', []), ensure_ascii=False)
                    if not isinstance(article_data.get('location_entities'), str)
                    else article_data.get('location_entities'),
                article_data.get('publication_date'),
                article_data.get('source_domain'),
                article_data.get('author'),
                article_data.get('word_count'),
                article_data.get('reading_time_minutes')
            ))

            article_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return article_id

        except Exception as e:
            print(f"Error inserting article: {e}")
            traceback.print_exc()
            return None

    def insert_image(self, article_id, image_path, image_metadata=None):
        """Insert image with enhanced metadata"""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            
            if image_metadata is None:
                image_metadata = {}
            
            cursor.execute('''
                INSERT INTO images (
                    article_id, image_path, image_url, image_alt_text, 
                    image_caption, image_width, image_height, image_size_bytes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article_id, 
                image_path,
                image_metadata.get('url'),
                image_metadata.get('alt_text'),
                image_metadata.get('caption'),
                image_metadata.get('width'),
                image_metadata.get('height'),
                image_metadata.get('size_bytes')
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error inserting image: {e}")
            traceback.print_exc()
            return False

    def update_image_face_detection(self, image_id, face_count, detected_faces):
        """Update image with face detection results"""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE images 
                SET face_count = ?, detected_faces = ?
                WHERE id = ?
            ''', (face_count, json.dumps(detected_faces), image_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating image face detection: {e}")
            traceback.print_exc()
            return False

    def get_image_by_id(self, image_id):
        """Get image record by ID"""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, article_id, image_path, face_count, detected_faces,
                       image_url, image_alt_text, image_caption, image_width, image_height
                FROM images WHERE id = ?
            ''', (image_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            print(f"Error getting image: {e}")
            traceback.print_exc()
            return None

    def insert_face_encoding(self, name, encoding, face_metadata=None):
        """Insert face encoding with enhanced metadata"""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            
            if face_metadata is None:
                face_metadata = {}
            
            cursor.execute('''
                INSERT INTO known_faces (
                    name, encoding, profession, organization, political_party,
                    country, birth_date, death_date, wikipedia_url,
                    face_image_path, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name, 
                json.dumps(encoding),
                face_metadata.get('profession'),
                face_metadata.get('organization'),
                face_metadata.get('political_party'),
                face_metadata.get('country'),
                face_metadata.get('birth_date'),
                face_metadata.get('death_date'),
                face_metadata.get('wikipedia_url'),
                face_metadata.get('face_image_path'),
                json.dumps(face_metadata.get('additional_metadata', {}))
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error inserting face encoding: {e}")
            traceback.print_exc()
            return False

    def get_article_count(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM articles')
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_image_count(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM images')
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_known_faces_count(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(DISTINCT name) FROM known_faces')
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_all_articles(self, limit=100, offset=0):
        """Get all articles with pagination"""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT article_id, title, target_uri, publication_date, 
                       source_domain, topic_category, sentiment_label, sentiment_score
                FROM articles 
                ORDER BY publication_date DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"Error getting articles: {e}")
            return []

    def get_all_images(self, limit=100, offset=0):
        """Get all images with pagination"""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT i.id, i.image_path, i.face_count, i.detected_faces,
                       a.title as article_title, a.source_domain
                FROM images i
                JOIN articles a ON i.article_id = a.article_id
                ORDER BY i.id DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"Error getting images: {e}")
            return []

    def get_all_known_faces(self, limit=100, offset=0):
        """Get all known faces with pagination"""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, profession, organization, country, 
                       news_mentions_count, confidence_score
                FROM known_faces 
                ORDER BY news_mentions_count DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"Error getting known faces: {e}")
            return []

    def search_articles(self, query, limit=50):
        """Search articles by title or content"""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT article_id, title, target_uri, publication_date, 
                       source_domain, topic_category
                FROM articles 
                WHERE title LIKE ? OR cleaned_text LIKE ?
                ORDER BY publication_date DESC 
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', limit))
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"Error searching articles: {e}")
            return []

    def get_face_recognition_history(self, face_id=None, limit=100):
        """Get face recognition history"""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            
            if face_id:
                cursor.execute('''
                    SELECT fh.id, fh.recognition_date, fh.confidence_score,
                           fh.context, a.title as article_title, i.image_path
                    FROM face_recognition_history fh
                    JOIN articles a ON fh.article_id = a.article_id
                    JOIN images i ON fh.image_id = i.id
                    WHERE fh.face_id = ?
                    ORDER BY fh.recognition_date DESC
                    LIMIT ?
                ''', (face_id, limit))
            else:
                cursor.execute('''
                    SELECT fh.id, fh.recognition_date, fh.confidence_score,
                           fh.context, a.title as article_title, i.image_path,
                           kf.name as face_name
                    FROM face_recognition_history fh
                    JOIN articles a ON fh.article_id = a.article_id
                    JOIN images i ON fh.image_id = i.id
                    JOIN known_faces kf ON fh.face_id = kf.id
                    ORDER BY fh.recognition_date DESC
                    LIMIT ?
                ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"Error getting face recognition history: {e}")
            return []
