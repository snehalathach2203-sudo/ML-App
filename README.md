# 🎓 AI-Based Student Performance & Career Recommendation System

<p align="center">

### 📊 Predict Performance • 🎯 Recommend Careers • 🧩 Identify Skill Gaps

An AI-driven Streamlit application that predicts student academic performance and recommends suitable career paths based on academic profile, skills, certifications, and career interests.

## 🚀 Live Demo
👉 **[Open Application on Streamlit Cloud](https://ml-app-sch.streamlit.app)**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge\&logo=pandas)
![Scikit Learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge\&logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge\&logo=streamlit)

</p>

---

## ✨ Features

### 📈 Student Performance Prediction

Predicts final academic marks and grade point using:

* Attendance
* Study Hours
* Assignment Score
* Internal Test Score

### 🎯 Career Recommendation

Recommends the **Top 5 career paths** based on:

* Education & Branch
* Grade Point
* Skills
* Certifications
* Career Interests

### 🧩 Skill Gap Analysis

For a selected career, identifies:

* ✅ Matched Skills
* 📚 Skills to Learn

### 💾 Prediction History

Every prediction is saved to a CSV file with:

* Timestamp
* Student details
* Prediction results
* Recommended careers

---

## 🔄 Workflow

```text
👨‍🎓 Student Profile
        ↓
📊 Performance Prediction
        ↓
⭐ Grade Point
        ↓
🎯 Top 5 Career Recommendations
        ↓
🧩 Select Career
        ↓
✅ Matched Skills + 📚 Missing Skills
        ↓
💾 Prediction History
```

---

## 🛠️ Tech Stack

| Category            | Technology   |
| ------------------- | ------------ |
| Programming         | Python       |
| Data Processing     | Pandas       |
| Machine Learning    | Scikit-learn |
| Web Application     | Streamlit    |
| Data Storage        | CSV          |
| Data/Knowledge Base | Pickle       |

---
## 📚 Data Sources

| Dataset | Purpose |
|---|---|
| [Student Academic Performance Dataset](https://www.kaggle.com/datasets/sonalshinde123/student-academic-performance-dataset/data) | Student performance prediction |
| [Job Skill Set Dataset](https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set) | Career skill analysis |
| Career Skills Knowledge Base & Career-wise skill mapping and recommendation | LLM (ChatGPT)  |

> Career knowledge and skill mappings were prepared and structured for the career recommendation module.

---

## 📁 App Structure

```text
App/
│
├── backend/
│   ├── main.py
│   ├── predict.py
│   ├── requirements.txt
│   └── recommendation.py
|
├── frontend/
│   ├── app.py
│   ├── requirements.txt
|
├── pickles/
│   └── marksmodel.pkl
│   └── career_recommendation.pkl
│
├── data/
│   └── prediction_history.csv
```

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt (for backend and frontend separately)
```

```bash
streamlit run app.py
```

---

## 📊 Application Preview

> Add your screenshots here after uploading them to the repository.

```text
assets/
├── home.png
├── prediction.png
├── recommendations.png
└── skill-gap.png
```

<img width="1354" height="690" alt="image" src="https://github.com/user-attachments/assets/6820b64d-e5fd-4f2d-941e-017799cb236b" />


---

## 🎯 Project Highlights

* Built an **end-to-end ML application** rather than only a standalone model.
* Combined **prediction + recommendation + skill-gap analysis** in one application.
* Implemented interactive career exploration using **Streamlit session state**.
* Added **timestamped prediction history** for future analysis.

---
## 🔮 Future Scope

- 🚀 **FastAPI Integration** — Serve the trained ML model through REST APIs for scalable and production-ready model inference.
- 🗄️ **Database Integration** — Replace CSV-based prediction history with a database such as PostgreSQL, Supabase, or Firebase for persistent and scalable data storage.
- 📊 **Analytics Dashboard** — Add visual analytics for prediction history, career trends, and skill gaps.
- 🔐 **User Authentication** — Add secure student and administrator accounts.
---

## ⚠️ Disclaimer

This application provides AI/ML-based predictions and career recommendations for **educational exploration**. Results should not be considered guaranteed academic or career outcomes.

---

<p align="center">

### ⭐ Built with Python, Machine Learning & Streamlit

</p>

