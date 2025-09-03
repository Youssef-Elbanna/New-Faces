# Data Flow Diagram - NewsFaces System

## 1. High-Level Data Flow Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Input     │    │  Process    │    │   Store     │    │   Output    │
│   Sources   │───▶│   Pipeline  │───▶│   Data      │───▶│   Results   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 2. Detailed Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INPUT DATA SOURCES                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   WARC      │  │     LFW     │  │  Wikipedia  │  │   Manual    │      │
│  │   Files     │  │   Dataset   │  │    Pages    │  │   Uploads   │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA EXTRACTION LAYER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   WARC      │  │   Image     │  │    Text     │  │    URL      │      │
│  │  Parser     │  │  Downloader │  │  Extractor  │  │  Fetcher    │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PROCESSING PIPELINE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Phase 1   │  │   Phase 2   │  │   Phase 3   │  │   Phase 4   │      │
│  │   WARC      │  │    Text     │  │    Face     │  │    Face     │      │
│  │ Processing  │  │  Analysis   │  │ Enrollment  │  │ Detection   │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA STORAGE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  Articles   │  │   Images    │  │ Known Faces │  │  Mappings   │      │
│  │   Table     │  │   Table     │  │   Table     │  │    JSON     │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ANALYTICS ENGINE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Face      │  │   Text      │  │   Image     │  │   System    │      │
│  │ Recognition │  │  Analytics  │  │  Analytics  │  │  Metrics    │      │
│  │ Matrices    │  │  (Sentiment)│  │ (Face Count)│  │ (Overview)  │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OUTPUT LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  Streamlit  │  │   Matrix    │  │   Search    │  │   Export    │      │
│  │  Dashboard  │  │   Files     │  │   Results   │  │   Reports   │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 3. Data Flow Details by Phase

### Phase 1: WARC Processing Data Flow
```
WARC Files → WARC Parser → HTML Content + Images → File System → Mappings.json
     ↓
Database ← Article Insertion ← Text Extraction ← HTML Parsing ← HTML Content
```

### Phase 2: Text Analysis Data Flow
```
Article Text → Text Processor → Sentiment Analysis → Entity Extraction → Database Update
     ↓
Topic Classification ← Content Analysis ← NLP Processing ← Cleaned Text
```

### Phase 3: Face Enrollment Data Flow
```
LFW Images → Face Processor → Face Encodings → Database Storage → Known Faces Table
     ↓
Encoding Validation ← Quality Check ← Face Detection ← Image Loading
```

### Phase 4: Face Detection Data Flow
```
New Images → Face Detection → Face Count → Face Recognition → Results Storage
     ↓
Database Update ← Confidence Scores ← Similarity Calculation ← Known Face Comparison
```

## 4. Data Transformation Flow

### Input Data Types
- **WARC Files**: Binary web archive format
- **Images**: JPG, PNG, JPEG formats
- **Text**: HTML, plain text content
- **URLs**: Web page references

### Processing Transformations
- **WARC → HTML**: Binary to text conversion
- **HTML → Clean Text**: Tag removal and content extraction
- **Images → Face Encodings**: 128-dimensional vectors
- **Text → Sentiment**: Numerical sentiment scores
- **Text → Entities**: Named entity recognition

### Output Data Types
- **Structured Data**: SQLite database records
- **Analytics**: JSON matrices and metrics
- **Visualizations**: Charts and heatmaps
- **Reports**: Formatted analysis results

## 5. Data Storage Flow

### Primary Storage
```
Raw Data → Processed Data → Structured Data → Analytics Data
   ↓           ↓              ↓              ↓
File System → Temp Storage → Database → JSON Files
```

### Data Persistence
- **File System**: Raw images and HTML files
- **Database**: Structured article and face data
- **JSON Files**: Analytics matrices and mappings
- **Cache**: In-memory processing data

## 6. Data Quality Flow

### Validation Steps
```
Input Data → Format Check → Content Validation → Quality Assessment → Storage
     ↓           ↓              ↓              ↓              ↓
   Raw Data → Valid Format → Valid Content → High Quality → Database
```

### Error Handling
- **Format Errors**: Invalid file types
- **Content Errors**: Corrupted or empty data
- **Quality Errors**: Low-resolution images, poor text
- **Processing Errors**: Algorithm failures

## 7. Performance Optimization Flow

### Caching Strategy
```
Frequent Data → Memory Cache → Fast Access → Reduced Processing Time
     ↓              ↓            ↓              ↓
Database → Cache Check → Cache Hit → Direct Return
```

### Batch Processing
```
Multiple Items → Batch Collection → Batch Processing → Batch Storage
     ↓              ↓              ↓              ↓
Queue → Buffer → Algorithm → Database
```

## 8. Security and Privacy Flow

### Data Protection
```
Input Data → Access Control → Processing → Secure Storage → Controlled Output
     ↓           ↓              ↓           ↓              ↓
   Raw Data → User Auth → Safe Processing → Encrypted → User Permissions
```

### Data Lifecycle
- **Collection**: Secure input handling
- **Processing**: Isolated processing environment
- **Storage**: Encrypted database storage
- **Access**: Role-based access control
- **Deletion**: Secure data removal
