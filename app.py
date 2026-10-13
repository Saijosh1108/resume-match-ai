
import streamlit as st

from src.resume_parser import extract_text_from_pdf
from src.matcher import calculate_similarity
from src.skill_extractor import extract_skills
from src.recommendations import generate_recommendations


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
st.caption(
    "Compare your resume with a job description, identify skill gaps, "
    "and discover ways to strengthen your application."
)

st.info(
    "This tool uses semantic similarity and dictionary-based skill "
    "detection. It does not predict hiring outcomes or understand every "
    "possible job requirement."
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
    placeholder="Paste the complete job description here...",
)


# --------------------------------------------------
# Analyze resume
# --------------------------------------------------
if st.button("🚀 Analyze Match", type="primary"):

    if resume_file is None:
        st.error("Please upload your resume.")

    elif not job_description.strip():
        st.error("Please paste a job description.")

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

                # Compare recognized skills
                resume_skill_set = set(resume_skills)
                job_skill_set = set(job_skills)

                matched_skills = sorted(
                    resume_skill_set & job_skill_set
                )

                missing_skills = sorted(
                    job_skill_set - resume_skill_set
                )

                # Calculate skill coverage
                total_job_skills = len(job_skill_set)
                matched_count = len(matched_skills)
                missing_count = len(missing_skills)

                if total_job_skills > 0:
                    skill_score = round(
                        matched_count / total_job_skills * 100,
                        2,
                    )
                    overall_score = round(
                        (semantic_score + skill_score) / 2,
                        2,
                    )
                else:
                    skill_score = None
                    overall_score = None

                # Generate recommendations
                recommendations = generate_recommendations(
                    resume_skills,
                    job_skills,
                    missing_skills,
                )

            # --------------------------------------------------
            # Match results
            # --------------------------------------------------
            st.success("Analysis complete!")
            st.header("📊 Match Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                if overall_score is not None:
                    st.metric(
                        "🎯 Overall Match Score",
                        f"{overall_score:.2f}%",
                    )
                else:
                    st.metric(
                        "🎯 Overall Match Score",
                        "N/A",
                    )

            with col2:
                st.metric(
                    "🧠 Semantic Similarity",
                    f"{semantic_score:.2f}%",
                )

            with col3:
                if skill_score is not None:
                    st.metric(
                        "🛠️ Skill Match Score",
                        f"{skill_score:.2f}%",
                    )
                else:
                    st.metric(
                        "🛠️ Skill Match Score",
                        "N/A",
                    )

            st.caption(
                "The overall score equally averages semantic similarity "
                "and recognized skill coverage. It is an experimental "
                "metric, not a prediction of hiring success."
            )

            st.divider()

            # --------------------------------------------------
            # Skill coverage summary
            # --------------------------------------------------
            st.header("📈 Skill Coverage")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Recognized Job Skills",
                    total_job_skills,
                )

            with col2:
                st.metric(
                    "Matched Skills",
                    matched_count,
                )

            with col3:
                st.metric(
                    "Missing Skills",
                    missing_count,
                )

            if total_job_skills > 0:
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
                    f"**Recognized skill coverage:** {matched_count} "
                    f"of {total_job_skills} detected job skills matched."
                )

                st.warning(
                    "This percentage covers only skills recognized by "
                    "the current dictionary. Requirements not included "
                    "in the dictionary are excluded from the calculation."
                )

            else:
                st.warning(
                    "No skills from the current dictionary were detected "
                    "in the job description. A skill match score cannot "
                    "be calculated reliably. Try a more detailed job "
                    "description or interpret semantic similarity separately."
                )

            st.divider()

            # --------------------------------------------------
            # Matched skills
            # --------------------------------------------------
            st.header("✅ Matched Skills")

            if matched_skills:
                st.write(
                    f"Found {matched_count} matching recognized skills."
                )

                for skill in matched_skills:
                    st.write(f"✅ {skill}")

            else:
                st.info("No matching skills were detected.")

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

            elif total_job_skills > 0:
                st.success(
                    "All detected job skills were found in your resume."
                )

            else:
                st.info(
                    "No recognized job skills are available to compare."
                )

            st.divider()

            # --------------------------------------------------
            # Resume improvement suggestions
            # --------------------------------------------------
            st.header("💡 Resume Improvement Suggestions")

            st.write(
                "Use these suggestions to improve how your relevant "
                "experience is presented. Only include skills and "
                "experience you genuinely have."
            )

            if recommendations:
                for i, recommendation in enumerate(
                    recommendations,
                    start=1,
                ):
                    st.markdown(
                        f"**{i}.** {recommendation}"
                    )
            else:
                st.info(
                    "No recommendations are available for this analysis."
                )

            st.divider()

            # --------------------------------------------------
            # All detected skills
            # --------------------------------------------------
            with st.expander("🔍 View All Detected Skills"):

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Resume Skills")
                    st.write(resume_skills or "No recognized skills found.")

                with col2:
                    st.subheader("Job Description Skills")
                    st.write(job_skills or "No recognized skills found.")

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

