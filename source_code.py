
import io
import re
from datetime import datetime
from xml.sax.saxutils import escape

import streamlit as st
import pdfplumber
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ResumeIQ | AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PROFESSIONAL WHITE UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #ffffff !important;
    color: #1e293b !important;
}

[data-testid="stHeader"] {
    background-color: #ffffff !important;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #172b4d !important;
}

p, label, .stMarkdown {
    color: #475569;
}

/* Hero section */
.hero {
    background: linear-gradient(120deg, #edf3ff, #dce8ff);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 1.5rem;
    border: 1px solid #d8e3f5;
}

.hero h1 {
    color: #172b4d !important;
    font-size: 2.7rem;
    font-weight: 750;
    letter-spacing: -1px;
    margin-bottom: .7rem;
}

.hero p {
    color: #526581 !important;
    font-size: 1.1rem;
    line-height: 1.6;
}

/* Branding row */
.brand-row {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 10px 0 25px;
    border-bottom: 2px solid #e2e8f0;
    margin-bottom: 25px;
}

.brand-icon {
    background: #344f86;
    width: 70px;
    height: 70px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    flex-shrink: 0;
}

.brand-name {
    color: #172b4d;
    font-size: 2rem;
    font-weight: 750;
    line-height: 1.2;
}

.brand-tagline {
    font-size: .95rem;
    letter-spacing: 1px;
    color: #64748b;
    margin-top: 8px;
}

.dashboard-pill {
    margin-left: auto;
    padding: 8px 16px;
    background: #e6f7ef;
    color: #087443;
    border-radius: 30px;
    font-size: 1rem;
    font-weight: 600;
}

/* Input cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #f8faff !important;
    border: 1px solid #e2e8f3 !important;
    border-radius: 18px !important;
    padding: 16px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #f8faff;
    border: 1px dashed #b7c9e7;
    border-radius: 14px;
    padding: 1rem;
}

[data-testid="stFileUploader"] section {
    background: #ffffff !important;
    border: 1px dashed #b7c9e7 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] * {
    color: #334155;
}

/* Text area */
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 14px !important;
    font-size: 1rem !important;
}

.stTextArea textarea::placeholder {
    color: #94a3b8 !important;
}

/* Buttons */
.stButton > button {
    background: #7899f4 !important;
    color: #102044 !important;
    border: none !important;
    border-radius: 14px !important;
    min-height: 58px;
    font-size: 1.15rem !important;
    font-weight: 750 !important;
    transition: all .2s ease;
}


/* Light blue upload button */
[data-testid="stFileUploader"] button {
    background-color: #dbeafe !important;
    color: #1d4ed8 !important;
    border: 1px solid #93c5fd !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploader"] button:hover {
    background-color: #bfdbfe !important;
    color: #1e40af !important;
    border-color: #60a5fa !important;
}

}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #f8faff !important;
    border: 1px solid #e2e8f3 !important;
    border-radius: 16px !important;
    padding: 1.15rem !important;
    box-shadow: 0 4px 15px rgba(25, 47, 88, .04);
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
}

div[data-testid="stMetricValue"] {
    color: #23477f !important;
    font-weight: 750 !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #475569 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #315b96 !important;
}

/* Progress bar */
div[data-testid="stProgressBar"] > div > div {
    background: #5378bd !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: #ffffff !important;
    color: #23477f !important;
    border: 1px solid #b8c9e5 !important;
    border-radius: 12px !important;
    min-height: 46px;
}

