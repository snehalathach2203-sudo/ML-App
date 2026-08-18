# type: ignore

# ---------------------------------------------------------
# Libraries
# ---------------------------------------------------------
import streamlit as st       
from streamlit_option_menu import option_menu
import pickle
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

import warnings 
warnings.filterwarnings("ignore") # To supress warnings

# ---------------------------------------------------------
# Path Setup
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# ---------------------------------------------------------
# Backend Imports
# ---------------------------------------------------------
from backend.predict import (predict_final_marks,marks_to_grade_point)
from backend.recommendation import (recommend_careers,get_skill_gap)

# ---------------------------------------------------------
# Module 2 Data
# ---------------------------------------------------------
CAREER_PICKLE = (BASE_DIR/ "pickles"/ "career_recommendation.pkl")
with open(CAREER_PICKLE, "rb") as file:
    career_data = pickle.load(file)

career_kb = career_data["career_knowledge_base"] # Career Knowledge Base
final_career_skills = career_data["career_skills"]

# ---------------------------------------------------------
# Prediction History
# ---------------------------------------------------------
PREDICTION_CSV = BASE_DIR / "data" / "prediction_history.csv"
PREDICTION_CSV.parent.mkdir(parents=True, exist_ok=True)

def save_prediction_history(education,branch,attendance,studyhours,assignmentscore,internaltestscore,
skills,certifications,interests,final_marks,grade_point,recommendations):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = {"Timestamp": timestamp,"Education": education,"Branch": branch,"Attendance(%)": attendance,
    "StudyHours": studyhours,"AssignmentScore": assignmentscore,"InternalTestScore": internaltestscore,"Skills": ", ".join(skills),
    "Certifications": ", ".join(certifications),"Interests": ", ".join(interests),"PredictedFinalMarks": round(final_marks, 2),
    "GradePoint": grade_point,"Career1": "","Career2": "","Career3": "","Career4": "","Career5": ""}

    if not recommendations.empty:
        careers = recommendations["career_path"].tolist()
        for index, career in enumerate(careers[:5], start=1):
            row[f"Career{index}"] = career

    new_data = pd.DataFrame([row])
    if PREDICTION_CSV.exists():
        new_data.to_csv(PREDICTION_CSV,mode="a",header=False,index=False)
    else:
        new_data.to_csv(PREDICTION_CSV,mode="w",header=True,index=False)
# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Student Career Recommendation",page_icon="🎓",layout="wide")
# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "student" not in st.session_state:
    st.session_state.student = None

if "skills" not in st.session_state:
    st.session_state.skills = []

if "final_marks" not in st.session_state:
    st.session_state.final_marks = None

if "grade_point" not in st.session_state:
    st.session_state.grade_point = None

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
st.markdown("""<style>
/* Adjust Sidebar Width */
[data-testid="stSidebar"]{width: 250px !important;  min-width: 250px !important;}
/* Justify main content */
.stMarkdown p {text-align: justify !important;}
/* Reduce the large top gap in the main content */
[data-testid="stMainBlockContainer"]{padding-top: 50px !important;}
.stButton > button {background-color: blue; border: 2px solid #4CAF50;}
</style>""",
unsafe_allow_html=True)

