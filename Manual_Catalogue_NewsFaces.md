# Manual Catalogue - NewsFaces System

## 1. System Overview

### Project Description
NewsFaces is an intelligent face recognition and news analysis system that processes web archive files, extracts articles and images, performs face detection and recognition, and provides comprehensive analytics through a web dashboard.

### System Purpose
- **Primary**: Automate face recognition in news articles and images
- **Secondary**: Provide sentiment analysis and content categorization
- **Tertiary**: Generate analytics matrices for system performance evaluation

## 2. System Architecture

### High-Level Components
1. **Data Input Layer**: WARC files, LFW dataset, Wikipedia pages
2. **Processing Layer**: 4-phase pipeline (WARC → Text → Face Enrollment → Face Detection)
3. **Storage Layer**: SQLite database, file system, JSON mappings
4. **Presentation Layer**: Streamlit dashboard with analytics

### Technology Stack
- **Backend**: Python 3.8+
- **Face Recognition**: dlib + face_recognition
- **Web Framework**: Streamlit
- **Database**: SQLite
- **Data Processing**: pandas, numpy, scikit-learn
- **Web Scraping**: requests, BeautifulSoup

## 3. Installation and Setup

### Prerequisites
```bash
# System Requirements
- Python 3.8 or higher
- 8GB RAM minimum
- 10GB free disk space
- Windows 10/11 or Linux

# Python Dependencies
- pip (Python package installer)
- virtual environment support
```

### Installation Steps
```bash
# 1. Clone Repository
git clone <repository-url>
cd Newsfaces-main

# 2. Create Virtual Environment
python -m venv .venv

# 3. Activate Virtual Environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Install Dependencies
pip install -r requirements.txt

# 5. Verify Installation
python -c "import face_recognition; print('Installation successful')"
```

### Configuration
```python
# config/settings.py
LFW_DATASET_PATH = "data/datasets/lfw"
DATABASE_PATH = "data/database/newsfaces.db"
EXTRACTED_DATA_PATH = "data/extracted_data"
LOG_LEVEL = "INFO"
```

## 4. System Operation

### Phase 1: WARC Processing
```bash
# Run Phase 1
python -c "from src.phases.phase1 import Phase1; Phase1().run()"

# What it does:
# - Extracts WARC files from data/warc_files/
# - Parses HTML content and downloads images
# - Generates mappings.json for content relationships
# - Saves extracted data to data/extracted_data/
```

### Phase 2: Text Processing
```bash
# Run Phase 2
python -c "from src.phases.phase2 import Phase2; Phase2().run()"

# What it does:
# - Processes extracted HTML files
# - Performs sentiment analysis
# - Extracts named entities
# - Categorizes content by topic
# - Updates database with analysis results
```

### Phase 3: Face Enrollment
```bash
# Run Phase 3
python -c "from src.phases.phase3 import Phase3; Phase3().run()"

# What it does:
# - Loads LFW dataset
# - Extracts face encodings (128-dimensional vectors)
# - Stores encodings in known_faces table
# - Prepares face recognition system
```

### Phase 4: Face Detection
```bash
# Run Phase 4
python -c "from src.phases.phase4 import Phase4; Phase4().run()"

# What it does:
# - Processes all images in database
# - Detects faces in each image
# - Recognizes faces against known faces
# - Updates face counts and recognition results
```

## 5. Dashboard Usage

### Starting the Dashboard
```bash
# Navigate to apps directory
cd apps

# Start Streamlit dashboard
streamlit run streamlit_app_simple.py

# Dashboard will open at: http://localhost:8501
```

### Dashboard Features

#### Main Dashboard
- **System Overview**: Key metrics and statistics
- **Recent Activity**: Charts and visualizations
- **Recent Articles**: Latest processed articles
- **Face Recognition Analytics**: Embedded matrix visualizations

#### Articles Page
- **Search**: Find articles by keywords
- **Filters**: Category, sentiment, language
- **Article Details**: Full article information with related images

#### Images & Faces Page
- **Image Display**: View all processed images
- **Face Detection**: See detected faces and counts
- **Processing**: Re-process images for face detection

