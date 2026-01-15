import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import streamlit as st
# print("APP LOADED")
st.set_page_config(
    page_title="AI Personalized Tutor",
    layout="centered",
    initial_sidebar_state="collapsed"
)
if "page" not in st.session_state:
    st.session_state.page = "setup"


# ---------------- QUESTION BANK ----------------

question_bank = {
    "Math": {
        "Easy": [
            {"q": "What is 1/2 + 1/2?", "options": ["1", "2", "1/4", "3/2"], "ans": "1"},
            {"q": "What is 2 + 3?", "options": ["4", "5", "6", "7"], "ans": "5"},
            {"q": "What is 10 - 4?", "options": ["6", "7", "5", "4"], "ans": "6"},
            {"q": "What is 5 × 2?", "options": ["7", "8", "10", "12"], "ans": "10"},
            {"q": "What is 9 ÷ 3?", "options": ["2", "3", "4", "5"], "ans": "3"}
        ],
        "Hard": [
            {"q": "What is 3/4 + 1/4?", "options": ["1", "2", "1/2", "3/4"], "ans": "1"},
            {"q": "Solve: 2x = 10. x = ?", "options": ["2", "3", "4", "5"], "ans": "5"},
            {"q": "What is 15% of 200?", "options": ["20", "30", "40", "50"], "ans": "30"},
            {"q": "What is √81?", "options": ["7", "8", "9", "10"], "ans": "9"},
            {"q": "What is 7 × 8?", "options": ["48", "54", "56", "64"], "ans": "56"}
        ]
    },

    "Computer Science": {
        "Easy": [
            {"q": "Which symbol is used to assign a value?", "options": ["=", "==", "!=", "<"], "ans": "="},
            {"q": "Which keyword is used for a loop?", "options": ["if", "for", "print", "def"], "ans": "for"},
            {"q": "Which stores text?", "options": ["int", "float", "string", "bool"], "ans": "string"},
            {"q": "Which means True/False?", "options": ["int", "bool", "char", "double"], "ans": "bool"},
            {"q": "Which prints output?", "options": ["print", "input", "scan", "show"], "ans": "print"}
        ],
        "Hard": [
            {"q": "Which loop runs at least once?", "options": ["for", "while", "do-while", "if"], "ans": "do-while"},
            {"q": "Which stores multiple values?", "options": ["int", "list", "bool", "float"], "ans": "list"},
            {"q": "What does len() return?", "options": ["size", "length", "value", "type"], "ans": "length"},
            {"q": "Which keyword defines a function?", "options": ["func", "def", "method", "run"], "ans": "def"},
            {"q": "Which is used for conditions?", "options": ["if", "for", "print", "break"], "ans": "if"}
        ]
    }
}

# ---------------- LEARNING RESOURCES ----------------

learning_resources = {
    "Math": {
        "Easy": {
            "video": "https://www.youtube.com/watch?v=IwW0GJWKH98",
            "text": "https://www.khanacademy.org/math/arithmetic"
        },
        "Hard": {
            "video": "https://www.youtube.com/watch?v=NybHckSEQBI",
            "text": "https://www.khanacademy.org/math/algebra"
        }
    },
    "Computer Science": {
        "Easy": {
            "video": "https://www.youtube.com/watch?v=rfscVS0vtbw",
            "text": "https://www.geeksforgeeks.org/python-programming-language/"
        },
        "Hard": {
            "video": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
            "text": "https://www.geeksforgeeks.org/data-structures/"
        }
    }
}


# ---------- DATA GENERATION ----------
np.random.seed(42)

num_students = 1000
students = [f"S{i+1}" for i in range(num_students)]

subjects = ["Math", "Computer Science"]
topics_math = ["Fractions", "Algebra", "Geometry"]
topics_cs = ["Loops", "Variables", "Functions"]

data = []

for student in students:
    for subject in subjects:
        if subject == "Math":
            topic = np.random.choice(topics_math)
        else:
            topic = np.random.choice(topics_cs)
        
        score = np.random.randint(0, 11)
        time_taken = np.random.randint(100, 600)
        attempts = np.random.randint(1, 4)
        accuracy = score / 10 * 100
        
        data.append([student, subject, topic, score, time_taken, attempts, accuracy])

df = pd.DataFrame(data, columns=[
    "student_id", "subject", "topic", "score", "time_taken", "attempts", "accuracy"
])

# ---------- LABEL CREATION ----------
def get_level(acc):
    if acc < 40:
        return "Struggling"
    elif acc < 75:
        return "Average"
    else:
        return "Advanced"

df["level"] = df["accuracy"].apply(get_level)

