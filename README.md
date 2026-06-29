<div align="center">

# 🏙️ CivicHero AI

### *AI-Powered Community Hero Platform*

**Together, we can build a better city.**

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Gemini AI](https://img.shields.io/badge/Gemini_2.5_Flash-AI_Powered-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud_Run-Deployed-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![HTML](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org)
[![CSS](https://img.shields.io/badge/Tailwind_CSS-Styled-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org)
[![License](https://img.shields.io/badge/License-MIT-16A34A?style=for-the-badge)](LICENSE)

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-16A34A?style=for-the-badge)](https://civichero-ai-840033169659.asia-south1.run.app)
[![Hackathon](https://img.shields.io/badge/Vibe2Ship-Hackathon_2026-FF6B35?style=for-the-badge&logo=google&logoColor=white)](https://blockseblock.com)

<br/>

> **Built for Google for Developers × Coding Ninjas Vibe2Ship Hackathon 2026**
> Problem Statement 2 — *Community Hero: Hyperlocal Problem Solver*

</div>

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🏗️ Architecture](#️-architecture)
- [📁 Project Structure](#-project-structure)
- [🚀 Installation](#-installation)
- [🔑 Environment Variables](#-environment-variables)
- [▶️ How to Run](#️-how-to-run)
- [☁️ Deployment on Google Cloud Run](#️-deployment-on-google-cloud-run)
- [📸 Screenshots](#-screenshots)
- [🤖 AI Features Deep Dive](#-ai-features-deep-dive)
- [🗺️ Future Improvements](#️-future-improvements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👤 Author](#-author)
- [🙏 Acknowledgements](#-acknowledgements)

---

## 🌟 About the Project

**CivicHero AI** is a production-ready, full-stack web platform that empowers citizens to **report, track, verify, and resolve** civic issues in their communities — powered by **Google Gemini 2.5 Flash AI**.

Communities across India face daily challenges with potholes, water leaks, broken streetlights, sewage overflow, and garbage mismanagement. Existing systems are fragmented, non-transparent, and lack intelligent routing to the right authorities.

CivicHero AI solves this by providing:

- 🤖 **Instant AI analysis** of every submitted issue using Gemini 2.5 Flash
- 📍 **Real-time geo-tagged issue mapping** with interactive Leaflet maps  
- 🔄 **Transparent status tracking** with timeline and community comments
- 🏆 **Gamified citizen engagement** with points, badges, and leaderboards
- 📊 **Live analytics dashboards** powered by Chart.js with real database data
- 🔒 **Complete authentication system** with secure password reset flow

---

## ✨ Features

### 🤖 AI-Powered Intelligence
| Feature | Description |
|---------|-------------|
| **Auto-categorization** | Gemini corrects wrong category selections automatically |
| **Severity Detection** | AI rates issues: Critical / High / Medium / Low |
| **Smart Department Routing** | Routes to PWD, Jal Nigam, DISCOM, Municipal Corp automatically |
| **Image Analysis** | Multimodal AI analyzes uploaded photos for visual severity |
| **AI Summary Generation** | Professional 2-3 sentence analysis of every issue |
| **ETA Prediction** | Estimated resolution time based on issue type and severity |
| **City-wide Insights** | Gemini generates monsoon risk alerts and cluster detection |
| **AI Chatbot Companion** | Real-time conversational assistant for any civic question |

### 🗺️ Mapping & Location
- Interactive **Leaflet.js + OpenStreetMap** with custom colored markers
- **GPS auto-detection** using browser geolocation API
- **Reverse geocoding** via Nominatim for automatic address fill
- Draggable markers with popup issue detail cards
- Filter by: Critical / High / In Progress / Resolved / Category
- Real-time side panel synchronized with map markers

### 👥 Community Features
- **Upvoting system** — issues with 10+ upvotes auto-escalated
- **Community comments** with real-time timeline updates
- **Gamification**: Points, badges (Pioneer, Active Voice, Change Maker, Top Hero)
- **Leaderboard podium** with Gold/Silver/Bronze rankings
- **Progress tracking** toward next badge level

### 🔐 Security & Authentication
- **Registration** with live password strength meter (PBKDF2-SHA256 hashing)
- **Login** with Remember Me and demo credentials auto-fill
- **Forgot Password** with cryptographically secure 32-byte tokens (1-hour expiry)
- **Reset Password** with one-time-use token verification
- **Profile management** with change-password functionality
- Full protection: SQL injection, XSS, path traversal, email enumeration prevention

### 📊 Analytics & Dashboard
- **5 Chart.js visualizations**: Bar, Doughnut, Line, Polar Area, Progress bars
- **Real-time KPI cards** with animated count-up
- **Department performance** comparison tables
- **Monthly trend analysis** — Reported vs Resolved over 6 months
- **Resolution funnel** visualization

---

## 🛠️ Tech Stack

### Backend
```
Python 3.10+  |  Flask 3.0.3  |  SQLite  |  Werkzeug 3.0.3
python-dotenv  |  requests     |  Pillow 10.4.0
```

### Frontend
```
HTML5  |  Tailwind CSS  |  Vanilla JavaScript ES6+
Chart.js  |  Leaflet.js  |  Lucide Icons
AOS (Animate on Scroll)  |  GSAP  |  Google Fonts
```

### AI & Cloud
```
Google Gemini 2.5 Flash  |  Gemini REST API v1beta
Google Cloud Run  |  Google AI Studio  |  Docker
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CIVICHERO AI                         │
│                                                         │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Browser  │───▶│  Flask App   │───▶│  SQLite DB   │  │
│  │(Tailwind) │    │  (app.py)    │    │ (5 tables)   │  │
│  └──────────┘    └──────┬───────┘    └──────────────┘  │
│                         │                               │
│                   ┌─────▼──────┐                        │
│                   │ Gemini API  │                        │
│                   │ REST v1beta │                        │
│                   │ 2.5 Flash   │                        │
│                   └─────┬──────┘                        │
│                         │                               │
│              ┌──────────▼──────────┐                    │
│              │  AI Analysis Module  │                    │
│              │  gemini_service.py   │                    │
│              │  Issue Analysis      │                    │
│              │  Chat Companion      │                    │
│              │  City Insights       │                    │
│              └─────────────────────┘                    │
└─────────────────────────────────────────────────────────┘

Deployed on: Google Cloud Run (asia-south1)
Container:   Docker
```

---

## 📁 Project Structure

```
civichero-ai/
│
├── app.py                          # Main Flask application & all routes
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in git)
├── README.md                       # This file
│
├── ai/
│   ├── __init__.py
│   └── gemini_service.py           # Gemini 2.5 Flash REST API integration
│
├── database/
│   ├── __init__.py
│   ├── db.py                       # SQLite schema, queries, seed data
│   └── civichero.db                # Auto-generated database
│
├── static/
│   ├── css/style.css               # All component styles
│   ├── js/app.js                   # Toast, ripple, search, transitions
│   └── uploads/                    # User-uploaded images & videos
│
├── templates/
│   ├── base.html                   # Layout: sidebar + navbar + AI chatbot
│   ├── index.html                  # Home page
│   ├── issues.html                 # Issues browser with filters
│   ├── report.html                 # 3-step report form
│   ├── dashboard.html              # Analytics dashboard
│   ├── issue_details.html          # Single issue view
│   ├── map.html                    # Full-screen live map
│   ├── community.html              # Leaderboard & community
│   ├── analytics.html              # Deep analytics
│   ├── 404.html                    # Error page
│   └── auth/
│       ├── auth_base.html          # Auth layout (split panel design)
│       ├── login.html              # Login page
│       ├── register.html           # Registration + password strength
│       ├── forgot_password.html    # Forgot password
│       ├── reset_password.html     # Reset password
│       └── profile.html            # User profile & settings
│
└── screenshots/                    # Application screenshots
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip
- Git

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/aaryanrajput/Civichero-Ai.git
cd civichero-ai

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Create .env file (see Environment Variables section below)

# 5. Run the application
python app.py
```

Open: **http://localhost:5000**

**Demo Account (ready to use):**
```
Email:    demo@civichero.ai
Password: demo123
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
# Flask
SECRET_KEY=your-random-secret-key-change-this
FLASK_ENV=development
FLASK_DEBUG=1

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# HERE Maps (optional)
HERE_API_KEY=your_here_key_here
```

---

## ▶️ How to Run

```bash
# Development server
python app.py

# Production with Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

---

## ☁️ Deployment on Google Cloud Run

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
```

```bash
gcloud run deploy civichero-ai \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key,SECRET_KEY=your_secret
```

**Live App:** https://civichero-ai-840033169659.asia-south1.run.app

---

## 🤖 AI Features Deep Dive

```
User Submits Report
       │
       ▼
┌─────────────────────────────────────────────────┐
│           Gemini 2.5 Flash REST API              │
│  Input: title + description + category + image  │
└───────────────────────┬─────────────────────────┘
                        │ Returns structured JSON:
                        ▼
  {
    "category":             "Pothole",
    "severity":             "critical",
    "department":           "PWD – Roads Division",
    "summary":              "Professional AI analysis...",
    "recommended_action":   "Deploy repair team...",
    "estimated_resolution": "24-48 hours",
    "confidence":           92
  }
```

---

## 🗺️ Future Improvements

| Feature | Priority | Version |
|---------|----------|---------|
| 📧 Email notifications via SendGrid | High | v1.1 |
| 📱 Browser push notifications | High | v1.1 |
| 🏛️ Government authority portal | High | v1.2 |
| 📱 Flutter mobile app (iOS/Android) | High | v2.0 |
| 🌆 Multi-city configuration | Medium | v2.0 |
| ⛓️ Blockchain audit trail | Low | v3.0 |

---

## 🤝 Contributing

```bash
git checkout -b feature/YourAmazingFeature
git commit -m 'Add: YourAmazingFeature'
git push origin feature/YourAmazingFeature
```

---

## 📄 License

Distributed under the **MIT License**.

---

## 👤 Author

**Aaryan Rajput**
- GitHub: [@aaryanrajput](https://github.com/aaryanrajput)
- Email: aaryanrajput0212@gmail.com
- Linkedin:www.linkedin.com/in/aaryan-rajput-63abb1384

---

## 🙏 Acknowledgements

- [Google for Developers](https://developers.google.com) — Gemini 2.5 Flash API
- [Coding Ninjas](https://codingninjas.com) — Vibe2Ship Hackathon 2026
- [Google Cloud Run](https://cloud.google.com/run) — Serverless container hosting
- [Leaflet.js](https://leafletjs.com) — Interactive maps
- [Tailwind CSS](https://tailwindcss.com) — Utility-first CSS framework
- [Chart.js](https://chartjs.org) — Data visualizations
- [Flask](https://flask.palletsprojects.com) — Python web framework

---

<div align="center">

**"Together, we can build a better city."** 🏙️

Made with ❤️ by Aaryan Rajput — Vibe2Ship Hackathon 2026

</div>