#### Known Faces Page
- **Face Database**: View all enrolled faces
- **Add New Face**: Upload and enroll new individuals
- **Search**: Find faces by name

#### Analytics Page
- **Distance Matrix**: Face similarity distances
- **Similarity Matrix**: Normalized similarity scores
- **Recognition Accuracy**: Per-person accuracy metrics
- **Threshold Performance**: System performance at different confidence levels

#### Search Page
- **Advanced Search**: Multi-type search functionality
- **Results**: Comprehensive search results
- **Filters**: Refine search results

## 6. Data Management

### Database Structure
```sql
-- Main Tables
articles: News articles with metadata
images: Extracted images with face counts
known_faces: Enrolled face encodings
face_recognition_history: Recognition results and performance

-- Key Fields
articles: title, target_uri, sentiment_score, topic_category
images: image_path, face_count, detected_faces
known_faces: name, encoding, confidence_score
```

### File Organization
```
data/
├── warc_files/          # Input WARC files
├── datasets/
│   └── lfw/            # Labeled Faces in the Wild dataset
├── extracted_data/
│   ├── html/           # Extracted HTML files
│   ├── images/         # Downloaded images
│   ├── mappings.json   # Content relationships
│   └── face_matrices.json # Analytics matrices
└── database/
    └── newsfaces.db    # SQLite database
```

### Data Backup
```bash
# Database Backup
cp data/database/newsfaces.db backup/newsfaces_$(date +%Y%m%d).db

# File System Backup
tar -czf backup/extracted_data_$(date +%Y%m%d).tar.gz data/extracted_data/
```

## 7. Troubleshooting

### Common Issues

#### Face Recognition Not Working
```bash
# Check if face_recognition is installed
python -c "import face_recognition"

# If not installed, install manually
pip install dlib
pip install face_recognition

# Verify LFW dataset path
ls data/datasets/lfw/
```

#### Database Connection Errors
```bash
# Check database file exists
ls -la data/database/

# Check file permissions
chmod 644 data/database/newsfaces.db

# Recreate database if corrupted
rm data/database/newsfaces.db
python -c "from src.data_access.database import DatabaseManager; DatabaseManager().create_tables()"
```

#### Image Display Issues
```bash
# Check image paths
ls -la data/extracted_data/images/

# Verify file permissions
chmod 644 data/extracted_data/images/*

# Check path separators (Windows vs Linux)
# Windows uses \, Linux uses /
```

#### Memory Issues
```bash
# Check available memory
free -h  # Linux
wmic computersystem get TotalPhysicalMemory  # Windows

# Reduce batch sizes in processing
# Modify batch_size parameters in phase files
```

### Performance Optimization

#### Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_articles_title ON articles(title);
CREATE INDEX idx_images_article_id ON images(article_id);
CREATE INDEX idx_known_faces_name ON known_faces(name);

-- Optimize database
VACUUM;
ANALYZE;
```

#### Processing Optimization
```python
# Reduce memory usage
BATCH_SIZE = 100  # Process 100 items at a time

# Enable parallel processing
import multiprocessing
pool = multiprocessing.Pool(processes=4)
```

## 8. Maintenance

### Regular Tasks

#### Daily
- Check system logs for errors
- Monitor disk space usage
- Verify dashboard accessibility

#### Weekly
- Database optimization (VACUUM, ANALYZE)
- Clean up temporary files
- Review system performance metrics

#### Monthly
- Full system backup
- Update dependencies
- Performance review and optimization

### Log Management
```bash
# View system logs
tail -f logs/newsfaces.log

# Log rotation
logrotate -f /etc/logrotate.d/newsfaces

# Log cleanup
find logs/ -name "*.log" -mtime +30 -delete
```

## 9. Security Considerations

### Data Privacy
- **Local Storage**: All data stored locally
- **No External Transmission**: No data sent to external servers
- **Access Control**: Dashboard access control through Streamlit

### Best Practices
- Regular security updates
- Secure file permissions
- Backup encryption
- Access logging

## 10. Support and Documentation

### Getting Help
1. **Check Logs**: Review system logs for error messages
2. **Documentation**: Refer to this manual and code comments
3. **Community**: Check project repository for issues and solutions

### Useful Commands
```bash
# System Status
python -c "from src.data_access.database import DatabaseManager; db = DatabaseManager(); print(f'Articles: {db.get_article_count()}, Images: {db.get_image_count()}, Faces: {db.get_known_faces_count()}')"

