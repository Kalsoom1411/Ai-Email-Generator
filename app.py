
import gradio as gr
from google.colab import userdata
from groq import Groq


# ==========================================
# GET API KEY FROM COLAB SECRET
# ==========================================

api_key = userdata.get("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found in Colab Secrets."
    )

client = Groq(api_key=api_key)


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

    if not purpose or not purpose.strip():
        return "⚠️ Please describe what you want the email to be about."

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

    except Exception as e:

        return (
            "❌ Unable to generate email.\n\n"
            "Please try again."
        )


# ==========================================
# CLEAR FUNCTION
# ==========================================

def clear_fields():

    return (
        "Internship Request",
        "",
        "Professional",
        "Medium",
        "English",
        "",
        "",
        ""
    )


# ==========================================
# GRADIO APPLICATION
# ==========================================

with gr.Blocks(
    title="AI Email Generator"
) as demo:

    gr.Markdown(
        """
        # ✉️ AI Email Generator

        ### Generate professional emails with AI in seconds

        Write better emails without starting from scratch.
        """
    )

    with gr.Row():

        # ----------------------------------
        # INPUT SECTION
        # ----------------------------------

        with gr.Column(scale=1):

            gr.Markdown("### 📝 Email Details")

            email_type = gr.Dropdown(
                choices=[
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
                ],
                label="Email Type",
                value="Internship Request"
            )

            recipient = gr.Textbox(
                label="Recipient",
                placeholder="e.g. HR Manager"
            )

            tone = gr.Dropdown(
                choices=[
                    "Professional",
                    "Formal",
                    "Friendly",
                    "Polite",
                    "Casual"
                ],
                label="Tone",
                value="Professional"
            )

            length = gr.Dropdown(
                choices=[
                    "Short",
                    "Medium",
                    "Detailed"
                ],
                label="Email Length",
                value="Medium"
            )

            language = gr.Dropdown(
                choices=[
                    "English",
                    "Urdu",
                    "Roman Urdu"
                ],
                label="Language",
                value="English"
            )

            purpose = gr.Textbox(
                label="What is the email about?",
                placeholder=(
                    "e.g. I want to apply for a "
                    "frontend development internship."
                ),
                lines=4
            )

            additional_details = gr.Textbox(
                label="Additional Details",
                placeholder="Add any important information here...",
                lines=4
            )

            with gr.Row():

                generate_btn = gr.Button(
                    "✨ Generate Email",
                    variant="primary"
                )

                clear_btn = gr.Button(
                    "🔄 Clear"
                )


        # ----------------------------------
        # OUTPUT SECTION
        # ----------------------------------

        with gr.Column(scale=1):

            gr.Markdown("### 📧 Generated Email")

            output = gr.Textbox(
                label="Your AI-generated email",
                placeholder=(
                    "Your generated email will appear here..."
                ),
                lines=22
            )


    # ======================================
    # GENERATE EVENT
    # ======================================

    generate_btn.click(
        fn=generate_email,
        inputs=[
            email_type,
            recipient,
            tone,
            length,
            language,
            purpose,
            additional_details
        ],
        outputs=output
    )


    # ======================================
    # CLEAR EVENT
    # ======================================

    clear_btn.click(
        fn=clear_fields,
        inputs=[],
        outputs=[
            email_type,
            recipient,
            tone,
            length,
            language,
            purpose,
            additional_details,
            output
        ]
    )


    # ======================================
    # FOOTER
    # ======================================

    gr.Markdown(
        """
        ---
        **🤖 AI Email Generator**
        
        Powered by **Groq + Gradio**
        """
    )


# ==========================================
# LAUNCH
# ==========================================

demo.launch(share=True)
