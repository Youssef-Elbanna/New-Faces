# Entity Relationship Diagram (ERD) - NewsFaces System

## 1. Database Schema Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE SCHEMA                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  Articles   │  │   Images    │  │ Known Faces │  │  Face       │      │
│  │   Table     │  │   Table     │  │   Table     │  │ Recognition │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  │  History    │      │
│                                                     │   Table     │      │
│                                                     └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2. Detailed Entity Relationships

### Articles Table
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ARTICLES                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  PK: article_id (INTEGER, AUTO_INCREMENT)                                  │
│  title (TEXT)                                                              │
│  target_uri (TEXT)                                                         │
│  language (TEXT)                                                            │
│  cleaned_text (TEXT)                                                        │
│  sentiment_label (TEXT)                                                     │
│  sentiment_score (REAL)                                                     │
│  topic_category (TEXT)                                                      │
│  created_at (TIMESTAMP)                                                     │
│  updated_at (TIMESTAMP)                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Images Table
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              IMAGES                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  PK: id (INTEGER, AUTO_INCREMENT)                                          │
│  FK: article_id (INTEGER) → Articles.article_id                            │
│  image_path (TEXT)                                                         │
│  image_url (TEXT)                                                          │
│  image_alt_text (TEXT)                                                     │
│  image_caption (TEXT)                                                      │
│  face_count (INTEGER)                                                      │
│  detected_faces (TEXT) - JSON array                                        │
│  created_at (TIMESTAMP)                                                    │
│  updated_at (TIMESTAMP)                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Known_Faces Table
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            KNOWN_FACES                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  PK: id (INTEGER, AUTO_INCREMENT)                                          │
│  name (TEXT)                                                               │
│  encoding (TEXT) - JSON array of 128 floats                               │
│  source_image (TEXT)                                                       │
│  confidence_score (REAL)                                                   │
│  created_at (TIMESTAMP)                                                    │
│  updated_at (TIMESTAMP)                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Face_Recognition_History Table
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FACE_RECOGNITION_HISTORY                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  PK: id (INTEGER, AUTO_INCREMENT)                                          │
│  FK: image_id (INTEGER) → Images.id                                        │
│  FK: face_id (INTEGER) → Known_Faces.id                                    │
│  confidence_score (REAL)                                                   │
│  recognition_time (TIMESTAMP)                                              │
│  processing_duration (REAL)                                                │
│  algorithm_version (TEXT)                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 3. Entity Relationship Mapping

### One-to-Many Relationships
```
Articles (1) ──────── (N) Images
     │                        │
     │                        │
     │                        ▼
     │                 Face_Recognition_History
     │                        │
     │                        │
     ▼                        │
Known_Faces (1) ──────── (N) Face_Recognition_History
```

### Relationship Details

#### Articles → Images (1:N)
- **Cardinality**: One article can have multiple images
- **Foreign Key**: `Images.article_id` references `Articles.article_id`
- **Cascade**: Delete images when article is deleted

#### Images → Face_Recognition_History (1:N)
- **Cardinality**: One image can have multiple face recognition results
- **Foreign Key**: `Face_Recognition_History.image_id` references `Images.id`
- **Purpose**: Track recognition attempts and results

#### Known_Faces → Face_Recognition_History (1:N)
- **Cardinality**: One known face can be recognized multiple times
- **Foreign Key**: `Face_Recognition_History.face_id` references `Known_Faces.id`
- **Purpose**: Track recognition performance and history

## 4. Database Constraints

### Primary Keys
- **Articles**: `article_id` (AUTO_INCREMENT)
- **Images**: `id` (AUTO_INCREMENT)
- **Known_Faces**: `id` (AUTO_INCREMENT)
- **Face_Recognition_History**: `id` (AUTO_INCREMENT)

### Foreign Keys
```sql
-- Images table
FOREIGN KEY (article_id) REFERENCES Articles(article_id) ON DELETE CASCADE

-- Face_Recognition_History table
FOREIGN KEY (image_id) REFERENCES Images(id) ON DELETE CASCADE
FOREIGN KEY (face_id) REFERENCES Known_Faces(id) ON DELETE CASCADE
```

### Unique Constraints
```sql
-- Articles table
UNIQUE (target_uri)

-- Known_Faces table
UNIQUE (name, source_image)
```

### Check Constraints
```sql
-- Images table
CHECK (face_count >= 0)
CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0)

-- Face_Recognition_History table
CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0)
CHECK (processing_duration >= 0.0)
```

## 5. Indexes for Performance

### Primary Indexes
```sql
-- Articles table
CREATE INDEX idx_articles_title ON Articles(title);
CREATE INDEX idx_articles_language ON Articles(language);
CREATE INDEX idx_articles_category ON Articles(topic_category);
CREATE INDEX idx_articles_sentiment ON Articles(sentiment_label);

-- Images table
CREATE INDEX idx_images_article_id ON Images(article_id);
CREATE INDEX idx_images_face_count ON Images(face_count);

-- Known_Faces table
CREATE INDEX idx_known_faces_name ON Known_Faces(name);

-- Face_Recognition_History table
CREATE INDEX idx_face_history_image_id ON Face_Recognition_History(image_id);
CREATE INDEX idx_face_history_face_id ON Face_Recognition_History(face_id);
CREATE INDEX idx_face_history_confidence ON Face_Recognition_History(confidence_score);
```

## 6. Data Types and Sizes

### Text Fields
- **TITLE**: Maximum 1000 characters
- **TARGET_URI**: Maximum 500 characters
- **LANGUAGE**: Maximum 10 characters
- **CLEANED_TEXT**: Maximum 50,000 characters
- **TOPIC_CATEGORY**: Maximum 100 characters

### Numeric Fields
- **SENTIMENT_SCORE**: REAL (-1.0 to 1.0)
- **CONFIDENCE_SCORE**: REAL (0.0 to 1.0)
- **FACE_COUNT**: INTEGER (0 to 100)
- **PROCESSING_DURATION**: REAL (seconds)

### JSON Fields
- **DETECTED_FACES**: Array of face objects
- **ENCODING**: Array of 128 float values

## 7. Sample Data Relationships

### Example Article with Images
```sql
-- Article
INSERT INTO Articles (article_id, title, target_uri) 
VALUES (1, 'Aaron Peirsol Olympic Champion', 'https://en.wikipedia.org/wiki/Aaron_Peirsol');

-- Related Images
INSERT INTO Images (id, article_id, image_path, face_count) 
VALUES 
(1, 1, 'data/extracted_data/images/aaron_peirsol_1.jpg', 1),
(2, 1, 'data/extracted_data/images/aaron_peirsol_2.jpg', 1);

-- Known Face
INSERT INTO Known_Faces (id, name, encoding) 
VALUES (1, 'Aaron Peirsol', '[0.123, 0.456, ...]');

-- Recognition History
INSERT INTO Face_Recognition_History (image_id, face_id, confidence_score) 
VALUES (1, 1, 0.95);
```

## 8. Database Maintenance

### Regular Operations
- **Backup**: Daily database backup
- **Cleanup**: Remove orphaned records monthly
- **Optimization**: VACUUM and ANALYZE weekly
- **Monitoring**: Track table sizes and performance

### Data Retention
- **Articles**: Keep indefinitely
- **Images**: Keep indefinitely
- **Known_Faces**: Keep indefinitely
- **Face_Recognition_History**: Keep for 2 years
