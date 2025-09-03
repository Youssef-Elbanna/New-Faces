# Class Diagram - NewsFaces System

## 1. System Class Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLASS HIERARCHY                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Services  │  │  Processors │  │   Database  │  │   Utils     │      │
│  │   Layer     │  │   Layer     │  │   Layer     │  │   Layer     │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2. Detailed Class Structure

### Core Service Classes

#### FaceService
```python
class FaceService:
    - processor: FaceProcessor
    - database: DatabaseManager
    
    + __init__()
    + process_image_faces(image_path: str, image_id: int) -> bool
    + enroll_faces_from_dataset(dataset_path: str) -> bool
    + get_face_statistics() -> Dict
    + update_face_recognition(image_path: str) -> bool
```

#### TextService
```python
class TextService:
    - processor: TextProcessor
    - database: DatabaseManager
    
    + __init__()
    + process_html_files() -> bool
    + analyze_sentiment(text: str) -> Dict
    + extract_entities(text: str) -> List[str]
    + categorize_topic(text: str) -> str
    + process_articles() -> bool
```

#### WARCService
```python
class WARCService:
    - file_manager: FileManager
    - database: DatabaseManager
    
    + __init__()
    + process_warc_files(warc_dir: str) -> bool
    + extract_articles(warc_file: str) -> List[Dict]
    + download_images(image_urls: List[str]) -> List[str]
    + generate_mappings() -> bool
```

### Processor Classes

#### FaceProcessor
```python
class FaceProcessor:
    - known_face_encodings: List[List[float]]
    - known_face_names: List[str]
    
    + __init__()
    + load_known_faces() -> None
    + get_face_encoding(image_path: str) -> Optional[List[float]]
    + detect_and_recognize_faces(image_path: str) -> Tuple[int, List[Dict]]
    + get_all_face_encodings(image_path: str) -> List[List[float]]
    + get_person_encodings(person_name: str) -> List[List[float]]
```

#### TextProcessor
```python
class TextProcessor:
    - nlp_model: Any
    - sentiment_analyzer: Any
    
    + __init__()
    + clean_html(html_content: str) -> str
    + extract_text(html_content: str) -> str
    + analyze_sentiment(text: str) -> Dict
    + extract_entities(text: str) -> List[str]
    + categorize_content(text: str) -> str
```

### Database Classes

#### DatabaseManager
```python
class DatabaseManager:
    - db_path: str
    - connection: sqlite3.Connection
    
    + __init__(db_path: str = None)
    + _connect() -> sqlite3.Connection
    + create_tables() -> bool
    + insert_article(article_data: Dict) -> int
    + insert_image(image_data: Dict) -> int
    + insert_face_encoding(face_data: Dict) -> int
    + get_article_count() -> int
    + get_image_count() -> int
    + get_known_faces_count() -> int
    + get_all_articles() -> List[Tuple]
    + get_all_images() -> List[Tuple]
    + get_all_known_faces() -> List[Tuple]
    + search_articles(query: str) -> List[Tuple]
    + get_face_recognition_history() -> List[Tuple]
```

### File Management Classes

#### FileManager
```python
class FileManager:
    - base_path: str
    - extracted_path: str
    
    + __init__(base_path: str)
    + create_directories() -> bool
    + save_html(content: str, filename: str) -> str
    + save_image(image_data: bytes, filename: str) -> str
    + download_file(url: str, filename: str) -> bool
    + get_file_path(filename: str) -> str
    + cleanup_temp_files() -> bool
```

### Phase Management Classes

#### Phase1 (WARC Processing)
```python
class Phase1:
    - warc_service: WARCService
    
    + __init__()
    + run() -> bool
    + process_warc_files() -> bool
    + extract_content() -> bool
    + save_extracted_data() -> bool
```

#### Phase2 (Text Processing)
```python
class Phase2:
    - text_service: TextService
    
    + __init__()
    + run() -> bool
    + process_html_files() -> bool
    + analyze_content() -> bool
    + update_database() -> bool
```

#### Phase3 (Face Enrollment)
```python
class Phase3:
    - face_service: FaceService
    
    + __init__()
    + run() -> bool
    + load_lfw_dataset() -> bool
    + extract_face_encodings() -> bool
    + store_encodings() -> bool
```

