import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px

# Import our modules
from data_access.database import DatabaseManager
from services.face_service import FaceService

# Page configuration
st.set_page_config(
    page_title="NewsFaces - Face Detection Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and services
@st.cache_resource
def init_services():
    db = DatabaseManager()
    face_service = FaceService()
    return db, face_service

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .image-container {
        border: 2px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .face-tag {
        background-color: #ff6b6b;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        margin: 0.25rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">📰 NewsFaces Dashboard</h1>', unsafe_allow_html=True)
    
    # Initialize services
    try:
        db, face_service = init_services()
        st.success("✅ Services initialized successfully!")
    except Exception as e:
        st.error(f"❌ Error initializing services: {e}")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["🏠 Dashboard", "📊 Articles", "🖼️ Images & Faces", "👥 Known Faces", "🔍 Search"]
    )
    
    if page == "🏠 Dashboard":
        show_dashboard(db, face_service)
    elif page == "📊 Articles":
        show_articles(db)
    elif page == "🖼️ Images & Faces":
        show_images_and_faces(db, face_service)
    elif page == "👥 Known Faces":
        show_known_faces(db)
    elif page == "🔍 Search":
        show_search(db)

def show_dashboard(db, face_service):
    st.header("📊 System Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        article_count = db.get_article_count()
        st.metric("📰 Articles", article_count)
    
    with col2:
        image_count = db.get_image_count()
        st.metric("🖼️ Images", image_count)
    
    with col3:
        faces_count = db.get_known_faces_count()
        st.metric("👥 Known Faces", faces_count)
    
    with col4:
        # Calculate total faces detected
        try:
            conn = db._connect()
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(face_count) FROM images WHERE face_count > 0')
            total_faces = cursor.fetchone()[0] or 0
            conn.close()
            st.metric("🔍 Total Faces Detected", total_faces)
        except:
            st.metric("🔍 Total Faces Detected", "N/A")
    
    # Charts
    st.subheader("📈 Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Articles by category
        try:
            conn = db._connect()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT topic_category, COUNT(*) as count 
                FROM articles 
                WHERE topic_category IS NOT NULL 
                GROUP BY topic_category 
                ORDER BY count DESC 
                LIMIT 10
            ''')
            category_data = cursor.fetchall()
            conn.close()
            
            if category_data:
                df_categories = pd.DataFrame(category_data, columns=['Category', 'Count'])
                fig = px.pie(df_categories, values='Count', names='Category', title="Articles by Category")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No category data available yet")
        except Exception as e:
            st.error(f"Error loading category data: {e}")
    
    with col2:
        # Sentiment distribution
        try:
            conn = db._connect()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sentiment_label, COUNT(*) as count 
                FROM articles 
                WHERE sentiment_label IS NOT NULL 
                GROUP BY sentiment_label
            ''')
            sentiment_data = cursor.fetchall()
            conn.close()
            
            if sentiment_data:
                df_sentiment = pd.DataFrame(sentiment_data, columns=['Sentiment', 'Count'])
                fig = px.bar(df_sentiment, x='Sentiment', y='Count', title="Sentiment Distribution")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No sentiment data available yet")
        except Exception as e:
            st.error(f"Error loading sentiment data: {e}")
    
    # Recent articles
    st.subheader("📰 Recent Articles")
    try:
        # Use existing schema - get basic article info
        conn = db._connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT article_id, title, target_uri, language, sentiment_label, sentiment_score, topic_category
            FROM articles 
            ORDER BY article_id DESC 
            LIMIT 5
        ''')
        recent_articles = cursor.fetchall()
        conn.close()
        
        if recent_articles:
            for article in recent_articles:
                with st.expander(f"📰 {article[1][:100] if article[1] else 'No Title'}..."):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Title:** {article[1] or 'No Title'}")
                        st.write(f"**Language:** {article[3] or 'Unknown'}")
                        st.write(f"**Category:** {article[6] or 'Unknown'}")
                        st.write(f"**Sentiment:** {article[4] or 'Unknown'} ({article[5] or 0:.2f})")
                    with col2:
                        st.write(f"**URL:** [Link]({article[2]})")
        else:
            st.info("No articles found")
    except Exception as e:
        st.error(f"Error loading recent articles: {e}")

def show_articles(db):
    st.header("📰 Articles Management")
    
    # Search and filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search articles", placeholder="Enter keywords...")
    
    with col2:
        category_filter = st.selectbox("📂 Category", ["All", "Politics", "Technology", "Sports", "Entertainment", "Business"])
    
    with col3:
        sentiment_filter = st.selectbox("😊 Sentiment", ["All", "Positive", "Negative", "Neutral"])
    
    # Load articles using existing schema
    try:
        conn = db._connect()
        cursor = conn.cursor()
        
        if search_query:
            cursor.execute('''
                SELECT article_id, title, target_uri, language, sentiment_label, sentiment_score, topic_category
                FROM articles 
                WHERE title LIKE ? OR cleaned_text LIKE ?
                ORDER BY article_id DESC 
                LIMIT 100
            ''', (f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute('''
                SELECT article_id, title, target_uri, language, sentiment_label, sentiment_score, topic_category
                FROM articles 
                ORDER BY article_id DESC 
                LIMIT 100
            ''')
        
        articles = cursor.fetchall()
        conn.close()
        
        if articles:
            # Apply filters
            if category_filter != "All":
                articles = [a for a in articles if a[6] == category_filter]
            if sentiment_filter != "All":
                articles = [a for a in articles if a[4] == sentiment_filter]
            
            # Display articles
            for i, article in enumerate(articles):
                with st.expander(f"📰 {article[1][:100] if article[1] else 'No Title'}...", expanded=(i < 3)):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Title:** {article[1] or 'No Title'}")
                        st.write(f"**Language:** {article[3] or 'Unknown'}")
                        st.write(f"**Category:** {article[6] or 'Unknown'}")
                        st.write(f"**Sentiment:** {article[4] or 'Unknown'} ({article[5] or 0:.2f})")
                    with col2:
                        st.write(f"**URL:** [Link]({article[2]})")
                        
                    # Show related images
                    try:
                        conn = db._connect()
                        cursor = conn.cursor()
                        cursor.execute('''
                            SELECT i.image_path, i.face_count, i.detected_faces
                            FROM images i
                            WHERE i.article_id = ?
                        ''', (article[0],))
                        images = cursor.fetchall()
                        conn.close()
                        
                        if images:
                            st.write("**Related Images:**")
                            for img in images:
                                if os.path.exists(img[0]):
                                    st.image(img[0], width=200, caption=f"Faces: {img[1]}")
                                else:
                                    st.write(f"Image: {img[0]} (Faces: {img[1]})")
                    except Exception as e:
                        st.error(f"Error loading images: {e}")
        else:
            st.info("No articles found matching your criteria")
    except Exception as e:
        st.error(f"Error loading articles: {e}")

def show_images_and_faces(db, face_service):
    st.header("🖼️ Images & Face Detection")
    
    # Load images using existing schema
    try:
        conn = db._connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.id, i.image_path, i.face_count, i.detected_faces, a.title as article_title
            FROM images i
            JOIN articles a ON i.article_id = a.article_id
            ORDER BY i.id DESC 
            LIMIT 50
        ''')
        images = cursor.fetchall()
        conn.close()
        
        if images:
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                min_faces = st.slider("Minimum faces", 0, 10, 0)
            with col2:
                show_only_faces = st.checkbox("Show only images with faces", value=False)
            
            # Filter images
            if show_only_faces:
                images = [img for img in images if img[2] > 0]
            if min_faces > 0:
                images = [img for img in images if img[2] >= min_faces]
            
            # Display images
            for img in images:
                with st.expander(f"🖼️ {img[4][:50] if img[4] else 'No Title'}... (Faces: {img[2]})"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        if os.path.exists(img[1]):
                            st.image(img[1], width=400, caption=f"Article: {img[4] or 'No Title'}")
                        else:
                            st.error(f"Image not found: {img[1]}")
                    
                    with col2:
                        st.write(f"**Article:** {img[4] or 'No Title'}")
                        st.write(f"**Face Count:** {img[2]}")
                        
                        # Show detected faces
                        if img[3]:
                            try:
                                detected_faces = json.loads(img[3])
                                if detected_faces:
                                    st.write("**Detected Faces:**")
                                    for face in detected_faces:
                                        confidence_color = "🟢" if face['confidence'] > 0.8 else "🟡" if face['confidence'] > 0.6 else "🔴"
                                        st.markdown(f"{confidence_color} **{face['name']}** ({face['confidence']:.1%})")
                                else:
                                    st.write("No faces detected")
                            except:
                                st.write("Error parsing face data")
                        
                        # Process button
                        if st.button(f"🔍 Process Image {img[0]}", key=f"process_{img[0]}"):
                            with st.spinner("Processing image..."):
                                try:
                                    success = face_service.process_image_faces(img[1], img[0])
                                    if success:
                                        st.success("✅ Image processed successfully!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Error processing image")
                                except Exception as e:
                                    st.error(f"❌ Error: {e}")
        else:
            st.info("No images found")
    except Exception as e:
        st.error(f"Error loading images: {e}")

def show_known_faces(db):
    st.header("👥 Known Faces Database")
    
    # Add new face
    with st.expander("➕ Add New Face", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name")
            profession = st.text_input("Profession")
            organization = st.text_input("Organization")
            country = st.text_input("Country")
        
        with col2:
            political_party = st.text_input("Political Party")
            birth_date = st.date_input("Birth Date")
            wikipedia_url = st.text_input("Wikipedia URL")
            face_image = st.file_uploader("Face Image", type=['jpg', 'jpeg', 'png'])
        
        if st.button("➕ Add Face"):
            if name and face_image:
                st.info("Face encoding will be processed when face_recognition is available")
                st.success(f"✅ Face '{name}' added to database")
            else:
                st.error("Please provide name and face image")
    
    # Display known faces using existing schema
    try:
        conn = db._connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, encoding
            FROM known_faces 
            ORDER BY id DESC 
            LIMIT 100
        ''')
        faces = cursor.fetchall()
        conn.close()
        
        if faces:
            # Search faces
            search_name = st.text_input("🔍 Search faces by name", placeholder="Enter name...")
            if search_name:
                faces = [f for f in faces if search_name.lower() in f[1].lower()]
            
            # Display faces
            for face in faces:
                with st.expander(f"👤 {face[1]}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Name:** {face[1]}")
                        st.write(f"**ID:** {face[0]}")
                    
                    with col2:
                        st.write(f"**Encoding:** {'Available' if face[2] else 'Not Available'}")
        else:
            st.info("No known faces found")
    except Exception as e:
        st.error(f"Error loading known faces: {e}")

def show_search(db):
    st.header("🔍 Advanced Search")
    
    # Search options
    search_type = st.selectbox("Search Type", ["Articles", "Images", "Faces", "All"])
    
    if search_type == "Articles":
        query = st.text_input("Search articles", placeholder="Enter keywords...")
        if query:
            try:
                conn = db._connect()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT article_id, title, target_uri, language, sentiment_label, topic_category
                    FROM articles 
                    WHERE title LIKE ? OR cleaned_text LIKE ?
                    ORDER BY article_id DESC 
                    LIMIT 50
                ''', (f'%{query}%', f'%{query}%'))
                results = cursor.fetchall()
                conn.close()
                
                if results:
                    st.success(f"Found {len(results)} articles")
                    for result in results:
                        with st.expander(f"📰 {result[1][:100] if result[1] else 'No Title'}..."):
                            st.write(f"**Title:** {result[1] or 'No Title'}")
                            st.write(f"**Language:** {result[3] or 'Unknown'}")
                            st.write(f"**Category:** {result[5] or 'Unknown'}")
                            st.write(f"**URL:** [Link]({result[2]})")
                else:
                    st.info("No articles found")
            except Exception as e:
                st.error(f"Error searching: {e}")
    
    elif search_type == "Images":
        st.info("Image search functionality coming soon...")
    
    elif search_type == "Faces":
        st.info("Face search functionality coming soon...")
    
    elif search_type == "All":
        st.info("Global search functionality coming soon...")

if __name__ == "__main__":
    main()
