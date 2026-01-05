import streamlit as st
import os
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import json
import re

# Load environment variables from .env file (for local development)
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Job Auto Formatter",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.75rem;
    }
    .stButton>button:hover {
        background-color: #333333;
    }
    .result-box {
        background-color: #f7f7f7;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Gemini API
def init_gemini():
    """Initialize Gemini API with key from environment or Streamlit secrets"""
    api_key = None
    
    # First, try environment variable (for local development)
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # If not found, try Streamlit secrets (for Streamlit Cloud)
    if not api_key:
        try:
            # Only access secrets if it exists (avoids error when secrets.toml doesn't exist)
            if hasattr(st, 'secrets'):
                # Check if secrets dict exists and has the key
                if st.secrets and 'GOOGLE_API_KEY' in st.secrets:
                    api_key = st.secrets['GOOGLE_API_KEY']
        except Exception:
            # If secrets access fails (e.g., no secrets.toml file), ignore and continue
            pass
    
    if not api_key:
        st.error("⚠️ Google API Key not found.")
        st.info("""
        **For local development:**
        - Create a `.env` file in the project root
        - Add: `GOOGLE_API_KEY=your_api_key_here`
        - Or set it as an environment variable
        
        **For Streamlit Cloud:**
        - Go to Settings → Secrets
        - Add: `GOOGLE_API_KEY = "your_api_key_here"`
        """)
        st.stop()
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring Gemini API: {str(e)}")
        st.stop()

# Initialize on first run
if 'gemini_initialized' not in st.session_state:
    init_gemini()
    st.session_state.gemini_initialized = True

def shorten_url(url: str):
    """Shorten URL using TinyURL API"""
    try:
        tinyurl_api = f"https://tinyurl.com/api-create.php?url={url}"
        short_url = requests.get(tinyurl_api, timeout=5).text
        
        # TinyURL returns literally "Error" on failure
        if short_url.lower() == "error":
            return url  # fallback to original link
        
        return short_url
    except:
        return url  # fallback if API fails

def normalize_experience(experience_text: str):
    """Normalize experience text to standard format while preserving original format when possible."""
    if not experience_text or experience_text.strip() == "":
        return "nothing is mentioned"
    
    exp_lower = experience_text.lower().strip()
    
    # Handle "nothing is mentioned" case
    if exp_lower in ['nothing is mentioned', 'not mentioned', 'not specified', 'not found', 'n/a', 'na']:
        return "nothing is mentioned"
    
    # Handle "yoe" or "fresher" defaults
    if exp_lower in ['yoe', 'fresher']:
        return "fresher"
    
    # If already in normalized format, return as is (preserve original case for common formats)
    normalized_formats = ['fresher', '1-2', '2-3', '3-4', '4-5', '2+', '3+', '4+', '5+', '1+', '6+']
    if exp_lower in normalized_formats:
        # Preserve original format but capitalize "Fresher"
        if exp_lower == 'fresher':
            return "Fresher"
        return experience_text.strip()
    
    # Check for fresher/intern/new grad patterns
    if any(keyword in exp_lower for keyword in ['fresher', 'intern', 'new grad', 'entry level', '0 years', 'no experience', 'no prior experience', 'graduate']):
        return "Fresher"
    
    # Check for senior/lead without years (infer 5+)
    if any(keyword in exp_lower for keyword in ['senior', 'lead', 'principal', 'architect']) and 'years' not in exp_lower:
        # Only if no years mentioned
        if not re.search(r'\d+\s*years?', exp_lower):
            return "5+"
    
    # Check for specific year ranges like "1-2 years", "2-3 years", etc.
    range_match = re.search(r'(\d+)\s*[-–to]\s*(\d+)', experience_text, re.IGNORECASE)
    if range_match:
        min_years = int(range_match.group(1))
        max_years = int(range_match.group(2))
        if min_years == 0:
            return "Fresher"
        else:
            return f"{min_years}-{max_years}"
    
    # Look for "X+ years" or "X+ years of experience" patterns - preserve the format
    plus_match = re.search(r'(\d+)\s*\+', experience_text)
    if plus_match:
        years = int(plus_match.group(1))
        return f"{years}+"
    
    # Look for "minimum X years", "at least X years"
    min_match = re.search(r'(?:minimum|at least|min\.?)\s*(\d+)\s*years?', exp_lower)
    if min_match:
        years = int(min_match.group(1))
        return f"{years}+"
    
    # Look for single year requirement like "2 years", "3 years"
    single_match = re.search(r'(\d+)\s+years?', experience_text)
    if single_match:
        years = int(single_match.group(1))
        if years == 0:
            return "Fresher"
        elif years == 1:
            return "1-2"
        elif years == 2:
            return "2+"
        else:
            return f"{years}+"
    
    # If we can't parse but there's some text, try to preserve it or default to "nothing is mentioned"
    if len(experience_text.strip()) > 0:
        # If it contains any number, try to extract it
        any_number = re.search(r'\d+', experience_text)
        if any_number:
            # Return the original text if it seems valid
            return experience_text.strip()
        return "nothing is mentioned"
    
    # Final fallback
    return "nothing is mentioned"

def format_job_message(data):
    """Format job data into the standard message format"""
    company = data.get('company', '')
    role = data.get('role', '')
    location = data.get('location', '')
    experience = data.get('experience', '')
    
    # Normalize experience format (with fallback to "nothing is mentioned")
    if not experience or experience.strip() == "":
        experience = "nothing is mentioned"
    else:
        experience = normalize_experience(experience)
    
    return f"""
*COMPANY* : {company}
*ROLE* : {role}
**LOCATION** : {location}
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
    """Extract and clean JSON from AI response"""
    # Remove code block markers
    ai_text = ai_text.replace("```json", "").replace("```", "").strip()
    
    # Extract JSON using regex (safer)
    match = re.search(r"\{.*\}", ai_text, re.DOTALL)
    if not match:
        return {}
    
    json_text = match.group(0)
    
    try:
        return json.loads(json_text)
    except:
        return {}

def fetch_dynamic_html(url: str):
    """Fetch HTML from dynamic pages using Playwright"""
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
        st.warning(f"Dynamic fetch error: {e}")
        return ""

def extract_job_details(url: str):
    """Extract job details from URL using AI"""
    try:
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📥 Downloading webpage...")
        progress_bar.progress(20)
        
        # 1. Download HTML
        response = requests.get(url, timeout=10)
        html = response.text
        
        status_text.text("🧹 Cleaning and parsing HTML...")
        progress_bar.progress(40)
        
        # 2. Clean text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        
        # If text is too short (likely LinkedIn), use Playwright fallback
        if len(text) < 300:
            status_text.text("🌐 Using browser automation for dynamic content...")
            progress_bar.progress(50)
            dynamic_html = fetch_dynamic_html(url)
            if dynamic_html:
                soup = BeautifulSoup(dynamic_html, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                
                # Extract only the real job description on LinkedIn
                job_desc_div = soup.find("div", {"data-test-job-description": True})
                if job_desc_div:
                    text = job_desc_div.get_text(separator=" ", strip=True)
        
        status_text.text("🤖 Extracting job details with AI...")
        progress_bar.progress(60)
        
        # 3. Gemini Prompt
        prompt = f"""
            You will receive raw webpage text extracted from a job posting page.

            Your task:
            1. Read the ENTIRE text carefully - scan the whole page content.
            2. Identify the *actual job description section* and ALL relevant sections.
            3. Ignore navigation, recommendations, ads, footers, but scan ALL job-related content.
            4. Extract these 5 fields:

            - company: The company name
            - role: The job title/position name
            - location: Job location (city, state, country)
            - experience: CRITICAL - Scan the ENTIRE page for experience requirements. Extract the EXACT experience requirement as mentioned in the job description.
              Look for ANY mention of experience requirements including:
              - "X years of experience" or "X+ years of experience" → return exactly as mentioned (e.g., "2+ years", "2+", "2 years")
              - "X-Y years" or "X to Y years" → return exactly as mentioned (e.g., "2-3 years", "2-3")
              - "minimum X years", "at least X years" → return "X+" or the exact format
              - "entry level", "fresher", "intern", "new grad", "0 years", "no experience required" → return "Fresher"
              - "senior", "lead", "principal" positions → check if years are mentioned, if not, return "5+"
              - "YOE" (years of experience) mentions → extract the number/range mentioned
              IMPORTANT: 
              * Scan the ENTIRE page content, not just a section
              * Extract the EXACT format as mentioned in JD (preserve "2+ years", "2+", "2-3 years", etc.)
              * If multiple experience requirements are mentioned, use the primary/required one
              * If nothing is explicitly mentioned about experience after scanning the entire page, return "nothing is mentioned"
            - apply_link: The application URL (if not found, return "")

            STRICT RULES:
            - Return ONLY a pure JSON.
            - No comments, no markdown, no explanation.
            - For experience: Extract the EXACT format as mentioned in the JD. Preserve formats like "2+ years", "2+", "2-3", etc.
            - If experience is not mentioned anywhere after scanning the entire page, return "nothing is mentioned" (not empty string, not "fresher", not "yoe").

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
        
        status_text.text("⚡ Processing with Gemini AI...")
        progress_bar.progress(80)
        
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        ai_response = model.generate_content(prompt)
        
        status_text.text("✨ Formatting results...")
        progress_bar.progress(90)
        
        cleaned_json = clean_ai_json(ai_response.text)
        
        # 1. Auto-fill missing apply_link
        apply_link = cleaned_json.get("apply_link", "")
        if not apply_link:
            apply_link = url
        
        # 2. Shorten the link
        short_link = shorten_url(apply_link)
        cleaned_json["apply_link"] = short_link
        
        formatted_message = format_job_message(cleaned_json)
        
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
        
        return {
            "status": "success",
            "parsed_output": cleaned_json,
            "formatted_message": formatted_message
        }
        
    except Exception as e:
        import traceback
        error_details = str(e)
        st.error(f"Error: {error_details}")
        st.code(traceback.format_exc())
        return {
            "status": "error",
            "message": error_details
        }

# Main UI
st.title("💼 Job Auto Formatter")
st.markdown("Automatically extract and format job postings from URLs")

# Input section
st.markdown("### 📋 Enter Job URL")
url = st.text_input(
    "Paste job link here...",
    placeholder="https://www.linkedin.com/jobs/view/...",
    label_visibility="collapsed"
)

# Extract button
if st.button("🚀 Generate Job Post", type="primary"):
    if not url:
        st.warning("⚠️ Please enter a valid job link.")
    else:
        # Validate URL
        if not url.startswith(("http://", "https://")):
            st.error("❌ Please enter a valid URL starting with http:// or https://")
        else:
            result = extract_job_details(url)
            
            if result["status"] == "success":
                st.success("✅ Job details extracted successfully!")
                
                # Display formatted message
                st.markdown("### 📝 Formatted Job Post")
                st.markdown(result["formatted_message"])
                
                # Copy button
                st.code(result["formatted_message"], language=None)
                
                # Store in session state for copy functionality
                st.session_state.last_formatted_message = result["formatted_message"]
                
                # Show parsed details in expander
                with st.expander("🔍 View Parsed Details"):
                    st.json(result["parsed_output"])
            else:
                st.error(f"❌ Failed to extract job details: {result.get('message', 'Unknown error')}")

# Copy functionality
if 'last_formatted_message' in st.session_state:
    if st.button("📋 Copy to Clipboard"):
        st.code(st.session_state.last_formatted_message, language=None)
        st.success("✅ Message copied! (Select and copy manually, or use the code block above)")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Powered by Google Gemini AI 🤖</p>
        <p>For issues or questions, contact: telugucodingcommunity88@gmail.com</p>
    </div>
""", unsafe_allow_html=True)

