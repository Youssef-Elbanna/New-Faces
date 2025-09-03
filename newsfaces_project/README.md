# NewsFaces - News Article Face Detection System

A comprehensive system for processing WARC files, extracting news articles and images, and detecting faces using AI.

## 🏗️ Project Structure

```
newsfaces_project/
├── config/                 # Configuration files
│   ├── __init__.py
│   └── settings.py        # Main configuration
├── core/                  # Core processing modules
│   ├── __init__.py
│   ├── face_processing.py # Face detection and recognition
│   ├── text_processing.py # Text analysis and metadata extraction
│   └── warc_processing.py # WARC file processing utilities
├── data_access/           # Database and file management
│   ├── __init__.py
│   ├── database.py        # Database operations
│   ├── file_manager.py    # File operations
│   └── warc_downloader.py # WARC file downloading
├── phases/                # Processing pipeline phases
│   ├── __init__.py
│   ├── phase1.py         # WARC processing and HTML extraction
│   ├── phase2.py         # Text processing and metadata
│   ├── phase3.py         # Face enrollment
│   └── phase4.py         # Face detection in images
├── services/              # Business logic services
│   ├── __init__.py
│   ├── face_service.py   # Face processing service
│   ├── text_service.py   # Text processing service
│   └── warc_service.py   # WARC processing service
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── logging_utils.py  # Logging configuration
├── data/                  # Data storage
│   ├── extracted_data/   # Extracted HTML and images
│   ├── database/         # SQLite database files
│   └── warc_files/       # Downloaded WARC files
├── logs/                  # Application logs
├── main.py               # Main pipeline entry point
├── main.ipynb            # Jupyter notebook for development
├── streamlit_app_simple.py # Streamlit dashboard (compatible with current DB)
├── run_streamlit.py      # Script to launch Streamlit app
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 2. Run the Complete Pipeline
```bash
python main.py
```
This will:
- Download WARC files from CommonCrawl
- Extract HTML content and images
- Process text (language, sentiment, entities)
- Detect faces in images
- Store everything in the database

### 3. Launch the Dashboard
```bash
python run_streamlit.py
```
Or manually:
```bash
streamlit run streamlit_app_simple.py
```

## 📊 What Each Component Does

### **Core Modules**
- **`face_processing.py`**: Face detection, encoding, and recognition
- **`text_processing.py`**: Text cleaning, language detection, sentiment analysis
- **`warc_processing.py`**: HTML parsing and image URL extraction

### **Services**
- **`face_service.py`**: Orchestrates face detection workflow
- **`text_service.py`**: Manages text processing pipeline
- **`warc_service.py`**: Handles WARC file processing

### **Phases**
- **Phase 1**: WARC processing and content extraction
- **Phase 2**: Text analysis and metadata generation
- **Phase 3**: Known face enrollment
- **Phase 4**: Face detection in extracted images

## 🔧 Configuration

Edit `config/settings.py` to adjust:
- `MAX_WARC_FILES`: Number of WARC files to process
- `MAX_HTML_PAGES`: Maximum HTML pages to extract
- `MAX_IMAGES_PER_PAGE`: Images per page limit
- `COMMON_CRAWL_INDEX`: WARC file source

## 📈 Dashboard Features

The Streamlit dashboard provides:
- **Dashboard**: System overview and statistics
- **Articles**: Browse and search processed articles
- **Images & Faces**: View images with face detection results
- **Known Faces**: Manage known face database
- **Search**: Advanced search across all data

## 🎯 Current Status

- ✅ **WARC Processing**: Fully functional
- ✅ **Text Analysis**: Language detection, sentiment, entities
- ✅ **Face Detection**: Mock processor (real recognition pending)
- ✅ **Database**: SQLite with current schema
- ✅ **Dashboard**: Streamlit interface working

## 🔮 Next Steps

1. **Install dlib and face_recognition** for real face recognition
2. **Process real WARC files** with `python main.py`
3. **Customize dashboard** as needed
4. **Add more known faces** to the database

## 📝 Notes

- **`streamlit_app.py`**: Enhanced version (requires enhanced DB schema)
- **`streamlit_app_simple.py`**: Compatible with current DB schema
- **Face Recognition**: Currently using mock processor due to dlib installation issues
- **WARC Files**: Large files (several GB each) - download may take time

## 🆘 Troubleshooting

- **Missing modules**: Run `pip install -r requirements.txt`
- **Database errors**: Check if `newsfaces.db` exists
- **WARC download issues**: Check internet connection and disk space
- **Face recognition errors**: Install dlib and face_recognition packages
