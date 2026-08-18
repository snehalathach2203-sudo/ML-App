import pandas as pd

# =========================================================
# 1. SKILL NORMALIZATION
# =========================================================

skill_aliases = {
    "communication": "Communication",
    "communication skills": "Communication",
    "problem solving": "Problem Solving",
    "problem-solving": "Problem Solving",
    "teamwork": "Teamwork",
    "collaboration": "Collaboration",
    "adaptability": "Adaptability",
    "time management": "Time Management",
    "leadership": "Leadership",
    "data analysis": "Data Analysis",
    "microsoft office": "Microsoft Office",
    "microsoft office suite": "Microsoft Office",
    "ms office": "Microsoft Office",
    "project management": "Project Management",
    "attention to detail": "Attention to Detail",
}

def normalize_skill(skill):
    skill = str(skill).strip()
    key = skill.lower()
    return skill_aliases.get(key, skill)

# =========================================================
# 2. EDUCATION SCORE
# =========================================================
def education_score(student_education, career_education):
    student = str(student_education).lower().strip()
    career_education = str(career_education).lower()
    if "any degree" in career_education:
        return 100
    if student in career_education:
        return 100
    degree_types = ["degree","b.sc","bca","b.tech","b.e","mca","m.tech","m.sc","mba",]
    if student in degree_types and "degree" in career_education:
        return 100

    return 0

# =========================================================
# 3. BRANCH SCORE
# =========================================================
branch_aliases = {
    "computer science": "CSE",
    "computer science engineering": "CSE",
    "cs": "CSE",
    "information technology": "IT",
    "it": "IT",
    "computers": "Computer Applications",
}

def branch_score(student_branch, career_branches):
    student = str(student_branch).lower().strip()
    student = branch_aliases.get(student,student)
    branches = [x.strip().lower() for x in str(career_branches).split(";")]
    if "any" in branches:
        return 100
    if student.lower() in branches:
        return 100
    for branch in branches:
        if (student.lower() in branch or branch in student.lower()):
            return 75
    return 0

# =========================================================
# 4. GRADE SCORE
# =========================================================

def grade_score(grade_point):
    grade_point = float(grade_point)
    if grade_point >= 8:
        return 100
    elif grade_point >= 7:
        return 80
    elif grade_point >= 6:
        return 60
    elif grade_point >= 5:
        return 40
    return 20


# =========================================================
# 5. INTEREST MAPPING
# =========================================================
interest_categories = {"Data": ["Data & Analytics","Data Engineering","Product & Analytics"],
                       "Analytics": ["Data & Analytics","Business & Technology","Product & Analytics"],
                       "AI": ["AI & Machine Learning"],
                       "Machine Learning": ["AI & Machine Learning"],
                       "Software": ["Software Development"],
                       "Web Development": ["Software Development"],
                       "Cloud": ["Cloud & Infrastructure"],
                       "DevOps": ["Cloud & Infrastructure"],
                       "Cybersecurity": ["Cybersecurity"],
                       "Design": ["Design & Technology"],
                       "Business": ["Business & Technology","Business & Analytics"]}

def interest_score(student_interests,career,career_kb):
    career_row = career_kb[career_kb["career_path"] == career]
    if career_row.empty:
        return 0
    career_category = career_row.iloc[0]["career_category"]
    for interest in student_interests:
        interest = str(interest).strip().lower()
        if interest in interest_categories:
            categories = interest_categories[interest]
            if career_category in categories:
                return 100
    return 0


# =========================================================
# 6. CERTIFICATION
# =========================================================
career_certifications = {"Data Analyst": ["Excel","Power BI","PL-300"],
                         "Business Intelligence Analyst": ["Power BI","PL-300"],
                         "Cloud Engineer": ["AWS","Azure"],
                         "DevOps Engineer": ["AWS","Azure","Kubernetes"],
                         "Cybersecurity Analyst": ["Security+"]}

