# NewsFaces Project

## 🚀 Quick Start

```bash
# Start the project
python scripts/start_project.py

# Or run directly
python main.py                    # Run complete pipeline
streamlit run apps/streamlit_app_simple.py  # Launch dashboard
```

## 📁 Project Organization

- **`src/`** - Core application source code
- **`apps/`** - Streamlit dashboard and launcher
- **`scripts/`** - Utility and startup scripts
- **`docs/`** - Detailed documentation
- **`notebooks/`** - Jupyter notebooks for development
- **`config/`** - Configuration files
- **`data/`** - Data storage and database
- **`logs/** - Application logs

## 📖 Documentation

See `docs/README.md` for complete documentation.

## 🎯 What This Project Does

- Processes WARC files from CommonCrawl
- Extracts news articles and images
- Analyzes text (language, sentiment, entities)
- Detects faces in images
- Provides a Streamlit dashboard for exploration

## 🔧 Requirements

- Python 3.8+
- See `requirements.txt` for dependencies
- Virtual environment recommended (`.venv`)
