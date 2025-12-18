from fastapi import FastAPI
from dotenv import load_dotenv
import os
import requests
import google.generativeai as genai

load_dotenv(dotenv_path=".env")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# CORS configuration - allow all origins for production
# In production, you can restrict this to your frontend domain
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins_env == "*":
    # When using wildcard, credentials must be False
    allowed_origins = ["*"]
    allow_credentials = False
else:
    # When specifying origins, we can use credentials
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
    allow_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "Job Auto Formatter API is running",
        "gemini_key_loaded": GEMINI_API_KEY is not None,
    }

@app.get("/health")
def health_check():
    """Health check endpoint for keep-alive pings"""
    return {
        "status": "healthy",
        "service": "Job Auto Formatter API"
    }

from pydantic import BaseModel

class JobRequest(BaseModel):
    url: str



from bs4 import BeautifulSoup

import json
import re

def shorten_url(url: str):
    try:
        tinyurl_api = f"https://tinyurl.com/api-create.php?url={url}"
        short_url = requests.get(tinyurl_api).text

        # TinyURL returns literally "Error" on failure
        if short_url.lower() == "error":
            return url  # fallback to original link

        return short_url
    except:
        return url  # fallback if API fails

def format_job_message(data):
    return f"""
**COMPANY** : {data.get('company', '')}
**ROLE** : {data.get('role', '')}
**LOCATION** : {data.get('location', '')}
**EXPERIENCE** : {data.get('experience', '')}

**Apply Link:** {data.get('apply_link', '')}

For More Job Updates & Important Updates Like this  
Follow Us On WhatsApp :  
https://whatsapp.com/channel/0029VagenEZFSAtDBtDg9v2y

Reach us at  
telugucodingcommunity88@gmail.com

Please Share With Your College Groups & Friends
""".strip()




def clean_ai_json(ai_text: str):
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

from playwright.sync_api import sync_playwright

def fetch_dynamic_html(url: str):
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
        print("Dynamic fetch error:", e)
        return ""

@app.options("/extract")
async def options_extract():
    """Handle CORS preflight for /extract endpoint"""
    return {"message": "OK"}

@app.post("/extract")
def extract_job_details(request: JobRequest):
    try:
        # 1. Download HTML
        response = requests.get(request.url, timeout=10)
        html = response.text

        # 2. Clean text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        # If text is too short (likely LinkedIn), use Playwright fallback
        if len(text) < 300:
            dynamic_html = fetch_dynamic_html(request.url)
            if dynamic_html:
                soup = BeautifulSoup(dynamic_html, "html.parser")
                text = soup.get_text(separator=" ", strip=True)

                # 🔥 Extract only the real job description on LinkedIn
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

            - company
            - role
            - location
            - experience (if not available, return "" not None)
            - apply_link (if not found, return "")

            STRICT RULES:
            - Return ONLY a pure JSON.
            - No comments, no markdown, no explanation.

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


        model = genai.GenerativeModel("models/gemini-2.5-flash")

        ai_response = model.generate_content(prompt)

        cleaned_json = clean_ai_json(ai_response.text)

        # 1. Auto-fill missing apply_link
        apply_link = cleaned_json.get("apply_link", "")
        if not apply_link:
            apply_link = request.url

        # 2. Shorten the link
        short_link = shorten_url(apply_link)

        cleaned_json["apply_link"] = short_link

        formatted_message = format_job_message(cleaned_json)

        return {
            "status": "Job message generated",
            "url": request.url,
            "parsed_output": cleaned_json,
            "formatted_message": formatted_message
        }


    except Exception as e:
        import traceback
        error_details = str(e)
        print(f"Error in extract_job_details: {error_details}")
        print(traceback.format_exc())
        return {
            "status": "error", 
            "message": error_details,
            "error_type": type(e).__name__
        }