st.markdown("""<style>
.skill-pill {display: inline-block;padding: 6px 12px;margin: 4px 4px 4px 0;border-radius: 15px;
font-size: 13px;font-weight: 500;}
.matched-pill {background-color: #123d2b;color: #4ade80;}
.missing-pill {background-color: #19324d;color: #60a5fa;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Student", ["Home", "Overview", "AI",'History'], 
        icons=['house', 'info-square-fill','calculator-fill','bi bi-clock-history'], 
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "black"},
            "icon": {"color": "white", "font-size": "15px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "black"},
            "nav-link-selected": {"background-color": "blue"},
        }
    )

if selected == 'Home':
    st.subheader(":green[📝 Summary]",divider='blue')
    cola, colb = st.columns([0.5,0.05])
    with cola: st.write("An AI-driven educational application that takes 🧑🏻‍🎓 student academic records and skill sets to predict final academic marks and recommend tailored career paths. Helps institutions allocate counseling and tutoring resources to students who need them most.")
    with colb: st.image("https://cdn-icons-png.flaticon.com/512/6427/6427283.png")
    st.subheader(":green[✨ Key Importance]",divider='blue')
    colw, colx = st.columns(2)
    with colw:
        with st.container(height=150):
            st.write("🎯 Data-Driven Guidance")
            st.write("Replaces generic career advice with personalized, evidence-based recommendations mapping specific skills to market demand.")
    with colx:
        with st.container(height=150):
            st.write("🎯 Skill Gap Analysis")
            st.write("Highlights the exact skills a student needs to develop to achieve their desired career path.")
    st.subheader(":green[👨‍👨 Target Audience]",divider='blue')
    colw, colx, coly = st.columns(3)
    with colw:
        with st.container(height=150):
            st.write("👨‍🎓 Students")
            st.write("Under Graduate students who are in final years or completed seeking academic clarity and career direction.")
    with colx:
        with st.container(height=150):
            st.write("🏢 Educational Institutions")
            st.write("Universities, colleges, and schools looking to enhance student success and placement rates.")
    with coly:
        with st.container(height=150):
            st.write("👩‍💼 Career Counselors")
            st.write("Advisors requiring data-backed tools to streamline and validate their counseling processes.")

elif selected == 'Overview':
    st.write("The app developed in two modules,")
    colw, colx = st.columns(2)
    with colw:
        with st.container(height=450):
            st.write("🧩 :blue[Module1] - Student Final Marks Prediction")
            st.write("Predicts the student's final marks using academic and study-related information.")
            st.write(":green[DataSource] https://www.kaggle.com/datasets/sonalshinde123/student-academic-performance-dataset/data")
            st.write(":green[DataSnippet]")
            st.dataframe(pd.read_csv(BASE_DIR / "data" / "final_marks.csv").head(2))
            st.write(":green[Implementation]")
            st.write("Collected data validated, pre-processed and built an ML Model (Linear Regression)")
            st.write(":green[Prediction]")
            st.write("👨‍🎓 Student Input -> 📅 Attendance, 📝 Internal Marks, 📚 Assignment Score, ⏱️ Study Hours -> 🎯 Predicted Final Marks -> ⭐ Grade Point")
            st.write(":green[Tech Stack]")
            st.write("🐍 Python | Core programming |, 🐼 Pandas | Data processing |, 🤖 Scikit-learn | ML model |")

    with colx:
        with st.container(height=450):
            st.write("🧩 :blue[Module2] - Career Path Recommendation")
            st.write("For the taken/given student details 🎓 Education, ⭐ Grade Point, 🛠️ Skills, 📜 Certifications & ❤️ Career Interests, Student profile will be created")
            st.write("Job-post data is taken to identify skills commonly required in different career paths.")
            st.write(":green[DataSource] https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set")
            st.write(":green[DataSnippet]")
            st.dataframe(pd.read_csv(BASE_DIR / "data" / "all_job_post.csv").head(2))
            st.write("Taken Career Skills & Knowledge Base data from LLM - Chatgpt to Build Career Profile")
            st.write(":green[DataSnippet]")
            st.dataframe(pd.read_csv(BASE_DIR / "data" / "career_skills.csv").head(2))
            st.write(":green[Implementation]")
            st.write("👤 Student Profile -> 🔎 Career Relevance -> 📊 Career Scoring -> 🏆 Top 5 Career Paths -> 🧩 Skill Gap Analysis -> 📚 Recommended Skills")
            st.write(":green[Scoring]")
            st.write("🎓 Education | **15%** |,  🌿 Branch | **15%** |,  ⭐ Grade Point | **15%** |, 🛠️ Core Skills | **30%** |, 🚀 Advanced Skills | **10%** |, 📜 Certification | **5%** |, ❤️ Interest | **10%** |")
            st.write(":green[Tech Stack]")
            st.write("🐍 Python | Core programming |, 🐼 Pandas | Data processing |")

    st.info('Click on AI for Prediction & Recommendation', icon="ℹ️")

elif selected == 'AI':
    st.caption("⚠️ This app provides AI predictions, not guaranteed facts; independently verify all outputs before making critical decisions.")
    st.write("Enter Below Asked Info of 👨‍🎓 Student.")
    cola, colb = st.columns(2, border=True)
    with cola:
        # =========================================================
        # STUDENT ACADEMIC DETAILS
        # =========================================================
        st.write("#### 📊 Academic Details")
        col1, col2 = st.columns(2)
        with col1:
            education = st.selectbox("📚 Education",
            ["B.Tech","B.E","Degree","B.Sc","B.Com","BCA","M.Tech","MBA","MCA"])
            attendance = st.number_input("🙋 Attendance (%):",min_value=0.0,max_value=100.0,value=75.0)
            assignmentscore = st.number_input("📝 Assignment Score",min_value=0.0,max_value=10.0,value=5.0)

        with col2:
            branch = st.text_input("🏷️ Branch",placeholder="Example: Computer Science")
            studyhours = st.number_input("👩🏻‍💻 Daily Study Hours",min_value=0.0,max_value=12.0,value=2.0)
            internaltestscore = st.number_input("📝 InternalTestScore:",min_value=0.0,max_value=40.0,value=20.0)
            
    with colb:
        # =========================================================
        # SKILLS DETAILS
        # =========================================================
        st.write("#### 📝 Other Information")
        col1, col2 = st.columns(2)
        with col1:
            skills_input = st.text_input("✨ Skills",placeholder="Python, SQL, Excel")
        with col2:
            certifications_input = st.text_input("🏅 Certifications",placeholder="Python, Excel, PL-300")
        interest_input = st.text_input("🧐 Career Interests",placeholder="Example: Data, Analytics")

    # =========================================================
    # PREDICTION BUTTON
    # =========================================================
    if st.button("🚀 Predict & Recommend",type="primary"):
        with st.spinner("🤖 Analyzing student profile... Please wait"):
            # Conversion of other inputs
            skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
            certifications = [cert.strip() for cert in certifications_input.split(",") if cert.strip()]
            interests = [interest.strip() for interest in interest_input.split(",") if interest.strip()]

            # STUDENT DATA GIVEN
            st.info('Given Student Data', icon="ℹ️")
            st.dataframe(pd.DataFrame(
                [[education,branch,attendance,studyhours,assignmentscore,internaltestscore,skills,certifications,interests]],
                columns=['Education','Branch','Attendance(%)','StudyHours','AssignmentScore','InternalTestScore',
                'Skills','Certifications','Interests']))

            # -----------------------------------------------------
            # PREDICTIONS & RECOMMENDATIONS
            # -----------------------------------------------------
            # MODULE 1
            final_marks = predict_final_marks(attendance,studyhours,assignmentscore,internaltestscore)
            grade_point = marks_to_grade_point(final_marks)
            # CAREER PROFILE
            student = {"education": education,"branch": branch,"grade_point": grade_point,"skills": skills,
            "certifications": certifications,"interest": interests}
            # MODULE 2
            recommendations = recommend_careers(student,career_kb,final_career_skills,top_n=5)
            # ---------------------------------------------------------
            # SAVE PREDICTION HISTORY
            # ---------------------------------------------------------
            save_prediction_history(education=education,branch=branch,attendance=attendance,studyhours=studyhours,
                assignmentscore=assignmentscore,internaltestscore=internaltestscore,skills=skills,certifications=certifications,
                interests=interests,final_marks=final_marks,grade_point=grade_point,recommendations=recommendations)

            st.session_state.skills = skills
            st.session_state.student = student
            st.session_state.final_marks = final_marks
            st.session_state.grade_point = grade_point
            st.session_state.recommendations = recommendations
            
            st.success("✅ Prediction and career recommendations completed!")

    # =========================================================
    # PREDICTION RESULTS DISPLAY
    # =========================================================
    if st.session_state.final_marks is not None:
        st.write("#### 📈 Performance Prediction")
        col1, col2 = st.columns(2)
        with col1:st.metric("Estimated Final Marks:",f"{st.session_state.final_marks:.1f}")
        with col2:st.metric("Grade Point:",st.session_state.grade_point)
    # =========================================================
    # CAREER RECOMMENDATION DISPLAY
    # =========================================================
    if st.session_state.recommendations is not None:
        recommendations = st.session_state.recommendations
        skills = st.session_state.skills
        st.write("#### 🎯 Recommended Top 5 Career Paths")
        if recommendations.empty:
            st.warning(
                "No relevant career paths found. "
                "Try adding more skills or career interests.")
        else:
            cola, colb = st.columns([0.3, 0.6], border=True)
            with cola:
                st.dataframe(recommendations,use_container_width=True,hide_index=True)
            with colb:
                selected_career = st.selectbox("Select a career to explore",recommendations["career_path"],key="career_selector")
                # Skill Gap
                matched, missing = get_skill_gap(selected_career,skills,final_career_skills)
                st.write(f"##### 🧩 Skill Gap — {selected_career}")
                col1, col2 = st.columns(2)

                # Matched
                with col1:
                    st.write("##### ✅ Matched Skills")
                    if matched:
                        pills = ""
                        for skill in sorted(matched):
                            pills += f"""<span class="skill-pill matched-pill">{skill}</span>"""
                        st.markdown(pills,unsafe_allow_html=True)
                    else:
                        st.write("⚠️ No matched skills yet.")

                # Missing
                with col2:
                    st.write("##### 📚 Skills to Learn")
                    if missing:
                        pills = ""
                        for skill in sorted(missing):
                            pills += f"""<span class="skill-pill missing-pill">{skill}</span>"""
                        st.markdown(pills,unsafe_allow_html=True)
                    else:
                        st.success("You already have the all required skills!")

else:
    try:
        st.dataframe(pd.read_csv(PREDICTION_CSV))
    except:
        pass
    
