
import streamlit as st

from src.resume_parser import extract_text_from_pdf
from src.matcher import calculate_similarity
from src.skill_extractor import extract_skills


# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="ResumeMatch AI",
    page_icon="🎯",
    layout="wide",
)


# --------------------------------------------------
# App header
# --------------------------------------------------
st.title("🎯 ResumeMatch AI")
st.write(
    "AI-powered resume and job description matching system."
)
st.divider()


# --------------------------------------------------
# User inputs
# --------------------------------------------------
st.header("1️⃣ Upload Your Resume")

resume_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
)

st.header("2️⃣ Paste Job Description")

job_description = st.text_area(
    "Job Description",
    height=300,
    placeholder="Paste the job description here...",
)


# --------------------------------------------------
# Analyze resume
# --------------------------------------------------
if st.button("🚀 Analyze Match", type="primary"):

    if resume_file is None:
        st.error("Please upload your resume.")

    elif not job_description.strip():
        st.error("Please paste the job description.")

    else:
        try:
            with st.spinner("Analyzing your resume..."):

                # Extract resume text
                resume_text = extract_text_from_pdf(resume_file)

                if not resume_text.strip():
                    st.error(
                        "No readable text was found in this PDF. "
                        "It may be a scanned document."
                    )
                    st.stop()

                # Calculate semantic similarity
                semantic_score = calculate_similarity(
                    resume_text,
                    job_description,
                )

                # Extract normalized skills
                resume_skills = extract_skills(resume_text)
                job_skills = extract_skills(job_description)

                # Compare skills
                matched_skills = sorted(
                    set(resume_skills) & set(job_skills)
                )

                missing_skills = sorted(
                    set(job_skills) - set(resume_skills)
                )

                # Calculate skill coverage
                if job_skills:
                    skill_score = round(
                        len(matched_skills)
                        / len(job_skills)
                        * 100,
                        2,
                    )
                else:
                    skill_score = 0.0

                # Overall score: equal weighting
                overall_score = round(
                    (semantic_score + skill_score) / 2,
                    2,
                )

            # --------------------------------------------------
            # Results
            # --------------------------------------------------
            st.success("Analysis complete!")
            st.header("📊 Match Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🎯 Overall Match Score",
                    f"{overall_score:.2f}%",
                )

            with col2:
                st.metric(
                    "🧠 Semantic Similarity",
                    f"{semantic_score:.2f}%",
                )

            with col3:
                st.metric(
                    "🛠️ Skill Match Score",
                    f"{skill_score:.2f}%",
                )

            st.caption(
                "The overall score equally averages semantic similarity "
                "and detected skill coverage. It is experimental and "
                "does not predict hiring success."
            )

            st.divider()

            # --------------------------------------------------
            # Skill coverage chart
            # --------------------------------------------------
            st.header("📈 Skill Coverage")

            total_skills = len(job_skills)
            matched_count = len(matched_skills)
            missing_count = len(missing_skills)

            if total_skills > 0:
                chart_data = {
                    "Category": [
                        "Matched Skills",
                        "Missing Skills",
                    ],
                    "Count": [
                        matched_count,
                        missing_count,
                    ],
                }

                st.bar_chart(
                    chart_data,
                    x="Category",
                    y="Count",
                    horizontal=True,
                  )

                st.write(
                    f"**Coverage:** {matched_count} of "
                    f"{total_skills} detected job skills matched."
                )

            else:
                st.info(
                    "No recognized skills were found in the job description."
                )

            st.divider()

            # --------------------------------------------------
            # Matched skills
            # --------------------------------------------------
            st.header("✅ Matched Skills")

            if matched_skills:
                st.write(
                    f"Found {matched_count} matching skills."
                )

                for skill in matched_skills:
                    st.write(f"✅ {skill}")
            else:
                st.info(
                    "No matching skills were detected."
                )

            st.divider()

            # --------------------------------------------------
            # Missing skills
            # --------------------------------------------------
            st.header("❌ Missing Skills")

            if missing_skills:
                st.write(
                    f"{missing_count} recognized job skills "
                    "were not detected in your resume."
                )

                for skill in missing_skills:
                    st.write(f"❌ {skill}")

            elif job_skills:
                st.success(
                    "All detected job skills were found in your resume!"
                )

            else:
                st.info(
                    "No skills from the current skill database "
                    "were detected in the job description."
                )

            st.divider()

            # --------------------------------------------------
            # Detailed skill lists
            # --------------------------------------------------
            with st.expander("🔍 View All Detected Skills"):

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Resume Skills")
                    st.write(resume_skills)

                with col2:
                    st.subheader("Job Description Skills")
                    st.write(job_skills)

            # --------------------------------------------------
            # Extracted resume text
            # --------------------------------------------------
            with st.expander("📄 View Extracted Resume Text"):
                st.text_area(
                    "Resume content",
                    resume_text,
                    height=300,
                    disabled=True,
                )

        except Exception as error:
            st.error(
                "An error occurred while analyzing your resume."
            )
            st.exception(error)
