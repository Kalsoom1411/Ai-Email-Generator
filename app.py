import streamlit as st
from groq import Groq

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="wide"
)

# ==========================================
# GET API KEY FROM STREAMLIT SECRETS
# ==========================================

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("GROQ_API_KEY is not configured in Streamlit Secrets.")
    st.stop()


# ==========================================
# EMAIL GENERATOR
# ==========================================

def generate_email(
    email_type,
    recipient,
    tone,
    length,
    language,
    purpose,
    additional_details
):

    prompt = f"""
You are a professional AI email writing assistant.

Generate a clear, natural and professional email.

Email Type:
{email_type}

Recipient:
{recipient}

Tone:
{tone}

Email Length:
{length}

Language:
{language}

Purpose:
{purpose}

Additional Details:
{additional_details}

Instructions:
- Create a suitable email subject.
- Write the complete email.
- Follow the requested tone.
- Follow the requested email length.
- Write in the requested language.
- Keep the email natural and professional.
- Do not explain your process.
- Do not add unnecessary information.
- Use [Your Name] where appropriate.

Return only:

Subject: [subject]

[Email body]
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert professional email writer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_completion_tokens=1000
        )

        return response.choices[0].message.content

    except Exception:
        return "❌ Unable to generate email. Please try again."


# ==========================================
# USER INTERFACE
# ==========================================

st.title("✉️ AI Email Generator")
st.write("### Generate professional emails with AI in seconds")
st.write("Write better emails without starting from scratch.")

st.divider()

col1, col2 = st.columns(2)

# ==========================================
# INPUT SECTION
# ==========================================

with col1:

    st.subheader("📝 Email Details")

    email_type = st.selectbox(
        "Email Type",
        [
            "Internship Request",
            "Job Application",
            "Leave Request",
            "Meeting Request",
            "Thank You Email",
            "Complaint Email",
            "Apology Email",
            "Follow-up Email",
            "Scholarship Request",
            "University Email",
            "Recommendation Request",
            "Project Collaboration",
            "Networking Email",
            "Business Inquiry",
            "General Professional Email"
        ]
    )

    recipient = st.text_input(
        "Recipient",
        placeholder="e.g. HR Manager"
    )

    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Formal",
            "Friendly",
            "Polite",
            "Casual"
        ]
    )

    length = st.selectbox(
        "Email Length",
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Urdu",
            "Roman Urdu"
        ]
    )

    purpose = st.text_area(
        "What is the email about?",
        placeholder="e.g. I want to apply for a frontend development internship.",
        height=120
    )

    additional_details = st.text_area(
        "Additional Details",
        placeholder="Add any important information here...",
        height=120
    )

    generate_button = st.button(
        "✨ Generate Email",
        type="primary",
        use_container_width=True
    )


# ==========================================
# OUTPUT SECTION
# ==========================================

with col2:

    st.subheader("📧 Generated Email")

    if generate_button:

        if not purpose.strip():
            st.warning("⚠️ Please describe what you want the email to be about.")

        else:

            with st.spinner("Generating your email..."):

                result = generate_email(
                    email_type,
                    recipient,
                    tone,
                    length,
                    language,
                    purpose,
                    additional_details
                )

            st.text_area(
                "Your AI-generated email",
                value=result,
                height=500
            )

    else:

        st.info(
            "Your generated email will appear here."
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption("🤖 AI Email Generator — Powered by Groq + Streamlit")