.stDownloadButton > button:hover {
    background: #edf3ff !important;
    border-color: #5378bd !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Dividers */
hr {
    border-color: #e2e8f0 !important;
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 1.3rem;
    }

    .hero h1 {
        font-size: 2rem;
    }

    .brand-icon {
        width: 55px;
        height: 55px;
        font-size: 27px;
    }

    .brand-name {
        font-size: 1.5rem;
    }

    .dashboard-pill {
        display: none;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# SKILL VOCABULARY
# =========================================================

SKILLS = [
    "Python", "Java", "C++", "SQL", "HTML", "CSS",
    "JavaScript", "React", "Node.js", "Machine Learning",
    "Artificial Intelligence", "Data Analysis", "Excel",
    "Communication", "Leadership", "Problem Solving",
    "Teamwork", "Git", "GitHub", "Streamlit", "Flask",
    "Django", "Pandas", "NumPy", "Power BI", "Tableau",
    "Data Structures", "Algorithms", "Cloud Computing",
    "Networking", "Cybersecurity", "Software Testing",
    "Operating Systems", "Database Management", "PHP",
    "MongoDB", "MySQL", "API", "Object-Oriented Programming",
    "OOP", "Deep Learning"
]


# =========================================================
# RESUME SECTION PATTERNS
# =========================================================

SECTIONS = {
    "Contact Information":
        r"email|phone|mobile|linkedin|github|portfolio",

    "Summary / Objective":
        r"summary|objective|profile",

    "Education":
        r"education|academic|qualification|university|college|degree",

    "Skills":
        r"skills|technical skills|core competencies",

    "Projects":
        r"projects|project experience|academic projects",

    "Experience":
        r"experience|employment|internship|work history",

    "Certifications":
        r"certifications|certificates|licenses"
}


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def extract_text(uploaded_file):
    """Extract text from a PDF or TXT resume."""

    if uploaded_file is None:
        return ""

    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                pages = [
                    page.extract_text() or ""
                    for page in pdf.pages
                ]
            return "\n".join(pages).strip()

        if uploaded_file.name.lower().endswith(".txt"):
            return uploaded_file.getvalue().decode(
                "utf-8",
                errors="ignore"
            ).strip()

    except Exception as error:
        st.error(f"Unable to read the file: {error}")

    return ""


def find_skills(text):
    """Find skills from the predefined vocabulary."""

    found = []
    text_lower = text.lower()

    for skill in SKILLS:
        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text_lower):
            found.append(skill)

    if (
        "Object-Oriented Programming" in found
        and "OOP" in found
    ):
        found.remove("OOP")

    return found


def find_sections(text):
    """Identify common resume sections."""

    found = []

    for section, pattern in SECTIONS.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(section)

    return found


def get_suggestions(text, skills, sections):
    """Generate rule-based resume improvement suggestions."""

    suggestions = []
    word_count = len(text.split())

    if word_count < 80:
        suggestions.append(
            "Your resume is quite short. Add relevant projects, "
            "education, and practical experience."
        )

    if "Summary / Objective" not in sections:
        suggestions.append(
            "Add a short professional summary or career objective."
        )

    if "Education" not in sections:
        suggestions.append(
            "Include your degree, college, and graduation year."
        )

    if "Skills" not in sections:
        suggestions.append(
            "Create a clearly labelled Skills section."
        )

    if "Projects" not in sections:
        suggestions.append(
            "Add projects, tools used, and your contribution."
        )

    if "Experience" not in sections:
        suggestions.append(
            "If applicable, include internships or practical experience."
        )

    if len(skills) < 5:
        suggestions.append(
            "Include relevant skills you genuinely possess."
        )

    if not re.search(
        r"\d+%|\b\d+\s*(users|projects|years|clients)\b",
        text,
        re.IGNORECASE
    ):
        suggestions.append(
            "Where accurate, quantify achievements with measurable results."
        )

    if not suggestions:
        suggestions.append(
            "Good work! Tailor your resume to each role and keep "
            "all information accurate."
        )

    return suggestions


def calculate_score(text, skills, sections):
    """Calculate a rule-based checklist score out of 100."""

    score = min(len(skills) * 3, 25)
    score += min(len(sections) * 5, 35)

    word_count = len(text.split())

    if 150 <= word_count <= 900:
        score += 20
    elif 80 <= word_count < 150 or 900 < word_count <= 1200:
        score += 12
    elif word_count > 0:
        score += 5

    if re.search(r"\S+@\S+\.\S+", text):
        score += 5

    if re.search(
        r"project|experience|internship",
        text,
        re.IGNORECASE
    ):
        score += 5

    if re.search(
        r"\d+%|\b\d+\s*(users|projects|years|clients)\b",
        text,
        re.IGNORECASE
    ):
        score += 10

    return min(score, 100)


def job_match(resume_text, job_text):
    """Compare recognized skills in the resume and job description."""

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_text)

    resume_set = {skill.lower() for skill in resume_skills}

    matched = [
        skill for skill in job_skills
        if skill.lower() in resume_set
    ]

    missing = [
        skill for skill in job_skills
        if skill.lower() not in resume_set
    ]

    if not job_skills:
        return None, matched, missing

    score = round(len(matched) / len(job_skills) * 100)

    return score, matched, missing


