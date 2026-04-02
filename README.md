<h1 align="center">
  <img src="https://raw.githubusercontent.com/yogender-ai/NewsIntel/main/frontend/public/favicon.ico" width="40" alt="NewsIntel Icon" valign="middle" /> 
  News Intelligence Platform
</h1>

<p align="center">
  <strong>A premium, real-time AI-powered news curation and NLP intelligence dashboard.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" />
  <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=000" />
  <img src="https://img.shields.io/badge/Gemini_2.0-4285F4?style=for-the-badge&logo=google&logoColor=white" />
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#quick-start">Quick Start</a>
</p>

---

## ⚡ Features

News Intelligence goes far beyond a simple RSS aggregator. It uses state-of-the-art NLP models and a high-performance backend to dissect live news feeds, offering deep intelligence briefings instantly.

- **🌍 Multi-Region Real-Time Aggregation:** Scrapes live Google News RSS feeds across 14+ regions globally, isolating top-tier journalism.
- **🤖 Deep NLP Pipeline:** Extracts content locally using `newspaper3k` and processes text with Hugging Face models for:
  - Sentimental Analysis
  - Entity Recognition (NER)
- **🧠 Automated Intelligence Briefings:** Hands off aggregated top stories to Google's Gemini 2.0 Flash to stitch together a comprehensive, analytical executive summary of the topic.
- **✨ Premium UI/UX:** Built with React & Vite using ultra-smooth glassmorphism, dynamic animations, and complex SVG charting libraries to visualize sentiment shifts and sources.

## 🛠 Tech Stack

**Frontend:** React 18, Vite, Lucide-React, Recharts (for analytics).  
**Backend:** FastAPI, Python 3.10+, Uvicorn, httpx.  
**AI/NLP Models:** Google Gemini `gemini-2.0-flash`, Hugging Face (`distilBART`, `twitter-roberta`, `bert-base-NER`).  
**Deployment:** Vercel (Frontend), Render (Backend).

## 📸 Screenshots

Discover the deep analytics and the beautiful, "alive" UI aesthetic of the News Intelligence Platform dashboard.

> *(Note: Ensure these screenshots are pushed to your root directory so they load properly.)*

### Main Dashboard & Result Analytics
![Dashboard View](Screenshot%202026-04-02%20062641.png)

### NLP Data Visualizations
![Data View](Screenshot%202026-04-02%20062649.png)

### Article Deep-Dive
![Articles View](Screenshot%202026-04-02%20070031.png)

### Trending & Weather Live Widgets
![Live Widgets View](Screenshot%202026-04-02%20071804.png)

## 🚀 Quick Start

To run the application locally, you will need a Google Gemini API Key and a Hugging Face Token.

### 1. Clone the Repository
```bash
git clone https://github.com/yogender-ai/NewsIntel.git
cd NewsIntel
```

### 2. Setup the Backend
Navigate to the `backend` directory, install requirements, and start FastAPI.
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create a .env file with:
# GEMINI_API_KEY=your_key
# HF_TOKEN=your_token

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Setup the Frontend
Navigate to the `frontend` directory, install Node dependencies, and fire up Vite.
```bash
cd ../frontend
npm install

# Create a .env file with:
# VITE_API_URL=http://localhost:8000

npm run dev
```

---

<p align="center">
  <b>Built by Yogender AI</b><br>
  <i>Empowering open-source data intelligence.</i>
</p>
