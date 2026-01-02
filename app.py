import streamlit as st
from src.pdf_parser import extract_text_from_pdf
from src.matcher import match_resume_job
from src.skill_scoring import weighted_skill_breakdown
from src.resume_recommender import resume_recommendations

st.set_page_config(page_title="AI Resume Matcher", layout="centered")

st.title(" AI Resume Matcher & Job Fit Analyzer")
st.write("Upload your resume and paste a job description to see how well you match.")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description", height=200)

if st.button(" Analyze Fit"):
    if resume_file is None or not job_description.strip():
        st.error("Please upload a resume and paste a job description.")
    else:
        resume_text = extract_text_from_pdf(resume_file)

        result = match_resume_job(resume_text, job_description)
        breakdown = weighted_skill_breakdown(resume_text, job_description)

        st.subheader(" Match Result")

        st.metric("Skill Detection Accuracy", f"{result['skill_match_percentage']:.2f}%")

        weighted_match_pct = breakdown["score"]   
        st.metric("Overall Match Percentage", f"{weighted_match_pct:.2f}%")
        st.progress(min(int(weighted_match_pct), 100))

        if result["fit_label"] == "Good Fit":
            st.success(result["fit_label"])
        elif result["fit_label"] == "Partial Fit":
            st.warning(result["fit_label"])
        else:
            st.error(result["fit_label"])


        st.write(result["recommendation"])

        st.subheader(" Matched Skills (Weighted)")
        if breakdown["matched"]:
            for skill in breakdown["matched"]:
                st.write(f"• {skill}")
        else:
            st.write("No matched skills.")

        st.subheader(" Missing Skills (Weighted)")
        if breakdown["missing"]:
            for skill in breakdown["missing"]:
                st.write(f"• {skill}")
        else:
            st.write("No major missing skills.")

        st.subheader(" Category-wise Score")
        for cat, val in breakdown["category_scores"].items():
            st.write(f"{cat}: {val}")

        st.subheader(" Resume Improvement Suggestions")
        for rec in resume_recommendations(breakdown["missing"]):
            st.write(f"• {rec}")