# =========================================================
# PDF REPORT
# =========================================================

def create_pdf_report(data):
    """Create a downloadable PDF analysis report."""

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ResumeIQTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#23477f"),
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name="ResumeIQHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#315b96"),
        spaceBefore=12,
        spaceAfter=6
    ))

    story = [
        Paragraph("ResumeIQ Analysis Report", styles["ResumeIQTitle"]),
        Paragraph(
            "Generated: " + datetime.now().strftime("%d %B %Y, %I:%M %p"),
            styles["Normal"]
        ),
        Spacer(1, 12),
        Paragraph("Resume Overview", styles["ResumeIQHeading"]),
        Paragraph(f"Resume checklist score: {data['score']}/100", styles["Normal"]),
        Paragraph(f"Word count: {data['words']}", styles["Normal"]),
        Paragraph(
            "Detected skills: " +
            escape(", ".join(data["skills"]) or "None detected"),
            styles["BodyText"]
        ),
        Paragraph(
            "Detected sections: " +
            escape(", ".join(data["sections"]) or "None detected"),
            styles["BodyText"]
        )
    ]

    if data["job_score"] is not None:
        story.extend([
            Paragraph("Job Description Match", styles["ResumeIQHeading"]),
            Paragraph(
                f"Recognized-skill overlap: {data['job_score']}%",
                styles["Normal"]
            ),
            Paragraph(
                "Matched skills: " +
                escape(", ".join(data["matched"]) or "None"),
                styles["BodyText"]
            ),
            Paragraph(
                "Skills not detected: " +
                escape(", ".join(data["missing"]) or "None"),
                styles["BodyText"]
            )
        ])

    story.append(
        Paragraph("Improvement Suggestions", styles["ResumeIQHeading"])
    )

    for suggestion in data["suggestions"]:
        story.append(Paragraph("• " + escape(suggestion), styles["BodyText"]))
        story.append(Spacer(1, 5))

    story.extend([
        Spacer(1, 12),
        Paragraph("Important Note", styles["ResumeIQHeading"]),
        Paragraph(
            "Scores are based on predefined rules and a fixed skill "
            "vocabulary. They are not hiring predictions. Review all "
            "results manually.",
            styles["BodyText"]
        )
    ])

    document.build(story)
    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="brand-row">
    <div class="brand-icon">📄</div>
    <div>
        <div class="brand-name">ResumeIQ</div>
        <div class="brand-tagline">YOUR CAREER, REFINED</div>
    </div>
    <div class="dashboard-pill">Dashboard</div>
</div>

<div class="hero">
    <h1>Build a resume that opens doors.</h1>
    <p>
        Analyze your resume, uncover skill gaps, and tailor
        your profile to your next opportunity.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# INPUTS
# =========================================================

with st.container(border=True):
    st.markdown("### 📤 Upload your resume")

    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=["pdf", "txt"],
        key="resume_upload"
    )

    st.caption("PDF or TXT · Upload your resume for analysis")


with st.container(border=True):
    st.markdown("### 🎯 Target job description")

    job_description = st.text_area(
        "Paste the target job description",
        height=120,
        placeholder=(
            "Python developer with SQL, Git, data analysis, "
            "and problem-solving skills..."
        ),
        label_visibility="collapsed",
        key="job_description"
    )

st.write("")

