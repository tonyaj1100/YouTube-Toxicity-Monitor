# 🛡️ YouTube Toxicity Monitor (Automated AI Pipeline)

**Problem:** Viral videos often attract toxic comments, but manual moderation is too slow.
**Solution:** A real-time "Threat Monitor" that uses AI to detect hate speech spikes and alerts moderators instantly.

## 📸 The Command Center
![Dashboard](dashboard_main.jpg)
*Live Power BI Dashboard detecting toxic content and displaying dynamic thumbnails.*

## 🚀 How It Works (The Architecture)
1.  **Ingestion (Python):** Connects to YouTube Data API to fetch live comments.
2.  **Intelligence (NLP):** Uses `TextBlob` to calculate a "Toxicity Score" (-1 to 1).
3.  **Storage (Supabase):** Warehouses historical data in a PostgreSQL Cloud Database.
4.  **Automation (n8n):** A "Watchdog" workflow triggers Slack alerts 🚨 when Toxicity > 0.5.
5.  **Visualization (Power BI):** Dark-mode Ops Dashboard for strategic monitoring.

## 🛠️ Tech Stack
* **Python:** Pandas, TextBlob, Google Client API
* **Database:** Supabase (PostgreSQL)
* **Automation:** n8n (Workflow Orchestration)
* **Visualization:** Microsoft Power BI (DAX, UI Design)

## 🧠 The Automation Flow (n8n)
![n8n Workflow](automation_flow.jpg)
*This workflow runs every hour, checks the database for high-risk scores, and sends a Slack alert.*

## 💻 The Code Logic
![Python Code](python_script.jpg)

## 💡 Key Insight
**"The Toxicity Lag":** My analysis found that views often spike 2-3 hours *before* the negative sentiment floods in. This tool catches that leading edge.