# Check Face Recognition
python -c "import face_recognition; print('Face recognition available')"

# Test Database
python -c "from src.data_access.database import DatabaseManager; db = DatabaseManager(); print('Database connection successful')"

# Generate Analytics
python -c "from src.services.face_service import FaceService; fs = FaceService(); print('Face service initialized')"
```

---

# Dependency Matrix - NewsFaces System

## 1. Package Dependencies

### Core Dependencies
| Package | Version | Purpose | Required |
|---------|---------|---------|----------|
| Python | 3.8+ | Runtime environment | ✅ |
| face_recognition | 1.3.0+ | Face detection/recognition | ✅ |
| dlib | 19.22+ | Face processing backend | ✅ |
| streamlit | 1.28+ | Web dashboard | ✅ |
| pandas | 1.5+ | Data manipulation | ✅ |
| numpy | 1.21+ | Numerical computing | ✅ |
| Pillow | 9.0+ | Image processing | ✅ |
| requests | 2.28+ | HTTP requests | ✅ |
| beautifulsoup4 | 4.11+ | HTML parsing | ✅ |
| plotly | 5.0+ | Data visualization | ✅ |

### Optional Dependencies
| Package | Version | Purpose | Required |
|---------|---------|---------|----------|
| scikit-learn | 1.1+ | Machine learning | ❌ |
| transformers | 4.20+ | NLP processing | ❌ |
| opencv-python | 4.6+ | Computer vision | ❌ |
| warcio | 1.7+ | WARC file processing | ❌ |

## 2. System Dependencies

### Operating System
| OS | Version | Support | Notes |
|----|---------|---------|-------|
| Windows | 10/11 | ✅ Full | Tested on Windows 10/11 |
| Linux | Ubuntu 18.04+ | ✅ Full | Recommended for production |
| macOS | 10.15+ | ⚠️ Partial | May have dlib compilation issues |

### Hardware Requirements
| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| CPU | 4 cores | 8+ cores | Multi-core for parallel processing |
| RAM | 8GB | 16GB+ | Large datasets require more memory |
| Storage | 10GB | 50GB+ | WARC files and images are large |
| GPU | Not required | NVIDIA GPU | Optional for faster face processing |

## 3. File Dependencies

### Input Files
| File Type | Location | Purpose | Required |
|-----------|----------|---------|----------|
| WARC files | data/warc_files/ | Web archive data | ✅ |
| LFW dataset | data/datasets/lfw/ | Face training data | ✅ |
| Configuration | config/settings.py | System settings | ✅ |

### Generated Files
| File Type | Location | Purpose | Generated By |
|-----------|----------|---------|--------------|
| Database | data/database/newsfaces.db | Data storage | DatabaseManager |
| Mappings | data/extracted_data/mappings.json | Content relationships | WARCService |
| Matrices | data/extracted_data/face_matrices.json | Analytics data | Analytics Engine |
| Logs | logs/newsfaces.log | System logs | LoggingUtils |

## 4. Service Dependencies

### Service Hierarchy
```
Streamlit Dashboard
    ↓
FaceService → FaceProcessor → face_recognition library
    ↓
TextService → TextProcessor → NLP libraries
    ↓
WARCService → FileManager → OS file system
    ↓
DatabaseManager → SQLite → File system
```

### Internal Dependencies
| Service | Depends On | Purpose |
|---------|------------|---------|
| FaceService | FaceProcessor, DatabaseManager | Face recognition operations |
| TextService | TextProcessor, DatabaseManager | Text analysis operations |
| WARCService | FileManager, DatabaseManager | WARC processing operations |
| Dashboard | All Services | User interface |

## 5. Phase Dependencies

### Pipeline Dependencies
```
Phase 1 (WARC) → Phase 2 (Text) → Phase 3 (Face Enrollment) → Phase 4 (Face Detection)
     ↓              ↓                    ↓                        ↓
  WARC files   HTML content      Known faces              Face recognition
     ↓              ↓                    ↓                        ↓
  File system   Database         Database                 Analytics matrices
