# Architecture Diagram - NewsFaces System

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Dashboard     │  │   Analytics     │  │   Search        │ │
│  │   (Streamlit)   │  │   (Matrices)    │  │   Interface     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Face Service   │  │  Text Service   │  │  WARC Service   │ │
│  │  (Recognition)  │  │  (Analysis)     │  │  (Processing)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Phase Manager  │  │  Image Service  │  │  Search Service │ │
│  │  (Pipeline)     │  │  (Detection)    │  │  (Queries)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Face Processor  │  │ Text Processor  │  │ WARC Processor  │ │
│  │ (dlib/face_rec) │  │ (NLP/AI)        │  │ (warcio/bs4)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Image Processor │  │ Entity Extractor│  │ URL Downloader  │ │
│  │ (PIL/OpenCV)    │  │ (spaCy/NLTK)    │  │ (requests)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Database      │  │   File System   │  │   Cache         │ │
│  │   (SQLite)      │  │   (Local)       │  │   (Memory)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Articles      │  │     Images      │  │  Known Faces    │ │
│  │   Table         │  │     Table       │  │     Table       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INTEGRATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   WARC Files    │  │   LFW Dataset   │  │   Web Sources   │ │
│  │   (Input)       │  │   (Training)    │  │   (Scraping)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Presentation Layer
- **Dashboard**: Main Streamlit interface showing system overview
- **Analytics**: Face recognition matrices and performance metrics
- **Search**: Article and image search functionality

### 2. Application Layer
- **Face Service**: Manages face detection and recognition operations
- **Text Service**: Handles article processing and analysis
- **WARC Service**: Processes web archive files
- **Phase Manager**: Orchestrates the 4-phase pipeline
- **Image Service**: Manages image processing and storage
- **Search Service**: Handles database queries and search

### 3. Processing Layer
- **Face Processor**: Core face recognition using dlib/face_recognition
- **Text Processor**: NLP processing with transformers/spaCy
- **WARC Processor**: Web archive extraction with warcio/BeautifulSoup
- **Image Processor**: Image handling with PIL/OpenCV
- **Entity Extractor**: Named entity recognition and extraction
- **URL Downloader**: Web content fetching with requests

### 4. Data Layer
- **Database**: SQLite database with structured tables
- **File System**: Local storage for images and extracted content
- **Cache**: In-memory caching for performance
- **Tables**: Articles, Images, Known_Faces, and related metadata

### 5. Integration Layer
- **WARC Files**: Input web archive files
- **LFW Dataset**: Labeled Faces in the Wild for training
- **Web Sources**: External websites for content scraping

## Data Flow Architecture

```
WARC Files → WARC Service → Text/Image Extraction → Database
     ↓
LFW Dataset → Face Service → Face Encoding → Known_Faces Table
     ↓
New Images → Face Detection → Face Recognition → Results Update
     ↓
Dashboard ← Analytics ← Matrix Generation ← Performance Data
```

## Security Architecture

- **Authentication**: Streamlit session management
- **Data Privacy**: Local storage, no external data transmission
- **Access Control**: Role-based dashboard access
- **Audit Trail**: Logging of all system operations

## Scalability Considerations

- **Modular Design**: Independent services for easy scaling
- **Database Optimization**: Indexed queries for performance
- **Caching Strategy**: In-memory caching for frequent operations
- **Batch Processing**: Efficient handling of large datasets
