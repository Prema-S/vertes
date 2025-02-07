import pandas as pd
from typing import List
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the JSON file (Fixing path issue)
json_file_path = os.path.join(os.path.dirname(__file__), "marks.json")

if os.path.exists(json_file_path):
    df = pd.read_json(json_file_path)
else:
    df = pd.DataFrame()  # Empty DataFrame if file is missing

@app.get("/api")
def get_students(class_: List[str] = Query(default=[], alias="class_")):
    """
    API to fetch student data based on class filter.
    Example: /api?class_=10&class_=12
    """
    if df.empty:
        return JSONResponse({"error": "marks.json file not found or empty"}, status_code=500)

    # Filter by class if specified
    filtered_df = df[df['class'].isin(class_)] if class_ else df

    # Convert the DataFrame to a list of dictionaries
    students_data = filtered_df.to_dict(orient='records')

    return JSONResponse({"students": students_data})
