import joblib
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# Load Model
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "pickles" / "marksmodel.pkl"
with open(MODEL_PATH, "rb") as file:
    model = joblib.load(file)
SCALER_PATH = BASE_DIR / "pickles" / "marksscaler.pkl"
with open(SCALER_PATH, "rb") as file:
    scaler = joblib.load(file)

# ---------------------------------------------------------
# Predict Final Marks
# ---------------------------------------------------------
def predict_final_marks(attendance,studyhours,assignmentscore,internaltestscore):
    data = pd.DataFrame({"Attendance%": [attendance],"DailyStudyHours": [studyhours],
    "AssignmentScore": [assignmentscore],"InternalTestScore": [internaltestscore]})

    data.iloc[:,:] = scaler.transform(data.iloc[:,:])
    prediction = model.predict(data)
    return float(prediction[0])

# ---------------------------------------------------------
# Final Marks → Grade Point
# ---------------------------------------------------------
def marks_to_grade_point(final_marks):
    if final_marks >= 90:
        return 10
    elif final_marks >= 80:
        return 9
    elif final_marks >= 70:
        return 8
    elif final_marks >= 60:
        return 7
    elif final_marks >= 50:
        return 6
    elif final_marks >= 40:
        return 5
    else:
        return 0