# NewsFaces Project - Data Sources & Update Guide

## 📍 **Current Data Sources & Paths**

### **1. WARC Files (Web Archives)**
**Location**: `data/extracted_data/`
**Source**: CommonCrawl web archive (https://data.commoncrawl.org/)

**Current Files**:
- `CC-MAIN-20230320083513-20230320113513-00000.warc.gz` (730MB)
- `CC-MAIN-20230320083513-20230320113513-00001.warc.gz` (1.1GB)
- `CC-MAIN-20230320083513-20230320113513-00002.warc.gz` (1.1GB)
- `CC-MAIN-20230320083513-20230320113513-00003.warc.gz` (365MB)
- `CC-MAIN-20230320083513-20230320113513-00004.warc.gz` (583MB)

**Total Size**: ~4GB of web archive data

### **2. Extracted HTML Content**
**Location**: `data/extracted_data/html/`
**Source**: Parsed from WARC files
**Current Files**: 7 HTML files extracted from web pages

### **3. Downloaded Images**
**Location**: `data/extracted_data/images/`
**Source**: Extracted from HTML content in WARC files
**Current Files**: 9 images from various web pages

### **4. Database**
**Location**: `data/database/bibliotheca_alexandrina.db`
**Content**: 7 articles, 9 images with metadata

### **5. Configuration**
**Location**: `config/settings.py`
**Key Settings**:
```python
COMMON_CRAWL_INDEX = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2023-14/warc.paths.gz"
MAX_WARC_FILES = 10
MAX_HTML_PAGES = 12
MAX_IMAGES_PER_PAGE = 5
```

## 🔄 **How to Update/Refresh Data**

### **Option 1: Download New WARC Files**
```bash
# 1. Update the CommonCrawl index in config/settings.py
# Change to a newer crawl:
COMMON_CRAWL_INDEX = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2024-XX/warc.paths.gz"

# 2. Clear existing data
rm -rf data/extracted_data/*.warc.gz
rm -rf data/extracted_data/html/*
rm -rf data/extracted_data/images/*
rm data/extracted_data/mappings.json

# 3. Run Phase 1 to download new data
python -c "from src.phases.phase1 import run_phase1; run_phase1()"
```

### **Option 2: Use Different WARC Files**
```bash
# 1. Download specific WARC files manually
# Visit: https://data.commoncrawl.org/
# Download files you want to analyze

# 2. Place them in data/extracted_data/
# 3. Update mappings.json manually or regenerate it
python create_mappings.py  # (if you have this script)
```

### **Option 3: Add Your Own Data**
```bash
# 1. Add your HTML files to data/extracted_data/html/
# 2. Add your images to data/extracted_data/images/
# 3. Update mappings.json to include your files
# 4. Run Phase 2 to process your data
python -c "from src.services.text_service import TextService; service = TextService(); service.process_html_files()"
```

## 📊 **Data Processing Pipeline**

### **Phase 1: WARC Processing**
- **Input**: WARC files from CommonCrawl
- **Output**: HTML files + downloaded images
- **Files Created**: `mappings.json`

### **Phase 2: Text Analysis**
- **Input**: HTML files + mappings.json
- **Output**: Articles in database
- **Process**: Text extraction, sentiment analysis, entity recognition

### **Phase 3: Face Enrollment**
- **Input**: LFW dataset (if available)
- **Output**: Known faces in database
- **Process**: Face encoding and storage

### **Phase 4: Face Detection**
- **Input**: Images from database
- **Output**: Face detection results
- **Process**: Detect and recognize faces in images

## 🎯 **Quick Data Update Commands**

### **Refresh Everything (New WARC Data)**
```bash
# Clear all extracted data
rm -rf data/extracted_data/html/* data/extracted_data/images/* data/extracted_data/*.warc.gz data/extracted_data/mappings.json

# Clear database
rm data/database/bibliotheca_alexandrina.db

# Run complete pipeline
python main.py
```

### **Keep WARC Files, Refresh Processing**
```bash
# Keep WARC files, clear processed data
rm -rf data/extracted_data/html/* data/extracted_data/images/* data/extracted_data/mappings.json

# Regenerate mappings and reprocess
python create_mappings.py
python -c "from src.services.text_service import TextService; service = TextService(); service.process_html_files()"
```

### **Add New Images Only**
```bash
# Add new images to data/extracted_data/images/
# Update mappings.json manually
# Run Phase 2 to process new images
python -c "from src.services.text_service import TextService; service = TextService(); service.process_html_files()"
```

## 📁 **File Structure for Updates**

```
data/
├── extracted_data/
│   ├── *.warc.gz          # WARC archive files (source data)
│   ├── html/              # Extracted HTML content
│   ├── images/            # Downloaded images
│   └── mappings.json      # Mapping between HTML and images
├── database/
│   └── bibliotheca_alexandrina.db  # SQLite database
└── warc_files/            # Additional WARC storage
```

## ⚠️ **Important Notes**

1. **WARC files are large** (100MB-1GB+ each)
2. **Processing takes time** - be patient
3. **Database is automatically created** - don't delete manually
4. **Images are linked to articles** - keep mappings.json in sync
5. **Backup your data** before major updates

## 🚀 **Recommended Update Strategy**

1. **Start small**: Use 2-3 WARC files initially
2. **Test processing**: Ensure pipeline works with new data
3. **Scale up**: Add more files as needed
4. **Monitor resources**: Check disk space and memory usage
5. **Keep backups**: Save working configurations

---

**Need help?** Check the logs in `logs/newsfaces.log` for detailed processing information!
