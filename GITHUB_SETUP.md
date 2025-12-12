# GitHub Setup Guide

Follow these steps to upload your backend (and entire project) to GitHub.

## Option 1: Using GitHub Desktop (Easiest)

1. **Download GitHub Desktop** (if not installed):
   - Go to https://desktop.github.com
   - Download and install

2. **Open GitHub Desktop**:
   - Click "File" → "Add Local Repository"
   - Browse to: `C:\Users\ravisaikumar88\Desktop\job-auto-formatter`
   - Click "Add Repository"

3. **Create GitHub Repository**:
   - Click "Publish repository" button
   - Choose a name (e.g., `job-auto-formatter`)
   - Make it Public or Private (your choice)
   - Click "Publish Repository"

Done! Your code is now on GitHub.

---

## Option 2: Using Git Command Line

### Step 1: Install Git (if not installed)

1. Download Git from: https://git-scm.com/download/win
2. Install with default settings
3. Restart your terminal/PowerShell

### Step 2: Initialize Git Repository

Open PowerShell in your project folder and run:

```powershell
cd C:\Users\ravisaikumar88\Desktop\job-auto-formatter
git init
```

### Step 3: Add All Files

```powershell
git add .
```

### Step 4: Create First Commit

```powershell
git commit -m "Initial commit: Job Auto Formatter"
```

### Step 5: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon → "New repository"
3. Name it: `job-auto-formatter`
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 6: Connect and Push

GitHub will show you commands. Run these in PowerShell:

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/job-auto-formatter.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Option 3: Using VS Code (If you have it)

1. Open VS Code in your project folder
2. Click the Source Control icon (left sidebar)
3. Click "Initialize Repository"
4. Click "+" to stage all files
5. Type commit message: "Initial commit"
6. Click "✓ Commit"
7. Click "..." → "Publish Branch"
8. Choose GitHub, name your repo, and publish

---

## What Gets Uploaded?

✅ **Will be uploaded:**
- All source code (backend/main.py, frontend/src, etc.)
- Configuration files (requirements.txt, package.json, etc.)
- Deployment configs (render.yaml, vercel.json, etc.)
- README and documentation

❌ **Will NOT be uploaded** (protected by .gitignore):
- `.env` files (your API keys)
- `node_modules/` folder
- `venv/` folder (Python virtual environment)
- `__pycache__/` folders

---

## After Uploading

Once your code is on GitHub, you can:
1. Deploy backend to Render/Railway
2. Deploy frontend to Vercel/Netlify
3. Access your app from anywhere!

---

## Need Help?

If you encounter any issues:
- Make sure Git is installed and in your PATH
- Check that you're logged into GitHub
- Verify your repository name doesn't have spaces or special characters

