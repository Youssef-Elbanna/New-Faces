# NewsFaces Project - Setup Guide for Professors

## 🎯 Project Overview
NewsFaces is a research project that processes web archives (WARC files) to extract news articles and images, then analyzes text content and detects faces in images. It demonstrates advanced web scraping, data processing, and machine learning workflows.

## 🚀 Quick Start (Recommended)

### 1. Prerequisites
- **Python 3.8+** (tested with Python 3.11.9)
- **PyCharm** (Community or Professional)
- **8GB+ RAM** (for processing large WARC files)
- **10GB+ free disk space**

### 2. Installation Steps
```bash
# Clone the repository
git clone <repository-url>
cd NewsFaces-main

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# If you encounter issues with heavy ML packages, use basic requirements:
# pip install -r requirements-basic.txt
```

### 3. Run the Project
```bash
# Option 1: Interactive startup script
python scripts/start_project.py

# Option 2: Direct Streamlit dashboard
streamlit run apps/streamlit_app_simple.py

# Option 3: Complete pipeline
python main.py
```

## 📊 What You'll See

### Streamlit Dashboard
- **Dashboard**: Overview of extracted articles and images
- **Articles**: Browse and search through extracted news content
- **Images & Faces**: View images with face detection results
- **Known Faces**: Database of recognized individuals
- **Search**: Advanced search across all data

### Data Processing
- **Phase 1**: Downloads and processes WARC files from CommonCrawl
- **Phase 2**: Extracts text metadata and analyzes content
- **Phase 3**: Enrolls known faces from datasets
- **Phase 4**: Detects and recognizes faces in images

## ⚠️ Common Issues & Solutions

### 1. Import Errors
```bash
# Run from project root directory
cd NewsFaces-main
python -c "import sys; print(sys.path)"
```

### 2. Missing Dependencies
```bash
# Install missing packages individually
pip install <package-name>

# Or reinstall all requirements
pip install -r requirements.txt --force-reinstall
```

### 3. PyTorch Installation Issues
```bash
# Use CPU-only version (recommended)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 4. Memory Issues
- Use smaller WARC files
- Reduce `MAX_WARC_FILES` in `config/settings.py`
- Process data in smaller batches

## 🔧 Configuration Options

### Edit `config/settings.py`
```python
MAX_WARC_FILES = 5        # Reduce for faster processing
MAX_HTML_PAGES = 10       # Limit HTML pages processed
MAX_IMAGES_PER_PAGE = 3   # Limit images per page
```

### Database Settings
- Database file: `data/database/bibliotheca_alexandrina.db`
- Tables: articles, images, known_faces, news_sources
- Schema: Automatically created on first run

## 📁 Project Structure
```
NewsFaces-main/
├── apps/                  # Streamlit applications
├── config/               # Configuration files
├── data/                 # Data storage
│   ├── database/        # SQLite database
│   ├── extracted_data/  # Processed HTML and images
│   └── warc_files/      # Downloaded WARC files
├── src/                  # Source code
│   ├── phases/          # Processing pipeline phases
│   ├── services/        # Business logic services
│   └── data_access/     # Database and file operations
├── scripts/              # Utility scripts
└── requirements.txt      # Dependencies
```

## 🎓 Academic Use Cases

### Research Applications
- **Web Archive Analysis**: Study historical web content
- **News Media Research**: Analyze article patterns and sentiment
- **Face Recognition**: Research in computer vision and privacy
- **Data Mining**: Large-scale web content extraction

### Teaching Applications
- **Web Scraping**: Demonstrate modern web data extraction
- **Database Design**: Show relational database implementation
- **API Development**: RESTful services and data processing
- **Machine Learning**: Integration of ML in data pipelines

## 📚 Additional Resources

### Documentation
- `docs/README.md` - Detailed project documentation
- `notebooks/main.ipynb` - Jupyter notebook examples

### Sample Data
- Pre-extracted data available in `data/extracted_data/`
- Sample database with working examples
- Mock implementations for demonstration

### Support
- Check logs in `logs/newsfaces.log`
- Use mock implementations if ML packages fail
- Project gracefully degrades functionality

## 🏆 Success Metrics
- ✅ Dashboard loads with sample data
- ✅ Images display correctly
- ✅ Database shows real extracted content
- ✅ Face detection works (mock or real)
- ✅ Text analysis processes articles

## 💡 Tips for Professors
1. **Start with the dashboard** - easiest way to see results
2. **Use existing data** - don't re-process WARC files initially
3. **Check logs** - detailed information about any issues
4. **Gradual complexity** - start basic, add ML features later
5. **Student projects** - great base for web scraping assignments

---

**Happy Researching! 🚀**

If you encounter any issues, the project includes comprehensive error handling and will use mock implementations when advanced features aren't available.
