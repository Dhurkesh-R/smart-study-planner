# 🧠 Smart Study Planner

An AI-powered study planner that helps students plan, retain, and revise efficiently using machine learning, spaced repetition, quiz generation (via LLaMA 3), and Google Calendar integration.

---

## 🚀 Features

- ✅ **Predict Optimal Study Time** using a trained ML model
- 📚 **Spaced Repetition Scheduling** based on recall performance
- 🧠 **Generate Quiz Questions** using local LLaMA 3 via Ollama
- 🗓️ **Google Calendar Integration** to schedule study sessions
- 🎯 User-friendly **React frontend**
- 🧪 Flask backend API with CORS and modular structure

---

## ⚙️ Technologies Used

### Frontend
- React + Tailwind CSS
- Axios for API calls

### Backend
- Flask + Flask-CORS
- Joblib for ML model loading
- OpenAI / Ollama + LLaMA 3 (for quiz generation)
- Google Calendar API

### Machine Learning
- RandomForestRegressor for study interval prediction
- Custom spaced repetition logic

---

## 🛠️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Dhurkesh-R/smart-study-planner.git