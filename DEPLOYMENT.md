# Deployment Guide for Job Auto Formatter

This guide will help you deploy both the backend and frontend so you can use the app on your phone.

## Prerequisites

1. A GitHub account (to host your code)
2. A Render account (for backend) - Sign up at https://render.com
3. A Vercel or Netlify account (for frontend) - Sign up at https://vercel.com or https://netlify.com
4. Your Google Gemini API key

---


## Step 1: Push Code to GitHub

1. Create a new repository on GitHub
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

---

## Step 2: Deploy Backend (Render)

### Option A: Using Render Dashboard

1. Go to https://render.com and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `job-auto-formatter-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`
5. Add Environment Variables:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - `ALLOWED_ORIGINS`: `*` (or your frontend URL later)
6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. **Copy your backend URL** (e.g., `https://job-auto-formatter-api.onrender.com`)

### Option B: Using Railway (Alternative)

1. Go to https://railway.app and sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
5. Set root directory to `backend`
6. Railway will auto-detect Python and deploy
7. **Copy your backend URL**

---

## Step 3: Deploy Frontend (Vercel - Recommended)

### Using Vercel:

1. Go to https://vercel.com and sign in
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - `VITE_API_URL`: Your backend URL from Step 2 (e.g., `https://job-auto-formatter-api.onrender.com`)
6. Click "Deploy"
7. **Copy your frontend URL** (e.g., `https://job-auto-formatter.vercel.app`)

### Using Netlify (Alternative):

1. Go to https://netlify.com and sign in
2. Click "Add new site" → "Import an existing project"
3. Connect your GitHub repository
4. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
5. Add Environment Variable:
   - `VITE_API_URL`: Your backend URL from Step 2
6. Click "Deploy site"
7. **Copy your frontend URL**

---

## Step 4: Update Backend CORS (If Needed)

If you deployed frontend to a specific domain, update backend CORS:

1. Go to your Render/Railway dashboard
2. Update environment variable:
   - `ALLOWED_ORIGINS`: Your frontend URL (e.g., `https://job-auto-formatter.vercel.app`)
3. Redeploy the backend

---

## Step 5: Test on Your Phone

1. Open your phone's browser
2. Navigate to your frontend URL (e.g., `https://job-auto-formatter.vercel.app`)
3. Paste a job URL and test!

---

## Troubleshooting

### Backend Issues:

- **Playwright not working**: Make sure build command includes `playwright install chromium`
- **API key error**: Verify `GOOGLE_API_KEY` is set correctly in environment variables
- **CORS errors**: Check `ALLOWED_ORIGINS` includes your frontend URL

### Frontend Issues:

- **Can't connect to backend**: Verify `VITE_API_URL` is set correctly
- **Build fails**: Make sure you're in the `frontend` directory and dependencies are installed

### Common Solutions:

1. **Check logs**: Both Render and Vercel show deployment logs
2. **Redeploy**: Sometimes a simple redeploy fixes issues
3. **Environment variables**: Double-check all env vars are set correctly

---

## Quick Deploy Commands (If using CLI)

### Render CLI:
```bash
npm install -g render-cli
render login
render deploy
```

### Vercel CLI:
```bash
npm install -g vercel
cd frontend
vercel
```

---

## Cost

- **Render**: Free tier available (spins down after inactivity)
- **Vercel**: Free tier available (unlimited for personal projects)
- **Netlify**: Free tier available
- **Railway**: Free tier with $5 credit/month

All platforms offer free tiers suitable for personal projects!

---

## Need Help?

If you encounter issues:
1. Check the deployment logs in your platform's dashboard
2. Verify all environment variables are set
3. Make sure your GitHub repo is public (or connect via private repo access)

Good luck with your deployment! 🚀

