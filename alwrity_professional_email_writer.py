import time #Iwish
import os
import json
import requests
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import google.generativeai as genai


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity - AI Professional Email Writer (Beta)",
        layout="wide",
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f"""
      <style>
      [class="st-emotion-cache-7ym5gk ef3psqc12"]{{
            display: inline-block;
            padding: 5px 20px;
            background-color: #4681f4;
            color: #FBFFFF;
            width: 300px;
            height: 35px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 8px;’
      }}
      </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ Alwrity - AI Professional Email Writer")


    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        col1, col2, space = st.columns([5, 5, 0.5])
        with col1:
            email_type = st.selectbox("**Select Professional Email Type**", ["Job Application", "Meeting Request", "Follow-Up Email", "Networking Email"])
        with col2:
            # Email Type Selection and Input Fields based on Category
            if email_type == "Job Application":
                position_name = st.text_input("**Enter Position Name, Applying for**")
                company_name = st.text_input("**Enter Company Name, Applying to**")
                skills_experience = st.text_area("**Enter Skills and Experiences to highlight**")

            elif email_type == "Meeting Request":
                meeting_topic = st.text_input("**Enter Meeting Topic**")
                proposed_dates = st.text_input("**Proposed Dates/Times**")
            elif email_type == "Follow-Up Email":
                previous_topic = st.text_input("**Previous Topic Discussed**")
                previous_context = st.text_input("**Optional: Enter last meeting highlights to remind Receiver**")
            elif email_type == "Networking Email":
                reason_for_connecting = st.text_area("**Enter Reason for Connecting & Networking:**")
                user_name = st.text_input("**Enter Name to include in Email:**")
                user_profession = st.text_input("**Enter your Profession to Use in Email:**")
            
    # Generate Blog FAQ button
    if st.button('**Write Professional Email**'):
        with st.status("Assigning a AI professional to write your Email..", expanded=True) as status:
            if email_type == "Job Application":
                if not position_name or not company_name or not skills_experience:
                    st.error("🚫 Error: Enter all the details, least you can do..")
                else:
                    response = professional_writer(position_name, company_name, skills_experience, status)
                    if response:
                        st.subheader(f'**🧕🔬👩 Alwrity can make mistakes. Your Final Email for Job Application!**')
                        st.write(response)
                    else:
                        st.write("💥**Failed to write professional email. Please try again!**")
            elif email_type == "Meeting Request":
                if not meeting_topic and not proposed_dates:
                    st.error("🚫 Error: Enter all the details, least you can do..")
                else:
                    response = meeting_request_writer(meeting_topic, proposed_dates, status)
                    if response:
                        st.subheader(f'**🧕🔬👩 Alwrity can make mistakes. Your Final Email for Meeting Request!**')
                        st.write(response)
                    else:
                        st.write("💥**Failed to write meeting request email. Please try again!**")
            elif email_type == "Follow-Up Email":
                if not previous_topic:
                    st.error("🚫 Error: Enter all the details, least you can do..")
                else:
                    response = followup_writer(previous_topic, status)
                    if response:
                        st.subheader(f'**🧕🔬👩 Alwrity can make mistakes. Your Final followUp Email!**')
                        st.write(response)
                    else:
                        st.write("💥**Failed to write meeting request email. Please try again!**")
            elif email_type == "Networking Email":
                if not reason_for_connecting:
                    st.error("🚫 Error: Enter all the details, least you can do..")
                else:
                    response = networking_writer(user_name, user_profession, reason_for_connecting, status)
                    if response:
                        st.subheader(f'**🧕🔬👩 Alwrity can make mistakes. Your Final Networking Email!**')
                        st.write(response)
                    else:
                        st.write("💥**Failed to write meeting request email. Please try again!**")


def professional_writer(position_name, company_name, skills_experience, status):
    """Combine the given online research and gpt blog content"""

    prompt = f"""
        **Position:** {position_name}
        **Company:** {company_name}

        **Skills and Experience:**

        {skills_experience}

        **Instructions:**

        * Write a compelling cover letter highlighting the applicant's qualifications for the position.
        * Focus on relevant skills and experience that match the job requirements. 
        * Use a professional and enthusiastic tone.
    """
    status.update(label="Writing Professional Job Application...")
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def meeting_request_writer(meeting_topic, proposed_dates, status):
    """Combine the given online research and gpt blog content"""

    prompt = f"""
        **Subject:** Meeting Request: {meeting_topic}


        **Body:**

        I would like to schedule a meeting to discuss {meeting_topic}. 
        Please let me know if you are available on any of the following dates/times:
        * {proposed_dates}

        **Instructions:**

        * Write a formal email requesting a meeting. 
        * Briefly explain the purpose of the meeting.
        * Suggest specific dates and times for the meeting.
    """
    status.update(label="Writing Professional Meeting request Email...")
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def followup_writer(previous_topic, status):
    """Combine the given online research and gpt blog content"""

    prompt = f"""
        **Subject:** Following Up: {previous_topic}

        **Body:**

        I hope this email finds you well. I am following up on our previous conversation regarding {previous_topic}. 

        **Instructions:**

        * Write a polite and professional follow-up email.
        * Briefly remind the recipient of the previous topic discussed. 
        * Inquire about the next steps or any updates.
    """
    status.update(label="Writing Professional Follow Up Email...")
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def networking_writer(user_name, user_profession, reason_for_connecting, status):
    """Combine the given online research and gpt blog content"""

    prompt = f"""
        **Subject:** Introduction: {user_name} - {user_profession}

        **Body:**

        I hope this email finds you well. 
        My name is {user_name} and I am a {user_profession}. 
        I am reaching out to you today because {reason_for_connecting}.

        **Instructions:**

        * Write a professional introduction email.
        * Briefly explain the reason for connecting and express your interest in the recipient's work or company. 
        * Keep the tone respectful and avoid being overly self-promotional.
    """
    status.update(label="Writing Professional Networking Email...")
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()
