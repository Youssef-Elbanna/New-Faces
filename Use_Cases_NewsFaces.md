# Use Cases - NewsFaces System

## 1. Primary Use Cases

### UC-001: Process WARC Files
**Actor:** System Administrator  
**Precondition:** WARC files available in data directory  
**Main Flow:**
1. System loads WARC files from data/warc_files/
2. Extracts HTML content and images
3. Saves extracted data to data/extracted_data/
4. Generates mappings.json for content relationships
5. Updates database with extracted information

**Postcondition:** Articles and images are available for processing

### UC-002: Enroll Known Faces
**Actor:** System Administrator  
**Precondition:** LFW dataset available  
**Main Flow:**
1. System loads LFW dataset
2. Extracts face encodings from images
3. Stores encodings in known_faces table
4. Associates encodings with person names
5. Updates face recognition system

**Postcondition:** Face recognition system is trained and ready

### UC-003: Detect Faces in Images
**Actor:** System  
**Precondition:** Images available in database  
**Main Flow:**
1. System loads image from database
2. Applies face detection algorithm
3. Counts detected faces
4. Updates image record with face count
5. Stores face detection results

**Postcondition:** Face count and detection data updated

### UC-004: Recognize Faces
**Actor:** System  
**Precondition:** Face detection completed, known faces enrolled  
**Main Flow:**
1. System loads detected face encoding
2. Compares against known face encodings
3. Calculates similarity scores
4. Identifies best match
5. Updates database with recognition results

**Postcondition:** Face recognition results stored

### UC-005: Analyze Article Content
**Actor:** System  
**Precondition:** Article text extracted  
**Main Flow:**
1. System processes article text
2. Performs sentiment analysis
3. Extracts key entities (people, organizations, locations)
4. Categorizes content by topic
5. Stores analysis results in database

**Postcondition:** Article analysis complete

## 2. Secondary Use Cases

### UC-006: View Dashboard
**Actor:** Data Analyst  
**Precondition:** System running, data processed  
**Main Flow:**
1. User accesses Streamlit dashboard
2. Views system overview metrics
3. Navigates between different sections
4. Interacts with visualizations
5. Exports data if needed

**Postcondition:** User has comprehensive system view

### UC-007: Search Articles
**Actor:** Researcher  
**Precondition:** Articles available in database  
**Main Flow:**
1. User enters search query
2. System searches article titles and content
3. Applies filters (category, sentiment, language)
4. Displays matching results
5. Shows related images and faces

**Postcondition:** User finds relevant articles

### UC-008: View Face Recognition Analytics
**Actor:** Data Analyst  
**Precondition:** Face recognition matrices generated  
**Main Flow:**
1. User navigates to Analytics page
2. Views distance and similarity matrices
3. Analyzes recognition accuracy
4. Reviews threshold performance
5. Interprets heatmaps and charts

**Postcondition:** User understands system performance

### UC-009: Add New Face
**Actor:** System Administrator  
**Precondition:** Face image available  
**Main Flow:**
1. User uploads face image
2. System extracts face encoding
3. User provides person details
4. System stores encoding and metadata
5. Updates face recognition system

**Postcondition:** New face enrolled in system

### UC-010: Process Wikipedia Pages
**Actor:** System Administrator  
**Precondition:** Wikipedia URL provided  
**Main Flow:**
1. System fetches Wikipedia page
2. Downloads page images
3. Processes content through pipeline
4. Adds to database
5. Updates face recognition if faces found

**Postcondition:** Wikipedia content integrated into system

## 3. Exception Use Cases

### UC-011: Handle Face Detection Failure
**Actor:** System  
**Precondition:** Image processing attempted  
**Main Flow:**
1. System attempts face detection
2. Detection fails (no faces, poor quality)
3. System logs error
4. Updates database with face_count = 0
5. Continues with next image

**Postcondition:** System continues processing

### UC-012: Handle Database Connection Error
**Actor:** System  
**Precondition:** Database operation attempted  
**Main Flow:**
1. System attempts database connection
2. Connection fails
3. System logs error
4. Retries connection
5. Falls back to error handling

**Postcondition:** System handles error gracefully