```

### Phase Requirements
| Phase | Input Requirements | Output Produces | Dependencies |
|-------|-------------------|-----------------|--------------|
| Phase 1 | WARC files | HTML + Images | None |
| Phase 2 | HTML files | Text analysis | Phase 1 complete |
| Phase 3 | LFW dataset | Face encodings | None |
| Phase 4 | Images + Known faces | Recognition results | Phase 3 complete |

## 6. Database Dependencies

### Table Dependencies
```
articles (independent)
    ↓
images (depends on articles)
    ↓
face_recognition_history (depends on images + known_faces)
    ↓
known_faces (independent)
```

### Foreign Key Relationships
| Table | Foreign Key | References | Cascade |
|-------|-------------|------------|---------|
| images | article_id | articles.article_id | DELETE CASCADE |
| face_recognition_history | image_id | images.id | DELETE CASCADE |
| face_recognition_history | face_id | known_faces.id | DELETE CASCADE |

## 7. Configuration Dependencies

### Environment Variables
| Variable | Default | Purpose | Required |
|----------|---------|---------|----------|
| PYTHONPATH | Project root | Module imports | ✅ |
| LFW_DATASET_PATH | data/datasets/lfw | Face dataset location | ✅ |
| DATABASE_PATH | data/database/newsfaces.db | Database location | ✅ |
| LOG_LEVEL | INFO | Logging verbosity | ❌ |

### File Permissions
| Directory/File | Permissions | Purpose |
|----------------|-------------|---------|
| data/ | 755 | Data storage |
| data/database/ | 755 | Database files |
| data/extracted_data/ | 755 | Processed data |
| logs/ | 755 | Log files |
| *.db | 644 | Database files |
| *.log | 644 | Log files |

## 8. Network Dependencies

### External Services
| Service | Purpose | Required | Notes |
|---------|---------|----------|-------|
| Internet | Download dependencies | ✅ | During installation |
| PyPI | Python packages | ✅ | Package installation |
| None | Runtime operation | ❌ | System works offline |

### Network Configuration
- **No external API calls** during runtime
- **Offline operation** supported after setup
- **Local network** not required
- **Firewall friendly** - no outgoing connections

## 9. Version Compatibility

### Python Version Compatibility
| Python Version | Status | Notes |
|----------------|--------|-------|
| 3.8 | ✅ Full | Minimum supported version |
| 3.9 | ✅ Full | Recommended version |
| 3.10 | ✅ Full | Fully compatible |
| 3.11 | ✅ Full | Latest stable version |
| 3.12 | ⚠️ Partial | May have compatibility issues |

### Library Version Compatibility
| Library | Min Version | Max Version | Notes |
|---------|-------------|-------------|-------|
| face_recognition | 1.3.0 | Latest | Core functionality |
| dlib | 19.22 | Latest | Face processing backend |
| streamlit | 1.28 | Latest | Dashboard framework |
| pandas | 1.5 | Latest | Data manipulation |

## 10. Dependency Resolution

### Installation Order
```bash
# 1. System dependencies
sudo apt-get install cmake build-essential  # Linux
# Windows: Install Visual Studio Build Tools

# 2. Python environment
python -m venv .venv
source .venv/bin/activate  # Linux
# .venv\Scripts\activate  # Windows

# 3. Core libraries
pip install numpy pandas Pillow requests beautifulsoup4

# 4. Face recognition (order matters)
pip install dlib
pip install face_recognition

# 5. Dashboard and utilities
pip install streamlit plotly

# 6. Optional libraries
pip install scikit-learn transformers opencv-python
```

### Conflict Resolution
| Conflict | Cause | Solution |
|----------|-------|----------|
| dlib compilation | Missing build tools | Install Visual Studio Build Tools (Windows) |
| face_recognition import | Wrong Python environment | Activate virtual environment |
| CUDA conflicts | Multiple CUDA versions | Use conda environment or specify CUDA version |
| Path issues | Windows backslashes | Use forward slashes or os.path.join() |
