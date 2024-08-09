## loading all the environment variables
from dotenv import load_dotenv
load_dotenv() 

# Import Important libraries
import streamlit as st
import google.generativeai as genai
import os

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the Model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192
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

# Load Gemini Pro model
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Navbar
st.set_page_config(
    page_title="SEO Guest Posting Generator",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Add the Title
st.markdown(
    "<h1 style='text-align: center; color: black;'>"
    "✨ SEO Guest Posting Generator"
    "</h1>",
    unsafe_allow_html=True
)

#st.title('✨ AI Blog Section Generator')

# create a subheader
st.markdown('''
<style>
h3 {
    font-family: 'Open Sans', sans-serif;
    font-size: 18px;
    line-height: 0px;
    margin-top: 0;
    margin-bottom: 24px;
    text-align: center;
    display: flex;
    justify-content: center;
}
</style>
<h3 style="text-align: center; color: black; font-weight: 300; font-style: italic;">💥&nbsp;&nbsp;Powered by: AppJingle Solutions&nbsp;&nbsp;💥</h3>
''', unsafe_allow_html=True)

# sidebar for the user input

with st.sidebar:
    st.markdown(
        "<style>h1 {text-align: center;}</style>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<style>h1 {text-align: center; color: black;}</style>",
        unsafe_allow_html=True
    )
    st.title("Input Settings")

    st.markdown(
        "<style>"
        "h4 {text-align: left; color: black; margin-top: 4px;}"
        "p {text-align: left; color: black;}"
        "</style>",
        unsafe_allow_html=True
    )
    st.markdown("<h4>Enter Details for the Article: </h4>", unsafe_allow_html=True)
    
    # Section Heading
    primary_heading = st.text_input("Primary Keyword (required)")
    
    # Primary Keyword
    keywords = st.text_input("Recommended Keywords (comma-separated)")
    
    # Subpoints
    
    #subpoints = st.text_area("Subpoints (comma-separated)")
    
    # Add the Voice Tones
    voice_tones = st.sidebar.selectbox("Choose Voice Tones:", ["Formal", "Informal", "Friendly", "Bold", "Adventurous", "Witty", "Professional", "Casual", "Informative", "Creative", "Trendy", "Caring", "Cheerful", "Excited", "Funny", "Sad", "Serious", "Tense", "Vulnerable", "Angry", "Surprised", "Worried", "Assertive", "Confident", "Cooperative", "Encouraging" ])
    
    # Add the Writing Styles
    writing_styles = st.sidebar.selectbox("Choose Writing Styles:", ["Academic", "Conversational", "Creative", "Critical", "Descriptive", "Instructive", "Technical", "Analytical","Business", "Causal", "Emotional", "Expository", "Formal", "Informal", "Legal", "Medical", "Poetic", "Persuasive"])
    
    # Audience
    audience = st.selectbox("Audience: Who is the target audience?", ["Digital Marketers", "General Audience", "Everyone", "Uninformed Audience", "Industry Experts", "Neutral Audience", "Business Owners and Entrepreneurs", "Researcher", "Expert Audience", "Potential Clients", "Tech", "Academic", "Teenager", "Adult", "20-years-old", "30-years-old",  "40-years-old", "50-years-old"] )
    
    num_words = st.number_input("Number of words", min_value=1250, max_value=3000, step=250)
    
    # Secondary Keyword
    #secondary_keyword = st.text_input("Secondary Keyword")
    
    # Reference Article Link
    # reference_article_link = st.text_input("Reference Article Link")

    # Prompt
    prompt_parts = [
            f"""
                Forget all previous instructions.
                    Assume the role of a proficient article writer fluent in English. Your task is to compose a {num_words}-word article on {primary_heading} that effectively capture the attention of the {audience} audience. Also Optimize this article for keyword {keywords}.
                    Here are the instructions to follow:
                    1. Use a {voice_tones} tone using {writing_styles} writing style, don't use jargon and complex terms like showcase, leverage, delve, craft etc. Make use of personal pronouns, rhetorical questions, and at least one relevant analogy or metaphor.
                    2. The content should be original to avoid plagiarism. Also, ensure it doesn't appear AI-generated.
                    3. Apply Markdown language and Heading tags (H1 for the main title, H2 for headings, and Strong or bold tags for subheadings) to enhance readability and SEO. 
                    Compose a meta title (up to 60 characters) and a meta description (up to 160 characters) which are engaging and relevant to the topic.
                    4. Use 'Plush dog toys' in meta description.
                    Following the introduction, include a Table of Contents (TOC) in a table format with two columns: 1. Sr# 2. Headings. Write must be 10-15 headings, relevant subheadings and explain them in detail. Develop engaging, detailed paragraphs using these headings and subheadings. The introduction and conclusion paragraph should not be more than 10% of text.
                    Conclude the article and follow up with five pertinent FAQs (with answers) relevant to the topic. Ensure each question ends with a question mark (?).
                    The goal is to produce valuable content that engages readers and satisfies SEO needs. Bold the headings, subheadings and keypoints.
            """
            ]

import streamlit as st
import io

# Initialize session state variables if they do not exist
if 'response' not in st.session_state:
    st.session_state.response = None

# Add the Clear all button
clear_button = st.sidebar.button("Clear All")
if clear_button:
    st.session_state.clear()
    st.experimental_rerun()  # This ensures the page is rerun to reflect the cleared state

# Sidebar Submit Button
submit_button = st.sidebar.button("Generate")

if submit_button and 'response' in st.session_state and not clear_button:
    # Display the spinner
    with st.spinner("Generating...."):
        # Generate the response
        response = model.generate_content(prompt_parts)
        # Store the response in session state
        st.session_state.response = response.text

# Write results if response is available
if st.session_state.response:
    st.write(st.session_state.response)

    # Download file option
    with open("keyword_analysis.txt", "w", encoding="utf-8") as f:
        f.write(st.session_state.response)
    st.download_button(
        label="Download File",
        data=io.BytesIO(st.session_state.response.encode("utf-8")).getvalue(),
        file_name='keyword_analysis.txt',
        mime='text/plain',
    )

    # Add styling to the generated text
    st.markdown('''
        <style>
            p {
                font-family: 'Open Sans', sans-serif;
                font-size: 16px;
                line-height: 24px;
                margin-top: 0;
                margin-bottom: 24px;
            }
            strong {
                font-weight: 600;
            }
            em {
                font-style: italic;
            }
            code {
                background-color: #f5f5f5;
                border-radius: 3px;
                display: inline-block;
                font-family: 'Menlo', monospace;
                font-size: 14px;
                margin: 0 1px;
                padding: 2px 4px;
            }
        </style>
    ''', unsafe_allow_html=True)
    
    
    
# Adding the HTML footer
# Profile footer HTML for sidebar


# Render profile footer in sidebar at the "bottom"
# Set a background image
def set_background_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.pexels.com/photos/4097159/pexels-photo-4097159.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1);
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_image()