analyze = st.button(
    "✦ Analyze My Resume",
    type="primary",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    if uploaded_file is None:
        st.warning("Please upload a PDF or TXT resume first.")

    else:
        resume_text = extract_text(uploaded_file)

        if not resume_text:
            st.error(
                "No readable text was found. Try a text-based PDF "
                "or upload a TXT file."
            )

        else:
            skills = find_skills(resume_text)
            sections = find_sections(resume_text)

            suggestions = get_suggestions(
                resume_text,
                skills,
                sections
            )

            score = calculate_score(
                resume_text,
                skills,
                sections
            )

            job_score = None
            matched = []
            missing = []

            if job_description.strip():
                job_score, matched, missing = job_match(
                    resume_text,
                    job_description
                )

            st.session_state["analysis"] = {
                "score": score,
                "words": len(resume_text.split()),
                "skills": skills,
                "sections": sections,
                "suggestions": suggestions,
                "job_score": job_score,
                "matched": matched,
                "missing": missing
            }

            st.session_state["filename"] = uploaded_file.name


# =========================================================
# RESULTS
# =========================================================

if "analysis" in st.session_state:

    data = st.session_state["analysis"]

    st.divider()
    st.header("📊 Your Analysis Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("RESUME SCORE", f"{data['score']}/100")
    col2.metric("WORD COUNT", f"{data['words']:,}")
    col3.metric("SKILLS DETECTED", len(data["skills"]))
    col4.metric("SECTIONS DETECTED", len(data["sections"]))

    st.progress(
        data["score"] / 100,
        text="Resume checklist score"
    )

    st.caption(
        "This rule-based score measures detected resume content. "
        "It does not predict hiring or interview success."
    )

    tab1, tab2, tab3 = st.tabs([
        "🧰 Skills & Sections",
        "🎯 Job Match",
        "💡 Suggestions"
    ])

    with tab1:
        left, right = st.columns(2)

        with left:
            st.subheader("Detected Skills")

            if data["skills"]:
                for skill in data["skills"]:
                    st.write(f"✅ {skill}")
            else:
                st.info("No predefined skills were detected.")

        with right:
            st.subheader("Resume Sections")

            for section in SECTIONS:
                if section in data["sections"]:
                    st.write(f"✅ {section}")
                else:
                    st.write(f"○ {section}")

    with tab2:
        if data["job_score"] is None:
            st.info(
                "Add a job description above and click Analyze My Resume "
                "to compare your skills."
            )

        else:
            st.metric(
                "RECOGNIZED-SKILL OVERLAP",
                f"{data['job_score']}%"
            )

            st.progress(data["job_score"] / 100)

            st.caption(
                "This percentage compares recognized skills only. "
                "It is not a hiring probability."
            )

            left, right = st.columns(2)

            with left:
                st.subheader("Matched Skills")

                if data["matched"]:
                    for skill in data["matched"]:
                        st.write(f"✅ {skill}")
                else:
                    st.write("No recognized skills matched.")

            with right:
                st.subheader("Skills Not Detected")

                if data["missing"]:
                    for skill in data["missing"]:
                        st.write(f"🔎 {skill}")
                else:
                    st.write("All recognized job skills were detected.")

    with tab3:
        st.subheader("Suggestions to Improve Your Resume")

        for suggestion in data["suggestions"]:
            st.markdown(f"- {suggestion}")

    # Downloads
    st.divider()
    st.header("📥 Download Your Report")

    pdf_report = create_pdf_report(data)

    download_col1, download_col2 = st.columns(2)

    with download_col1:
        st.download_button(
            "⬇️ Download PDF Report",
            data=pdf_report,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    text_report = f"""
RESUMEIQ ANALYSIS REPORT

File: {st.session_state.get('filename', 'resume')}
Generated: {datetime.now().strftime('%d %B %Y')}

RESUME OVERVIEW
Resume checklist score: {data['score']}/100
Word count: {data['words']}

DETECTED SKILLS
{', '.join(data['skills']) or 'None detected'}

DETECTED SECTIONS
{', '.join(data['sections']) or 'None detected'}

JOB DESCRIPTION MATCH
{
    str(data['job_score']) + '%'
    if data['job_score'] is not None
    else 'Not assessed'
}

MATCHED SKILLS
{', '.join(data['matched']) or 'None'}

SKILLS NOT DETECTED
{', '.join(data['missing']) or 'None'}

IMPROVEMENT SUGGESTIONS
""" + "\n".join(
        "- " + suggestion
        for suggestion in data["suggestions"]
    ) + """

IMPORTANT
Scores are rule-based indicators, not hiring predictions.
"""

    with download_col2:
        st.download_button(
            "⬇️ Download Text Report",
            data=text_report,
            file_name="resume_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "ResumeIQ | Built with Python and Streamlit | Educational mini-project"
)
