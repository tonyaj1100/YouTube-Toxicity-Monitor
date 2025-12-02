import os
import re
from googleapiclient.discovery import build
from textblob import TextBlob
from supabase import create_client
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# --- CONFIGURATION ---
# ⚠️ SECURITY WARNING: Never share these keys publicly in a real project.
YOUTUBE_API_KEY = "YOUR_KEY_HERE"
SUPABASE_URL = "hYOUR_URL_HERE"
SUPABASE_KEY = "YOUR_KEY_HERE" 

# --- SETUP ---
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def extract_video_id(url):
    """
    Extracts the Video ID from various YouTube URL formats.
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # 1. Handle 'youtu.be' short links
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    
    # 2. Handle 'youtube.com/watch?v=' links
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            p = parse_qs(parsed_url.query)
            return p['v'][0]
        if parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]
        if parsed_url.path[:8] == '/v/':
            return parsed_url.path.split('/')[2]
        # Handle Shorts
        if parsed_url.path[:8] == '/shorts/':
            return parsed_url.path.split('/')[2]

    # Return None if no ID found
    return None

def get_video_sentiment(video_id):
    print(f"🔄 Connecting to YouTube API for ID: {video_id}...")
    
    # 1. Get Video Stats
    try:
        stats_request = youtube.videos().list(part="snippet,statistics", id=video_id)
        stats_response = stats_request.execute()
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

    if not stats_response['items']: 
        return None
    
    item = stats_response['items'][0]
    title = item['snippet']['title']
    views = int(item['statistics']['viewCount'])
    comments_count = int(item['statistics'].get('commentCount', 0))
    
    # 2. Get Top Comments for Sentiment Analysis
    comments = []
    print("💬 Fetching comments...")
    try:
        comment_request = youtube.commentThreads().list(
            part="snippet", videoId=video_id, maxResults=20, textFormat="plainText"
        )
        comment_response = comment_request.execute()
        for item in comment_response['items']:
            text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(text)
    except:
        print("⚠️ Comments are disabled or unavailable.")
        pass 

    # 3. Calculate "Toxicity" (Negative Sentiment)
    print("🧠 Analyzing sentiment...")
    total_polarity = 0
    for comment in comments:
        analysis = TextBlob(comment)
        total_polarity += analysis.sentiment.polarity
    
    avg_polarity = total_polarity / len(comments) if comments else 0
    # Invert polarity: Lower polarity (-1) means High Toxicity (1)
    toxicity_score = round((1 - avg_polarity) / 2, 2) 

    return {
        "video_title": title,
        "video_id": video_id,
        "view_count": views,
        "comment_count": comments_count,
        "toxicity_score": toxicity_score,
        "upload_date": datetime.now().isoformat()
    }

# --- MAIN EXECUTION LOOP ---
while True:
    print("\n" + "="*40)
    print("   TUBEGUARD: THREAT MONITOR SYSTEM   ")
    print("="*40)
    user_input = input("👉 Paste YouTube URL (or type 'exit' to quit): ").strip()

    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    # Extract ID from URL
    video_id = extract_video_id(user_input)

    if video_id:
        data = get_video_sentiment(video_id)

        if data:
            print("\n📊 ANALYSIS RESULT:")
            print(f"   📺 Title:    {data['video_title']}")
            print(f"   👀 Views:    {data['view_count']}")
            print(f"   ☣️  Toxicity: {data['toxicity_score']} (0=Safe, 1=Toxic)")
            
            # Insert into Supabase
            try:
                data_save = supabase.table("video_stats").insert(data).execute()
                print("✅ Data saved to Supabase Database!")
                
                # OPTIONAL: Check if it's toxic and warn the user immediately
                if data['toxicity_score'] > 0.5:
                    print("⚠️ WARNING: High Toxicity Detected! Slack Alert Triggered (via n8n).")
                    
            except Exception as e:
                print(f"❌ Database Error: {e}")
        else:
            print("❌ Video details could not be found.")
    else:
        print("❌ Invalid YouTube URL. Please try again.")