# Set a background image for the sidebar
sidebar_background_image = '''
<style>
[data-testid="stSidebar"] {
    background-image: url("https://www.pexels.com/photo/abstract-background-with-green-smear-of-paint-6423446/");
    background-size: cover;
}
</style>
'''

st.sidebar.markdown(sidebar_background_image, unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Custom CSS to inject into the Streamlit app
footer_css = """
<style>
.footer {
    position: fixed;
    right: 0;
    bottom: 0;
    width: auto;
    background-color: transparent;
    color: black;
    text-align: right;
    padding-right: 10px;
}
</style>
"""


# HTML for the footer - replace your credit information here
footer_html = f"""
<div class="footer">
    <p style="font-size: 12px; font-style: italic; color: gray; margin-bottom: 0px; opacity: 0.7; line-height: 1.2; text-align: center;">
        <span style="display: block; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px; font-family: 'Open Sans', sans-serif;">Developed by::</span>
        <span style="font-size: 20px; font-weight: 800; text-transform: uppercase; font-family: 'Open Sans', sans-serif;">Farhan Akbar</span>
    </p>
    <a href="https://www.linkedin.com/in/farhan-akbar-ai/"><img src="https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin" alt="LinkedIn"/></a>
    <a href="https://api.whatsapp.com/send?phone=923034532403"><img src="https://img.shields.io/badge/WhatsApp-Chat%20Me-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp"/></a>
    <a href="https://www.facebook.com/appjingle"><img src="https://img.shields.io/badge/Facebook-Connect-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"/></a>
    <a href="mailto:rasolehri@gmail.com"><img src="https://img.shields.io/badge/Email-Contact%20Me-red?style=for-the-badge&logo=email" alt="Email"/></a>
</div>
"""

# Combine CSS and HTML for the footer
st.markdown(footer_css, unsafe_allow_html=True)
st.markdown(footer_html, unsafe_allow_html=True)     

