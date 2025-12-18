import streamlit as st
import os
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup
import json
import re
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("⚠️ GOOGLE_API_KEY not found in environment variables!")

# Page configuration
st.set_page_config(
    page_title="Job Auto Formatter",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark mode styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        transition: background-color 0.3s;
    }
    .result-box {
        background-color: #1E1E1E;
        color: #FAFAFA;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border: 1px solid #333333;
    }
    /* Dark mode text input styling */
    .stTextInput>div>div>input {
        background-color: #262730;
        color: #FAFAFA;
    }
    /* Footer styling */
    .footer {
        color: #888888;
    }
    .footer a {
        color: #FF4B4B;
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def shorten_url(url: str):
    """Shorten URL using TinyURL"""
    try:
        tinyurl_api = f"https://tinyurl.com/api-create.php?url={url}"
        short_url = requests.get(tinyurl_api, timeout=5).text
        
        if short_url.lower() == "error":
            return url
        return short_url
    except:
        return url

def normalize_experience(experience_text: str, role: str = "") -> str:
    """Normalize experience text to standard format"""
    if not experience_text:
        return "Fresher"
    
    exp_lower = experience_text.lower()
    role_lower = role.lower()
    
    # Check role first (intern, internship, graduate, fresher, entry level)
    if any(keyword in role_lower for keyword in ["intern", "internship", "graduate", "fresher", "entry level", "entry-level"]):
        return "Fresher"
    
    # Check for explicit years mentioned
    import re
    years_pattern = r'(\d+)[\s-]+(?:to|-|or more|\+)[\s-]*(\d+)?[\s-]*years?'
    years_match = re.search(years_pattern, exp_lower)
    
    if years_match:
        min_years = int(years_match.group(1))
        max_years = years_match.group(2)
        
        if max_years:
            max_years = int(max_years)
            if min_years <= 1:
                return "0-1 years"
            elif min_years <= 2:
                return "0-2 years"
            elif min_years <= 3:
                return "2-3 years"
            else:
                return "3+ years"
        else:
            # Pattern like "3+ years" or "5 or more years"
            if min_years >= 5:
                return "5+ years"
            elif min_years >= 3:
                return "3+ years"
            elif min_years >= 2:
                return "2-3 years"
            elif min_years >= 1:
                return "0-2 years"
            else:
                return "0-1 years"
    
    # Check for keywords in experience text
    if any(keyword in exp_lower for keyword in ["fresher", "entry level", "entry-level", "no experience", "0 years"]):
        return "Fresher"
    
    if "intern" in exp_lower or "internship" in exp_lower or "graduate" in exp_lower or "pursuing" in exp_lower:
        return "Fresher"
    
    if "senior" in exp_lower or "lead" in exp_lower or "principal" in exp_lower:
        return "5+ years"
    
    if "mid-level" in exp_lower or "mid level" in exp_lower or "experienced" in exp_lower:
        return "3+ years"
    
    if "junior" in exp_lower or "associate" in exp_lower:
        return "0-2 years"
    
    # If no clear indication, check if it mentions specific years
    if re.search(r'\d+[\s-]+years?', exp_lower):
        # Extract number
        num_match = re.search(r'(\d+)[\s-]+years?', exp_lower)
        if num_match:
            years = int(num_match.group(1))
            if years >= 5:
                return "5+ years"
            elif years >= 3:
                return "3+ years"
            elif years >= 2:
                return "2-3 years"
            elif years >= 1:
                return "0-2 years"
            else:
                return "0-1 years"
    
    # Default: if it's an intern/graduate role or mentions "pursuing", it's fresher
    if "pursuing" in exp_lower or "phd" in exp_lower or "student" in exp_lower:
        return "Fresher"
    
    # If we can't determine, default to Fresher for safety
    return "Fresher"

def format_job_message(data):
    """Format job data into message template"""
    # Normalize experience to standard format
    experience = normalize_experience(
        data.get('experience', ''), 
        data.get('role', '')
    )
    
    return f"""
**COMPANY** : {data.get('company', '')}
**ROLE** : {data.get('role', '')}
**LOCATION** : {data.get('location', '')}
**EXPERIENCE** : {experience}

**Apply Link:** {data.get('apply_link', '')}

For More Job Updates & Important Updates Like this  
Follow Us On WhatsApp :  
https://whatsapp.com/channel/0029VagenEZFSAtDBtDg9v2y

Reach us at  
telugucodingcommunity88@gmail.com

Please Share With Your College Groups & Friends
""".strip()

def clean_ai_json(ai_text: str):
    """Clean and parse AI response JSON"""
    ai_text = ai_text.replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{.*\}", ai_text, re.DOTALL)
    if not match:
        return {}
    
    json_text = match.group(0)
    try:
        return json.loads(json_text)
    except:
        return {}

def fetch_dynamic_html(url: str):
    """Fetch dynamic HTML using Playwright for JavaScript-rendered pages"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            html = page.content()
            browser.close()
            return html
    except Exception as e:
        st.error(f"Dynamic fetch error: {e}")
        return ""

def extract_job_details(url: str):
    """Extract job details from URL"""
    try:
        # 1. Download HTML
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        html = response.text

        # 2. Clean text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        
        # If text is too short (likely LinkedIn), use Playwright fallback
        if len(text) < 300:
            with st.spinner("Fetching dynamic content (this may take 30-60 seconds)..."):
                dynamic_html = fetch_dynamic_html(url)
                if dynamic_html:
                    soup = BeautifulSoup(dynamic_html, "html.parser")
                    text = soup.get_text(separator=" ", strip=True)

                    # Extract only the real job description on LinkedIn
                    job_desc_div = soup.find("div", {"data-test-job-description": True})
                    if job_desc_div:
                        text = job_desc_div.get_text(separator=" ", strip=True)

        # 3. Gemini Prompt
        prompt = f"""
            You will receive raw webpage text extracted from a job posting page.

            Your task:
            1. Read the text.
            2. Identify the *actual job description section*.
            3. Ignore everything else (navigation, recommendations, ads, footers, unrelated content).
            4. Extract these 5 fields:

            - company: Company name
            - role: Job title/position
            - location: Job location (city, state/country)
            - experience: Extract the experience/qualification requirements from the job description. Return the full text about experience, years required, or qualifications. Include keywords like "intern", "fresher", "senior", years mentioned, etc.
            - apply_link: Application URL (if not found, return "")

            STRICT RULES:
            - Return ONLY a pure JSON.
            - No comments, no markdown, no explanation.
            - For experience field: Return the complete experience/qualification text from the job description (we will process and normalize it in code).

            TEXT BELOW:
            {text}

            OUTPUT JSON FORMAT:
            {{
            "company": "",
            "role": "",
            "location": "",
            "experience": "",
            "apply_link": ""
            }}
            """

        if not GEMINI_API_KEY:
            raise Exception("Google API key not configured")

        model = genai.GenerativeModel("models/gemini-2.5-flash")
        ai_response = model.generate_content(prompt)
        cleaned_json = clean_ai_json(ai_response.text)

        # Auto-fill missing apply_link
        apply_link = cleaned_json.get("apply_link", "")
        if not apply_link:
            apply_link = url

        # Shorten the link
        short_link = shorten_url(apply_link)
        cleaned_json["apply_link"] = short_link

        # Normalize experience field before formatting
        cleaned_json["experience"] = normalize_experience(
            cleaned_json.get("experience", ""),
            cleaned_json.get("role", "")
        )

        formatted_message = format_job_message(cleaned_json)
        
        return {
            "status": "success",
            "formatted_message": formatted_message,
            "parsed_output": cleaned_json
        }

    except Exception as e:
        import traceback
        error_details = str(e)
        st.error(f"Error: {error_details}")
        return {
            "status": "error",
            "message": error_details
        }

# Main App
def main():
    st.title("💼 Job Auto Formatter")
    st.markdown("---")
    
    # Input section
    url = st.text_input(
        "Paste job link here...",
        placeholder="https://linkedin.com/jobs/view/...",
        key="job_url"
    )
    
    # Generate button
    if st.button("🚀 Generate Job Post", type="primary"):
        if not url:
            st.warning("⚠️ Please enter a valid job link.")
        elif not GEMINI_API_KEY:
            st.error("❌ Google API key not configured. Please set GOOGLE_API_KEY environment variable.")
        else:
            with st.spinner("🔄 Processing... This may take 30-60 seconds..."):
                result = extract_job_details(url)
                
                if result["status"] == "success":
                    # Store in session state
                    st.session_state['formatted_message'] = result["formatted_message"]
                    st.session_state['parsed_output'] = result["parsed_output"]
                    st.success("✅ Job post generated successfully!")
                else:
                    st.error(f"❌ Error: {result.get('message', 'Failed to extract job details')}")
    
    # Display result
    if 'formatted_message' in st.session_state and st.session_state['formatted_message']:
        st.markdown("---")
        st.subheader("📋 Formatted Job Post")
        
        # Display formatted message
        st.markdown(f"<div class='result-box'>{st.session_state['formatted_message'].replace(chr(10), '<br>').replace('**', '<strong>').replace('**', '</strong>')}</div>", unsafe_allow_html=True)
        
        # Copy button
        if st.button("📋 Copy to Clipboard"):
            st.code(st.session_state['formatted_message'], language=None)
            st.success("✅ Copied to clipboard! (You can also select and copy the text above)")
        
        # Show parsed data in expander
        with st.expander("🔍 View Extracted Data"):
            st.json(st.session_state.get('parsed_output', {}))
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class='footer' style='text-align: center; color: #888888; padding: 1rem;'>
        <p>For More Job Updates & Important Updates</p>
        <p>Follow Us On WhatsApp: <a href='https://whatsapp.com/channel/0029VagenEZFSAtDBtDg9v2y' target='_blank' style='color: #FF4B4B;'>Join Channel</a></p>
        <p>Reach us at: telugucodingcommunity88@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
