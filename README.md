# AI-Powered Personalized Learning System

An intelligent tutoring system that uses Machine Learning to personalize student learning paths based on quiz performance.

## 🎯 Project Overview

This project was developed as part of **Module E – IIT Ropar (Minor in AI)** under the track  
**AI in Personalized Learning**.

The system analyzes:
- Quiz score
- Time taken
- Attempts
- Accuracy  

and predicts the learner’s level:
- Struggling
- Average
- Advanced  

Based on this, it recommends:
- Easier practice
- Medium difficulty quizzes
- Advanced challenge material

A full interactive web app is also provided using **Streamlit**.

---

## 🧠 AI Technique Used
- Decision Tree Classifier (Scikit-learn)
- Explainable rule-based recommendations
- Synthetic student learning data (1000 learners)

---

## 📁 Repository Structure
ai-personalized-learning-system/
│
├── Personalized_Learning_System.ipynb ← Main evaluation notebook
├── app.py ← Streamlit interactive app
└── README.md


---

## 🚀 How to Run the App

1. Install dependencies:
pip install pandas numpy scikit-learn streamlit matplotlib seaborn

2. Run the app:
streamlit run app.py



3. Open browser at:
http://localhost:8501


---

## 📊 What the System Does

1. User selects subject and quiz level  
2. User takes a quiz  
3. AI model predicts learner level  
4. System recommends:
   - Learning speed
   - Difficulty
   - YouTube video
   - Reading resource  

This simulates how real EdTech platforms personalize content.

---

## 👤 Author
**Eraf Ali**  
Minor in Artificial Intelligence  
IIT Ropar


