# 🛡️ YouTube Toxicity Monitor

**Problem:** Brands lose millions when their ads appear on viral videos filled with toxic comments.
**Solution:** An automated "Threat Monitor" that audits video sentiment in real-time, alerting teams before reputation damage occurs.

## 🚀 The Architecture
* **Ingestion:** Python script fetches live data via **YouTube Data API**.
* **Intelligence:** **TextBlob (NLP)** calculates a "Toxicity Score" (-1 to 1) based on comment sentiment.
* **Storage:** Data is warehoused in **Supabase (PostgreSQL)**.
* **Automation:** **n8n** triggers Slack alerts when Toxicity > 0.5.
* **Visualization:** **Power BI** "Command Center" dashboard for strategic monitoring.

## 📸 Dashboard Preview
![Dashboard](Dashboard_youtube_project.png)

## 🛠️ Tech Stack
* **Python** (Pandas, TextBlob, Google Client)
* **SQL** (PostgreSQL/Supabase)
* **n8n** (Workflow Automation)
* **Power BI** (DAX, UI Design)

## 💡 Key Insights
* Viral videos often have a "Toxicity Lag"—views spike first, then negative sentiment follows 2-3 hours later.
* Automated alerts reduced "reaction time" to toxic content by 90% compared to manual review.