le = LabelEncoder()
df["level_encoded"] = le.fit_transform(df["level"])

X = df[["score", "time_taken", "attempts", "accuracy"]]
y = df["level_encoded"]

model = DecisionTreeClassifier()
model.fit(X, y)

# ---------- RECOMMENDATION FUNCTION ----------
def recommend_content(score, time_taken, attempts, accuracy):
    input_data = [[score, time_taken, attempts, accuracy]]
    predicted_level = model.predict(input_data)[0]
    level_name = le.inverse_transform([predicted_level])[0]

    # Learning speed
    if time_taken < 250:
        speed = "Fast"
    elif time_taken < 450:
        speed = "Normal"
    else:
        speed = "Slow"

    # Explainable AI
    explanation = ""
    if accuracy < 40:
        explanation += "Low accuracy. "
    if attempts > 2:
        explanation += "Many attempts. "
    if time_taken > 450:
        explanation += "Slow response. "
    if explanation == "":
        explanation = "Strong and confident performance."

    if level_name == "Struggling":
        recommendation = "Show basic tutorial + easy practice questions"
    elif level_name == "Average":
        recommendation = "Show medium difficulty quiz with hints"
    else:
        recommendation = "Show challenge problems + advanced content"

    return level_name, speed, explanation, recommendation


# ---------- STREAMLIT UI ----------
st.title("AI-Powered Personalized Tutor")
st.markdown("""
<style>
h1 {
    color: #2b6cb0;
    text-align: center;
}
.stButton > button {
    background-color: #2b6cb0;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
.block-container {
    max-width: 900px;
    margin: auto;
}

[data-testid="stMetric"] {
    background-color: #f8fafc;
    padding: 12px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

if st.session_state.page == "setup":
    st.header("Quiz Setup")

    subject = st.selectbox("Select Subject", ["Math", "Computer Science"])
    level_choice = st.selectbox("Select Quiz Level", ["Easy", "Hard"])

    if st.button("🚀 Start Quiz"):
        st.session_state.subject = subject
        st.session_state.level_choice = level_choice
        st.session_state.quiz_start = time.time()
        st.session_state.page = "quiz"
        st.rerun()

# ---------------- QUIZ PAGE ----------------
if st.session_state.page == "quiz":
    subject = st.session_state.subject
    level_choice = st.session_state.level_choice
    questions = question_bank[subject][level_choice]

    score = 0
    attempts = 1

    elapsed = int(time.time() - st.session_state.quiz_start)
    st.info(f"⏱️ Time spent: {elapsed} seconds")

    st.write("Answer the 5 questions below:")
    user_answers = []

    for i, q in enumerate(questions):
        st.write(f"Q{i+1}: {q['q']}")
        ans = st.radio(
            f"Choose answer for Q{i+1}",
            ["-- Select an option --"] + q["options"],
            key=f"q{i}"
        )
        user_answers.append(ans)

    if st.button("Submit Quiz"):
        end_time = time.time()
        st.session_state.time_taken = int(end_time - st.session_state.quiz_start)

        for i, q in enumerate(questions):
            if user_answers[i] == q["ans"]:
                score += 1

        st.session_state.score = score
        st.session_state.accuracy = (score / 5) * 100
        st.session_state.page = "result"
        st.rerun()


# ---------------- RESULT PAGE ----------------
if st.session_state.page == "result":
    score = st.session_state.score
    accuracy = st.session_state.accuracy
    time_taken = st.session_state.time_taken
    subject = st.session_state.subject

    level, speed, explanation, recommendation = recommend_content(score*2, time_taken, 1, accuracy)

    st.subheader("Quiz Result")
    c1, c2, c3 = st.columns(3)
    c1.metric("Score", f"{score} / 5")
    c2.metric("Accuracy", f"{accuracy:.1f}%")
    c3.metric("Time (sec)", time_taken)

    st.progress(accuracy / 100)

    st.markdown("## 🧠 AI Decision")

    st.success(f"Learner Level: {level}")

    st.write("Learning Speed:", speed)
    st.write("Why this decision:", explanation)

    if level in ["Struggling", "Average"]:
        res_level = "Easy"
    else:
        res_level = "Hard"

    video = learning_resources[subject][res_level]["video"]
    text = learning_resources[subject][res_level]["text"]

    st.write("Recommended Action:", recommendation)

    st.markdown("### 📚 Learning Resources")
    st.link_button("📺 Watch Learning Video", video)
    st.link_button("📘 Read Learning Material", text)

    if st.button("🔄 Try Another Quiz"):
        st.session_state.page = "setup"
        st.rerun()