def certification_score(student_certifications,career):
    required = career_certifications.get(career,[])
    if not required:
        return 0
    student_certs = {str(cert).lower().strip() for cert in student_certifications}
    required_certs = {str(cert).lower().strip() for cert in required}
    matched = student_certs.intersection(required_certs)
    if matched:
        return 100
    return 0


# =========================================================
# 7. CORE + ADVANCED SKILLS
# =========================================================
def calculate_skill_scores(student_skills,career,final_career_skills):
    career_data = final_career_skills[final_career_skills["career_path"] == career]
    core_skills = set(career_data[career_data["skill_type"] == "Core"]["skill"])
    advanced_skills = set(career_data[career_data["skill_type"] == "Advanced"]["skill"])
    student_skills = set(normalize_skill(skill)for skill in student_skills)
    matched_core = student_skills.intersection(core_skills)
    matched_advanced = student_skills.intersection(advanced_skills)
    if len(core_skills) > 0:
        core_score = (len(matched_core)/len(core_skills)) * 100
    else:
        core_score = 0

    if len(advanced_skills) > 0:
        advanced_score = (len(matched_advanced)/len(advanced_skills)) * 100
    else:
        advanced_score = 0

    return (core_score,advanced_score,matched_core,matched_advanced)

# =========================================================
# 8. CAREER RELEVANCE
# =========================================================
def career_relevance(student,career,career_kb,final_career_skills):
    (core_score,advanced_score,matched_core,matched_advanced) = calculate_skill_scores(
        student["skills"],career,final_career_skills)
    interest = interest_score(student["interest"],career,career_kb)
    if (len(matched_core) > 0 or len(matched_advanced) > 0 or interest > 0):
        return True
    return False


# =========================================================
# 9. FINAL CAREER SCORE
# =========================================================
def calculate_career_score(student,career,career_kb,final_career_skills):
    career_row = career_kb[career_kb["career_path"] == career].iloc[0]
    # Education → 15%
    edu_score = education_score(student["education"],career_row["education"])
    # Branch → 15%
    branch_score_value = branch_score(student["branch"],career_row["preferred_branches"])
    # Grade Point → 15%
    gp_score = grade_score(student["grade_point"])

    # Core + Advanced Skills
    (core_skill_score,advanced_skill_score,matched_core,matched_advanced) = calculate_skill_scores(
        student["skills"],career,final_career_skills)

    # Certification → 5%
    cert_score = certification_score(student["certifications"],career)
    # Interest → 10%
    interest_score_value = interest_score(student["interest"],career,career_kb)

    # Final Score
    total_score = (edu_score * 0.15+branch_score_value * 0.15+gp_score * 0.15+core_skill_score * 0.30
    +advanced_skill_score * 0.10+cert_score * 0.05+interest_score_value * 0.10)

    return round(total_score,2)


# =========================================================
# 10. RECOMMEND CAREERS
# =========================================================

def recommend_careers(student,career_kb,final_career_skills,top_n=5):
    career_scores = []
    for career in career_kb["career_path"]:
        # Career relevance filter
        if not career_relevance(student,career,career_kb,final_career_skills):
            continue

        # Calculate score
        score = calculate_career_score(student,career,career_kb,final_career_skills)
        career_scores.append([career,score])

    recommendations = pd.DataFrame(career_scores,columns=["career_path","score"])

    if recommendations.empty:
        return recommendations

    recommendations = (recommendations.sort_values("score",ascending=False).head(top_n).reset_index(drop=True))
    return recommendations

# =========================================================
# 11. SKILL GAP
# =========================================================

def get_skill_gap(career,student_skills,final_career_skills):
    required = set(final_career_skills[final_career_skills["career_path"] == career]["skill"])
    student = set(normalize_skill(skill)for skill in student_skills)
    matched = student.intersection(required)
    missing = required - student
    return matched, missing
