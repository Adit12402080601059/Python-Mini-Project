# Python-Mini-Project
Python Mini Project Submission
# ResumeIQ — AI-Powered Resume Analyzer

ResumeIQ is a Python and Streamlit mini-project that analyzes resumes and helps compare a resume with a job description. It is designed as an educational project and uses rule-based text analysis rather than a trained machine-learning model.

## Features

- Upload a resume in PDF or TXT format.
- Extract and review resume text.
- Detect selected skills and common resume sections.
- Provide a rule-based resume analysis score and improvement suggestions.
- Paste a job description to identify matched and missing skills.
- Generate downloadable analysis reports where supported by the app.

## Tech Stack

- Python
- Streamlit
- pdfplumber — PDF text extraction
- ReportLab — PDF report generation

## Project Files

- `streamlit_interface.py` — main Streamlit application (run this file if it is the entry point in your project).
- `requirements.txt` — Python dependencies.
- `README.md` — project overview and setup instructions.
- `sample_data/` — fictional sample resumes and matching job descriptions for testing.

> If your local main file has a different name, replace `streamlit_interface.py` in the run command with that filename.

## Setup and Run

1. Install Python 3.9 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. (Optional but recommended) Create and activate a virtual environment.

   **macOS/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

5. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the app:

   ```bash
   streamlit run streamlit_interface.py
   ```

7. Streamlit will show a local URL in the terminal, usually `http://localhost:8501`. Open it in your browser.

## How to Test

1. Upload one of the `.txt` resumes in `sample_data/`.
2. If testing job matching, open the matching job description file and paste its text into the app's job-description field.
3. Review the detected skills, matched/missing skills, score, and suggestions.
4. Try another resume to compare results across different fields.

## Sample Data

The `sample_data/` folder contains four fictional resumes from different career areas and a matching job description for each:

- Software Developer
- Data Analyst
- UI/UX Designer
- Digital Marketing Specialist

All names and contact details are fictional placeholders. Do not use these documents as real credentials.

## Limitations

- Results depend on the skills and sections recognized by the current implementation.
- Keyword overlap and rule-based scoring do not guarantee job suitability or hiring outcomes.
- The project is intended for learning and demonstration; it should not be used as the sole basis for recruitment decisions.

## Future Enhancements

- Expand the skill dictionary and support more roles.
- Improve extraction and handling of varied resume layouts.
- Add configurable scoring and more detailed feedback.
- Explore semantic matching in a future version.

## Author

Created as an educational mini-project.
