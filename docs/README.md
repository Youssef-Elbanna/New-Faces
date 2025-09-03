# NewsFaces - News Article Face Detection System

A comprehensive system for processing WARC files, extracting news articles and images, and detecting faces using AI.

## 🏗️ Project Structure

```
newsfaces_project/
├── src/                   # Core application source code
│   ├── core/             # Core processing modules
│   ├── services/         # Business logic services
│   ├── phases/           # Processing pipeline phases
│   ├── data_access/      # Database and file management
│   └── utils/            # Utility functions
├── apps/                  # User-facing applications
│   ├── streamlit_app_simple.py # Streamlit dashboard
│   └── run_streamlit.py  # Dashboard launcher
├── scripts/               # Utility and startup scripts
│   └── start_project.py  # Main startup script
├── docs/                  # Documentation
│   └── README.md         # This file
├── notebooks/             # Jupyter notebooks
│   └── main.ipynb        # Development notebook
├── config/                # Configuration files
├── data/                  # Data storage
├── logs/                  # Application logs
├── main.py               # Main pipeline entry point
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
python scripts/start_project.py
```
Then choose option 2, or manually:
```bash
streamlit run apps/streamlit_app_simple.py
```

## 📊 What Each Component Does

### **Core Modules (`src/core/`)**
- **`face_processing.py`**: Face detection, encoding, and recognition
- **`text_processing.py`**: Text cleaning, language detection, sentiment analysis
- **`warc_processing.py`**: HTML parsing and image URL extraction

### **Services (`src/services/`)**
- **`face_service.py`**: Orchestrates face detection workflow
- **`text_service.py`**: Manages text processing pipeline
- **`warc_service.py`**: Handles WARC file processing

### **Phases (`src/phases/`)**
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

- **Face Recognition**: Currently using mock processor due to dlib installation issues
- **WARC Files**: Large files (several GB each) - download may take time
- **Database**: Uses simple schema compatible with current data

## 🆘 Troubleshooting

- **Missing modules**: Run `pip install -r requirements.txt`
- **Database errors**: Check if `data/database/newsfaces.db` exists
- **WARC download issues**: Check internet connection and disk space
- **Face recognition errors**: Install dlib and face_recognition packages
