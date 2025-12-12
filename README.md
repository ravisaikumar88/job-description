# Job Auto Formatter

Automatically extract and format job postings from URLs into a standardized message format.

## Features

- 🔗 Extract job details from any job posting URL
- 🤖 AI-powered extraction using Google Gemini
- 📱 Mobile-friendly interface
- 📋 One-click copy to clipboard
- 🚀 Ready for deployment

## Tech Stack

- **Backend**: FastAPI, Google Gemini AI, Playwright, BeautifulSoup
- **Frontend**: React, Vite

## Quick Start (Local Development)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
playwright install chromium
# Create .env file with GOOGLE_API_KEY=your_key
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

**Quick Summary:**
1. Push code to GitHub
2. Deploy backend to Render/Railway
3. Deploy frontend to Vercel/Netlify
4. Set environment variables
5. Access from your phone!

## Environment Variables

### Backend (.env)
```
GOOGLE_API_KEY=your_google_gemini_api_key
ALLOWED_ORIGINS=*  # or specific frontend URL
```

### Frontend (.env)
```
VITE_API_URL=https://your-backend-url.onrender.com
```

## License

MIT

