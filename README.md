# Job Auto Formatter

Automatically extract and format job postings from URLs into a standardized message format using AI.

## Features

- 🔗 Extract job details from any job posting URL (LinkedIn, Workday, etc.)
- 🤖 AI-powered extraction using Google Gemini 2.5 Flash
- 🌐 Automatic handling of dynamic content with Playwright
- 📱 Mobile-friendly Streamlit interface
- 📋 Easy copy-to-clipboard functionality
- 🚀 One-click deployment to Streamlit Cloud

## Tech Stack

- **Framework**: Streamlit
- **AI**: Google Gemini 2.5 Flash
- **Web Scraping**: BeautifulSoup4, Playwright
- **URL Shortening**: TinyURL API

## Quick Start (Local Development)

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd job-description
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browser**
   ```bash
   playwright install chromium
   ```

5. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

6. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## Deployment to Streamlit Cloud

### Step 1: Push to GitHub

Make sure your code is pushed to a GitHub repository:
```bash
git add .
git commit -m "Initial Streamlit app"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to: `app.py`
6. Click "Deploy"

### Step 3: Configure Secrets

1. In your Streamlit Cloud app dashboard, go to **Settings** → **Secrets**
2. Add your Google API key:
   ```toml
   GOOGLE_API_KEY = "your_google_gemini_api_key_here"
   ```
3. Save and wait for the app to redeploy

### Step 4: Verify Deployment

The app will automatically:
- Install Python dependencies from `requirements.txt`
- Install system packages from `packages.txt`
- Run `postBuild` script to install Playwright browser
- Deploy your app

Your app will be available at: `https://your-app-name.streamlit.app`

## Project Structure

```
job-description/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── packages.txt       # System packages for Streamlit Cloud
├── postBuild          # Post-build script (installs Playwright)
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## How It Works

1. **User Input**: Paste a job posting URL
2. **Web Scraping**: 
   - First attempts simple HTTP request
   - Falls back to Playwright for dynamic content (LinkedIn, etc.)
3. **AI Extraction**: Google Gemini AI extracts:
   - Company name
   - Job role
   - Location
   - Experience requirements
   - Apply link
4. **Formatting**: Formats into standardized message template
5. **URL Shortening**: Shortens apply link using TinyURL
6. **Output**: Displays formatted message ready to copy

## Environment Variables

### Local Development (.env file)
```
GOOGLE_API_KEY=your_google_gemini_api_key
```

### Streamlit Cloud (Secrets)
```toml
GOOGLE_API_KEY = "your_google_gemini_api_key"
```

## Troubleshooting

### Playwright Installation Issues

If you see Playwright errors:
- **Local**: Run `playwright install chromium`
- **Streamlit Cloud**: Ensure `packages.txt` and `postBuild` are in your repo

### API Key Not Found

- **Local**: Check your `.env` file exists and has `GOOGLE_API_KEY`
- **Streamlit Cloud**: Verify secrets are set in Settings → Secrets

### Dynamic Content Not Loading

- The app automatically uses Playwright for dynamic pages
- If extraction fails, try the URL again (some sites have rate limiting)

## Supported Job Sites

- ✅ LinkedIn
- ✅ Workday
- ✅ Most standard job posting sites
- ✅ Any site with static HTML

## License

MIT

## Support

For issues or questions:
- Email: telugucodingcommunity88@gmail.com
- WhatsApp: [Join our channel](https://whatsapp.com/channel/0029VagenEZFSAtDBtDg9v2y)
