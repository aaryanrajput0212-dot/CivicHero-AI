# 🏙️ CivicHero AI — Community Hero Platform

> **Google for Developers × Coding Ninjas Vibe2Ship Hackathon**
> Problem Statement 2 — Community Hero: Hyperlocal Problem Solver

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-purple)](https://ai.google.dev)

---

## 🚀 What is CivicHero AI?

CivicHero AI is a production-ready civic issue reporting platform that empowers citizens to report, track, and resolve community problems — powered by **Google Gemini 2.5 Flash** AI.

Citizens can report potholes, water leaks, broken streetlights, garbage overflow, and more. The AI automatically analyzes, categorizes, prioritizes, and routes each issue to the correct government department.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Analysis** | Gemini 2.5 Flash auto-categorizes, detects severity, and routes to departments |
| 📍 **Interactive Map** | Live issue map with colored markers, filters, and popups |
| 📸 **Media Upload** | Photo & video upload with AI image analysis |
| 📊 **Analytics Dashboard** | Chart.js-powered insights on issues, trends, and department performance |
| 🏆 **Gamification** | Points, badges, and leaderboard for citizen engagement |
| 🔍 **Community Verification** | Upvoting, comments, and AI confidence scores |
| 📈 **Predictive Insights** | Monsoon risk alerts, cluster detection, resolution forecasting |

---

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite (via sqlite3)
- **AI**: Google Gemini 2.5 Flash API
- **Frontend**: HTML5 + Tailwind CSS + Vanilla JS
- **Maps**: Leaflet.js (OpenStreetMap) / HERE Maps ready
- **Charts**: Chart.js
- **Icons**: Lucide Icons
- **Animations**: AOS + GSAP
- **Fonts**: Inter + Poppins

---

## 📁 Project Structure

```
civichero-ai/
├── app.py                  # Flask application & routes
├── static/
│   ├── css/style.css       # All component styles
│   ├── js/app.js           # Client-side JS
│   └── uploads/            # User-uploaded images/videos
├── templates/
│   ├── base.html           # Layout with sidebar & navbar
│   ├── index.html          # Home page
│   ├── issues.html         # Issues list
│   ├── report.html         # Report issue (multi-step)
│   ├── dashboard.html      # Analytics dashboard
│   ├── issue_details.html  # Single issue view
│   ├── map.html            # Full-screen live map
│   ├── community.html      # Leaderboard & community
│   ├── analytics.html      # Deep analytics
│   └── 404.html            # Error page
├── ai/
│   └── gemini_service.py   # Gemini AI integration
├── database/
│   └── db.py               # SQLite schema & queries
├── requirements.txt
├── .env                    # Environment variables
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/civichero-ai.git
cd civichero-ai
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env .env.local
# Edit .env and add your keys:
# GEMINI_API_KEY=your_key_here
# HERE_API_KEY=your_key_here
```

Get your Gemini API key free at: https://aistudio.google.com/app/apikey

### 3. Run

```bash
python app.py
```

Open http://localhost:5000 🎉

---

## 🤖 AI Features (Gemini 2.5 Flash)

When a citizen submits an issue, Gemini automatically:

- **Categorizes** the issue (Roads, Water, Electricity, Sewage, Garbage, Parks, etc.)
- **Detects severity** (Critical / High / Medium / Low)
- **Assigns priority** based on public safety impact
- **Routes to department** (PWD, Jal Nigam, DISCOM, Municipal Corp, etc.)
- **Generates AI summary** with recommended action
- **Estimates resolution time** (24h to 2 weeks)
- **Analyzes uploaded images** for visual severity confirmation
- **Generates citywide insights** with risk alerts and recommendations

---

## 📊 Evaluation Criteria Coverage

| Criteria | Coverage |
|----------|----------|
| **Problem Solving & Impact** (20%) | Solves fragmented civic reporting with end-to-end tracking |
| **Agentic Depth** (20%) | Gemini AI auto-analyzes, categorizes, routes, and escalates autonomously |
| **Innovation & Creativity** (20%) | Gamification, predictive insights, cluster detection, AI image analysis |
| **Usage of Google Technologies** (15%) | Gemini 2.5 Flash API, Google AI Studio deployment |
| **Product Experience & Design** (10%) | Linear/Vercel-inspired SaaS UI, smooth animations, responsive |
| **Technical Implementation** (10%) | Flask + SQLite + Chart.js + Leaflet Maps, full CRUD |
| **Completeness & Usability** (5%) | All features working, seeded data, production-ready |

---

## 🌐 Deployment (Google AI Studio)

Refer to: https://ai.google.dev/gemini-api/docs/aistudio-deploying

---

## 📝 License

MIT — Built for Vibe2Ship Hackathon 2026
