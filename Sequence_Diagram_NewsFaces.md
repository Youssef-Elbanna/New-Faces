# Sequence Diagram - NewsFaces System

## 1. Main System Initialization Sequence

```
User                    Dashboard           FaceService         Database
 |                          |                    |                |
 |-- Start Streamlit ------>|                    |                |
 |                          |-- Initialize ----->|                |
 |                          |                    |-- Connect ---->|
 |                          |                    |<-- Connected --|
 |                          |<-- Ready ----------|                |
 |<-- Dashboard Ready ------|                    |                |
```

## 2. Face Recognition Pipeline Sequence

```
User                    Dashboard           FaceService         FaceProcessor    Database
 |                          |                    |                    |                |
 |-- Upload Image --------->|                    |                    |                |
 |                          |-- Process Image -->|                    |                |
 |                          |                    |-- Detect Faces --->|                |
 |                          |                    |                    |-- Load Image --|
 |                          |                    |                    |<-- Image Data -|
 |                          |                    |<-- Face Count -----|                |
 |                          |                    |-- Recognize ------>|                |
 |                          |                    |                    |-- Get Known ---|
 |                          |                    |                    |<-- Encodings --|
 |                          |                    |<-- Recognition ---|                |
 |                          |<-- Results --------|                    |                |
 |<-- Face Results ---------|                    |                    |                |
```

## 3. WARC Processing Sequence

```
User                    Dashboard           WARCService         FileManager      Database
 |                          |                    |                    |                |
 |-- Process WARC --------->|                    |                    |                |
 |                          |-- Extract WARC --->|                    |                |
 |                          |                    |-- Read Files ----->|                |
 |                          |                    |<-- File Data -----|                |
 |                          |                    |-- Parse HTML ----->|                |
 |                          |                    |<-- Content -------|                |
 |                          |                    |-- Save Images --->|                |
 |                          |                    |<-- Saved ---------|                |
 |                          |                    |-- Update DB ----->|                |
 |                          |                    |                    |-- Insert Data |
 |                          |                    |                    |<-- Success ----|
 |                          |<-- Complete -------|                    |                |
 |<-- WARC Processed ------|                    |                    |                |
```

## 4. Face Enrollment Sequence

```
User                    Dashboard           FaceService         FaceProcessor    Database
 |                          |                    |                    |                |
 |-- Enroll Faces --------->|                    |                    |                |
 |                          |-- Load LFW ------->|                    |                |
 |                          |                    |-- Extract Dataset>|                |
 |                          |                    |<-- Dataset -------|                |
 |                          |                    |-- Process Images->|                |
 |                          |                    |                    |-- Store Encodings
 |                          |                    |<-- Encodings -----|                |
 |                          |<-- Enrollment -----|                    |                |
 |<-- Faces Enrolled ------|                    |                    |                |
```

## 5. Article Analysis Sequence

```
User                    Dashboard           TextService         TextProcessor    Database
 |                          |                    |                    |                |
 |-- Analyze Articles ----->|                    |                    |                |
 |                          |-- Process Text --->|                    |                |
 |                          |                    |-- Load Articles -->|                |
 |                          |                    |                    |-- Get Text ----|
 |                          |                    |                    |<-- Article ----|
 |                          |                    |<-- Text Data -----|                |
 |                          |                    |-- Sentiment ----->|                |
 |                          |                    |<-- Sentiment -----|                |
 |                          |                    |-- Entities ------>|                |
 |                          |                    |<-- Entities ------|                |
 |                          |                    |-- Update DB ----->|                |
 |                          |                    |                    |-- Save Results
 |                          |                    |                    |<-- Saved ------|
 |                          |<-- Analysis -------|                    |                |
 |<-- Analysis Complete ---|                    |                    |                |
```

## 6. Matrix Generation Sequence

```
User                    Dashboard           Analytics           FaceService      Database
 |                          |                    |                    |                |
 |-- Generate Matrices ---->|                    |                    |                |
 |                          |-- Create Matrices->|                    |                |
 |                          |                    |-- Get Face Data -->|                |
 |                          |                    |                    |-- Query Faces |
 |                          |                    |                    |<-- Face Data --|
 |                          |                    |<-- Encodings -----|                |
 |                          |                    |-- Calculate Dist->|                |
 |                          |                    |<-- Distances -----|                |
 |                          |                    |-- Generate Sim --->|                |
 |                          |                    |<-- Similarity ----|                |
 |                          |                    |-- Save JSON ----->|                |
 |                          |                    |<-- Saved ---------|                |
 |                          |<-- Matrices -------|                    |                |
 |<-- Matrices Ready ------|                    |                    |                |
```

## 7. Search and Query Sequence

```
User                    Dashboard           SearchService       Database
 |                          |                    |                |
 |-- Search Query --------->|                    |                |
 |                          |-- Process Query -->|                |
 |                          |                    |-- Execute Query->|
 |                          |                    |                    |-- Search DB --|
 |                          |                    |                    |<-- Results ---|
 |                          |                    |<-- Results ------|                |
 |                          |-- Format Results ->|                |
 |                          |<-- Formatted ------|                |
 |<-- Search Results ------|                    |                |
```

## 8. Error Handling Sequence

```
User                    Dashboard           Service             Database
 |                          |                    |                |
 |-- Request --------------->|                    |                |
 |                          |-- Process Request->|                |
 |                          |                    |-- Operation --->|
 |                          |                    |<-- Error -------|                |
 |                          |                    |-- Log Error --->|                |
 |                          |                    |<-- Logged ------|                |
 |                          |<-- Error ----------|                |
 |<-- Error Message --------|                    |                |
```

## Key Sequence Patterns

### Synchronous Operations
- Face detection and recognition
- Database queries and updates
- File system operations

### Asynchronous Operations
- WARC file processing
- Batch image processing
- Matrix generation

### Error Handling
- Graceful degradation
- User notification
- Logging and monitoring

### Performance Optimization
- Caching of frequent operations
- Batch processing where possible
- Database connection pooling