#### Phase4 (Face Detection)
```python
class Phase4:
    - face_service: FaceService
    
    + __init__()
    + run() -> bool
    + process_all_images() -> bool
    + detect_faces() -> bool
    + update_face_counts() -> bool
```

### Utility Classes

#### LoggingUtils
```python
class LoggingUtils:
    - logger: logging.Logger
    
    + __init__(name: str)
    + setup_logging(log_file: str) -> None
    + log_info(message: str) -> None
    + log_error(message: str) -> None
    + log_debug(message: str) -> None
```

## 3. Class Relationships

### Inheritance Relationships
```
BaseProcessor (Abstract)
    ├── FaceProcessor
    ├── TextProcessor
    └── WARCProcessor

BaseService (Abstract)
    ├── FaceService
    ├── TextService
    └── WARCService
```

### Composition Relationships
```
FaceService
    ├── FaceProcessor (1:1)
    └── DatabaseManager (1:1)

TextService
    ├── TextProcessor (1:1)
    └── DatabaseManager (1:1)

WARCService
    ├── FileManager (1:1)
    └── DatabaseManager (1:1)
```

### Association Relationships
```
Dashboard
    ├── FaceService (1:1)
    ├── TextService (1:1)
    ├── WARCService (1:1)
    └── DatabaseManager (1:1)

PhaseManager
    ├── Phase1 (1:1)
    ├── Phase2 (1:1)
    ├── Phase3 (1:1)
    └── Phase4 (1:1)
```

## 4. Class Dependencies

### High-Level Dependencies
```
Streamlit App
    ↓
Dashboard
    ↓
Services (Face, Text, WARC)
    ↓
Processors (Face, Text, WARC)
    ↓
DatabaseManager
    ↓
SQLite Database
```

### Service Dependencies
```
FaceService → FaceProcessor → face_recognition library
TextService → TextProcessor → NLP libraries
WARCService → FileManager → OS file system
All Services → DatabaseManager → SQLite
```

## 5. Method Signatures

### Core Methods
```python
# Face Detection
def detect_and_recognize_faces(image_path: str) -> Tuple[int, List[Dict]]:
    """
    Detect faces in image and recognize them against known faces
    
    Returns:
        Tuple of (face_count, detected_faces_list)
        detected_faces_list contains dicts with 'name' and 'confidence'
    """

# Text Analysis
def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of given text
    
    Returns:
        Dictionary with 'label' and 'score' keys
    """

# Database Operations
def insert_article(article_data: Dict[str, Any]) -> int:
    """
    Insert article into database
    
    Returns:
        ID of inserted article
    """
```

## 6. Error Handling

### Exception Classes
```python
class NewsFacesError(Exception):
    """Base exception for NewsFaces system"""
    pass

class FaceProcessingError(NewsFacesError):
    """Exception raised during face processing"""
    pass

class DatabaseError(NewsFacesError):
    """Exception raised during database operations"""
    pass

class FileProcessingError(NewsFacesError):
    """Exception raised during file processing"""
    pass
```

### Error Handling Patterns
```python
try:
    result = processor.process_data(input_data)
except FaceProcessingError as e:
    logger.error(f"Face processing failed: {e}")
    return False
except DatabaseError as e:
    logger.error(f"Database operation failed: {e}")
    return False
```

## 7. Configuration Management

### Settings Class
```python
class Settings:
    - LFW_DATASET_PATH: str
    - DATABASE_PATH: str
    - EXTRACTED_DATA_PATH: str
    - LOG_LEVEL: str
    - FACE_RECOGNITION_TOLERANCE: float
    
    + __init__()
    + load_from_file(config_file: str) -> None
    + get_setting(key: str) -> Any
    + set_setting(key: str, value: Any) -> None
```

## 8. Testing Support

### Mock Classes
```python
class MockFaceProcessor(FaceProcessor):
    """Mock face processor for testing"""
    
    + __init__()
    + detect_and_recognize_faces(image_path: str) -> Tuple[int, List[Dict]]
    + get_face_encoding(image_path: str) -> List[float]

class MockDatabaseManager(DatabaseManager):
    """Mock database manager for testing"""
    
    + __init__()
    + insert_article(article_data: Dict) -> int
    + get_article_count() -> int
```
