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
        page_title="Alwrity - AI Business Email Writer (Beta)",
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
    st.title("✍️ Alwrity - AI Business Email Writer (Beta)")


    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        col1, col2, space = st.columns([5, 5, 0.5])
        with col1:
            # Email Type/Purpose
            email_type = st.selectbox("**Select Business Email Type**", ["Sales Pitch", "Customer Service", "Partnership Proposal", "Project Update"])
        with col2:
            # Email Category Selection
            if email_type == "Sales Pitch":
                product_service_name = st.text_input("Product/Service Name")
                target_audience = st.text_input("**Target Audience**")
            elif email_type == "Customer Service":
                issue_description = st.text_area("**Customer Issue Description**")
            elif email_type == "Partnership Proposal":
                partner_company_name = st.text_input("**Partner Company Name**")
                collaboration_objective = st.text_area("**Collaboration Objective**")
            elif email_type == "Project Update":
                project_name = st.text_input("**Project Name**")
                key_achievements = st.text_area("**Key Achievements**")
            
        # Generate Blog FAQ button
    if st.button('**Write Business Email**'):
        with st.status("Assigning a AI professional to write your Email..", expanded=True) as status:
            if email_type == "Sales Pitch":
                if not product_service_name or not target_audience:
                    st.error("🚫 Error: Enter all the details, least you can do..")
                else:
                    response = sales_pitch_writer(product_service_name, target_audience, status)
                    if response:
                        st.subheader(f'**🧕 Alwrity can make mistakes. Your Final Email for Sales Pitch!**')
                        st.write(response)
                    else:
                        st.write("💥**Failed to write Email. Please try again!**")
            elif email_type == "Customer Service":
                if not issue_description:
                    st.error("🚫 Error: Enter all the details, least you can do..")
                else:
                    response = customer_service_writer(issue_description, status)
                    if response:
                        st.subheader(f'**🧕 Alwrity can make mistakes. Your Final Email for Customer Service!**')
                        st.write(response)
                    else:
                        st.write("💥**Failed to write Email. Please try again!**") 
            if email_type == "Partnership Proposal":
                if not partner_company_name or not collaboration_objective:
                    st.error("🚫 Error: Enter all the details, least you can do..")
                else:
                    response = partnership_proposal_writer(partner_company_name, collaboration_objective, status)
                    if response:
                        st.subheader(f'**🧕 Alwrity can make mistakes. Your Final Email for Partnership Proposal!**')
                        st.write(response)
                        st.write("\n\n\n")
                    else:
                        st.write("💥**Failed to write Email. Please try again!**")
            elif email_type == "Project Update":
                if not project_name and not key_achievements:
                    st.error("🚫 Error: Enter all the details, least you can do..")
                else:
                    response = project_update_writer(project_name, key_achievements, status)
                    if response:
                        st.subheader(f'**🧕 Alwrity can make mistakes. Your Final Email for Project update!**')
                        st.write(response)
                    else:
                        st.write("💥**Failed to write Email. Please try again!**")


def sales_pitch_writer(product_service_name, target_audience, status):
    """AI email sales pitch writer"""

    prompt = f"""
        **Product/Service:** {product_service_name}
        **Target Audience:** {target_audience}

        **Instructions:**

        * Write a persuasive email introducing the product/service and its key benefits. 
        * Focus on how the product/service solves pain points or addresses the needs of the target audience.
        * Use a confident and enthusiastic tone. 
        * Include a call to action to learn more or make a purchase.
    """
    status.update(label="Writing Your Sales Pitch...")
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def customer_service_writer(issue_description, status):
    """ Email customer_service_writer"""

    prompt = f"""
        **Issue Description:**

        {issue_description}

        **Instructions:**

        * Write a professional and empathetic email addressing the customer's issue. 
        * Acknowledge the problem and express understanding of the customer's frustration.
        * Offer a solution or explanation to resolve the issue.
        * Ensure a positive and helpful tone.
    """
    status.update(label="Writing Customer Service Email...")
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def partnership_proposal_writer(partner_company_name, collaboration_objective, status):
    """ Email partnership_proposal_writer"""

    prompt = f"""
        **Subject:** Partnership Proposal: Collaboration between [Your_Company] and {partner_company_name}

        **Body:**

        We are writing to propose a partnership between our companies, [Your_Company] and {partner_company_name}. 
        We believe that a collaboration would be mutually beneficial for the following reasons: 

        {collaboration_objective}

        **Instructions:**

        * Write a formal email outlining the proposed partnership. 
        * Clearly state the objectives and potential benefits of the collaboration for both parties.
        * Highlight the strengths and expertise that each company brings to the partnership.
        * Propose next steps for discussion and further exploration of the partnership.
    """
    status.update(label="Writing Partnership Proposal Email...")
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def project_update_writer(project_name, key_achievements, status):
    """ Email project_update_writer """

    prompt = f"""
        **Project:** {project_name}

        **Key Achievements:**

        {key_achievements}

        **Instructions:**

        * Write a concise and informative email summarizing the project's progress. 
        * Highlight key achievements and milestones reached. 
        * Provide a brief overview of next steps and future plans.
        * Maintain a professional and positive tone.
    """
    status.update(label="Writing Project update Email...")
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
